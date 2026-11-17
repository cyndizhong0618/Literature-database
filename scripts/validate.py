#!/usr/bin/env python3
"""Validate local structure only; no network access or writes."""
import csv
import json
import re
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
errors = []
def fail(s):
    errors.append(s)
def load_csv(path, expected):
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != expected:
            fail(str(path.relative_to(ROOT)) + ": incorrect header/order")
        rows = list(reader)
    for i, row in enumerate(rows, 2):
        if None in row or any(v is None for v in row.values()):
            fail(f"{path.name}:{i}: incorrect number of columns")
    return rows
def items(v):
    return v.split("|") if v else []
def valid_date(v):
    try:
        return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", v)) and bool(date.fromisoformat(v))
    except ValueError:
        return False
def local_path(v):
    p = Path(v)
    return not p.is_absolute() and ".." not in p.parts and chr(92) not in v
def check():
    fields = json.loads((ROOT/"schema/fields.json").read_text())
    tags = json.loads((ROOT/"schema/tags.json").read_text())
    projects = json.loads((ROOT/"schema/projects.json").read_text())
    vocabulary = {k+":"+v for k, values in tags.items() for v in values}
    specs = fields["fields"]
    rows = load_csv(ROOT/"data/papers.csv", [x["name"] for x in specs])
    ids, keys, dois, byid = set(), set(), set(), {}
    for n, raw in enumerate(rows, 2):
        row = {k:(v or "").strip() for k,v in raw.items() if k is not None}
        prefix = f"papers.csv:{n}"
        for field in specs:
            k = field["name"]
            value = row.get(k, "")
            if field["required"] == "yes" and not value:
                fail(f"{prefix}: missing {k}")
            if value and field["type"] == "enum" and value not in field["description"].split("|"):
                fail(f"{prefix}: invalid {k}")
            if value and field["type"] == "date" and not valid_date(value):
                fail(f"{prefix}: invalid date {k}")
            if value and field["type"] == "uri" and not re.match(r"^https?://[^\s]+$",value):
                fail(f"{prefix}: invalid URL {k}")
        pid = row.get("paper_id","")
        if not re.fullmatch(r"lit-\d{6}", pid):
            fail(f"{prefix}: invalid paper_id")
        key = row.get("citekey","")
        if not re.fullmatch(r"[a-z][a-z0-9]*",key):
            fail(f"{prefix}: invalid citekey")
        for value, seen, label in [(pid,ids,"paper_id"),(key,keys,"citekey")]:
            if value in seen:
                fail(f"{prefix}: duplicate {label}")
            seen.add(value)
        byid[pid] = row
        doi = row.get("doi","")
        if doi:
            normalized = re.sub(r"^(https?://(dx\.)?doi.org/|doi:\s*)","",doi.lower()).strip()
            if doi != normalized or not re.fullmatch(r"10\.\d{4,9}/\S+",doi):
                fail(f"{prefix}: DOI must be normalized")
            if normalized in dois:
                fail(f"{prefix}: duplicate DOI")
            dois.add(normalized)
        year = row.get("year","")
        if year and not re.fullmatch(r"\d{4}",year):
            fail(f"{prefix}: invalid year")
        for k,allowed in [("projects",set(projects)),("tags",vocabulary)]:
            values = items(row.get(k,""))
            if len(values)!=len(set(values)) or any(v not in allowed for v in values):
                fail(f"{prefix}: invalid or duplicate {k}")
        if row.get("reading_status")=="excluded" and not row.get("screening_reason"):
            fail(f"{prefix}: excluded requires reason")
        path = row.get("note_path","")
        if path and (path!=f"notes/{pid}.md" or not local_path(path) or not (ROOT/path).is_file()):
            fail(f"{prefix}: invalid/missing note_path")
        if row.get("reading_status")=="read" and not path:
            fail(f"{prefix}: read requires note_path")
        a,u = row.get("added_on",""),row.get("updated_on","")
        if valid_date(a) and valid_date(u) and u<a:
            fail(f"{prefix}: updated_on before added_on")
    matrix_headers = ["paper_id","use_role","research_question","theory","design_sample","key_finding","evidence_locator","relevance","boundary_or_gap","verification_status"]
    for code in projects:
        p = ROOT/"projects"/code
        if not (p/"README.md").is_file():
            fail(f"{code}: missing README")
        seen = set()
        for n,row in enumerate(load_csv(p/"matrix.csv", matrix_headers),2):
            pid = row.get("paper_id")
            prefix = f"{code}/matrix.csv:{n}"
            if pid not in ids or pid in seen:
                fail(f"{prefix}: unknown/duplicate paper_id")
            seen.add(pid)
            if pid in byid and code not in items(byid[pid].get("projects","")):
                fail(f"{prefix}: project not assigned in master")
            if row.get("use_role") not in {"background","theory","mechanism","competing-explanation","method","boundary"}:
                fail(f"{prefix}: invalid use_role")
            if row.get("verification_status") not in {"unverified","verified"}:
                fail(f"{prefix}: invalid verification_status")
            if row.get("verification_status")=="verified" and not row.get("evidence_locator"):
                fail(f"{prefix}: verified requires evidence_locator")
    return len(rows),len(projects)
if __name__=="__main__":
    try:
        count, projects = check()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        fail(str(exc))
        count, projects = 0, 0
    if errors:
        print("\n".join("ERROR: "+e for e in errors))
        sys.exit(1)
    print(f"PASS: {count} papers; {projects} project matrices. Content accuracy requires manual review.")

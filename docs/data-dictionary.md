# 欄位字典

空值使用空白儲存格，不填 NA、null 或「待補」。清單使用 |，單一項目不可含 |。CSV 內含逗號、引號或換行時使用標準 CSV quoting。

| 欄位 | 型別 | 必填 | 定義 |
|---|---|---|---|
| paper_id | string | yes | 永久識別碼，例如 lit-000001；只增不改、不重用 |
| citekey | string | yes | ASCII 引用鍵，例如 wang2026shorttopic；未知作者或年用 anon/nd；碰撞加 a,b |
| title | string | yes | 正式原文標題；不可自行翻譯取代 |
| authors | string | no | 依原順序 Last, Given；作者間使用 | |
| year | integer|null | no | 正式出版年；未知留空 |
| publication_type | enum | yes | journal_article|conference_paper|book|book_chapter|preprint|thesis|report|other |
| venue | string | no | 期刊、會議或出版者全名 |
| doi | string | no | 小寫裸 DOI；移除 https://doi.org/ 及 doi: 前綴 |
| url | uri | no | 無 DOI 時優先使用出版者或機構永久連結 |
| language | string | no | 例如 en、zh-Hant、zh-Hans |
| abstract | string | no | 自行摘要或可合法使用的摘要；公開庫避免大量複製 |
| projects | list | no | 對應 projects 中專案代碼，以 | 分隔 |
| tags | list | no | 受控詞彙 namespace:value，以 | 分隔 |
| reading_status | enum | yes | inbox|screened|reading|read|excluded |
| priority | enum | yes | high|medium|low |
| added_on | date | yes | YYYY-MM-DD |
| updated_on | date | yes | YYYY-MM-DD；不得早於 added_on |
| screening_reason | string | no | 納入理由；excluded 必填排除理由 |
| note_path | path | no | 相對於根目錄；已讀必填 notes/<paper_id>.md |
| source_url | uri | yes | 實際發現/查核此筆資料的來源連結 |
| metadata_checked_on | date | no | 核對作者、標題、年分、DOI 的日期 |
| fulltext_status | enum | yes | not_sought|available_local|open_access|unavailable |
| fulltext_url | uri | no | 合法公開全文連結；不放含權杖或個人雲端連結 |

年分、DOI 未知可先留空；在未核對前不補猜測值。無 DOI 的記錄仍須 source_url。

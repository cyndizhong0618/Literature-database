# Literature-database

供 Keyi 使用的跨研究主題文獻資料庫。以一份 CSV 管理書目與閱讀進度，以 Markdown 保存可追溯閱讀筆記，以專案矩陣支援理論比較與論文寫作。

[開啟私人文獻研究室](https://keyi-literature-hub.slopedbagel8.chatgpt.site)

第一版不預載未查核文獻，data/papers.csv 與各矩陣目前只有欄位。下載後即可加入第一篇真實文獻。Python 3.9+ 只用於驗證，日常編輯不需要程式套件或資料庫服務。

## 檔案入口

| 路徑 | 用途 |
|---|---|
| data/papers.csv | 唯一書目主表，一篇一列 |
| schema/fields.json | 機器可讀欄位契約（自訂格式，非 JSON Schema） |
| schema/tags.json | 受控標籤唯一來源 |
| schema/projects.json | 專案代碼與名稱 |
| notes/ | 每篇一份可公開的閱讀筆記 |
| projects/<code>/matrix.csv | 專案證據矩陣，透過 paper_id 參照主表 |
| templates/reading-note.md | 閱讀筆記模板 |
| docs/data-dictionary.md | 完整欄位定義、必填與空值規則 |
| docs/naming-and-tags.md | 識別碼、引用鍵與標籤規範 |
| docs/workflow.md | 收錄、去重、閱讀、匯出與查核流程 |
| docs/publication-policy.md | 公開範圍、全文及私人內容處理 |
| scripts/validate.py | 主表、詞彙、筆記與矩陣檢查 |

## 研究主題

- [工業維護暗資料、知識圖譜與永續知識管理](projects/dark-data-kms/README.md)（dark-data-kms）
- [智能政務代理的公眾信任與支持](projects/gov-ai-trust/README.md)（gov-ai-trust）
- [資料洩漏通知具象度、威脅、效能與資訊保護行為](projects/breach-concreteness/README.md)（breach-concreteness）
- [Instagram 人寵親密、業配與互動](projects/human-pet-bond/README.md)（human-pet-bond）
- [聊天機器人幽默、信任與共同服務補救](projects/chatbot-humor/README.md)（chatbot-humor）
- [真人網紅人格反差、評估目標與真實性](projects/influencer-persona/README.md)（influencer-persona）
- [AI 能力進步、個人需求與持續使用](projects/ai-continuance/README.md)（ai-continuance）
- [寵物擬人化內容與觀眾反應](projects/pet-anthropomorphism/README.md)（pet-anthropomorphism）

專案歸屬與標籤分開：前者表示「用在哪項研究」，後者表示「這篇文獻談什麼」。同篇文獻可以連到多個專案，不複製書目或筆記。

## 五分鐘開始

1. 開啟 data/papers.csv，依 docs/data-dictionary.md 新增一列。先填 paper_id、citekey、title、publication_type、reading_status、priority、added_on、updated_on、source_url、fulltext_status。
2. paper_id 從 lit-000001 起；日期用 YYYY-MM-DD。未知欄位留空。source_url 填實際找到或查核文獻的來源，不能填猜測連結。
3. projects 可填 breach-concreteness；tags 例如 topic:message-concreteness|method:experiment，但僅在文獻確實涉及時填入。
4. 複製 templates/reading-note.md 到 notes/lit-000001.md，填原文發現、頁碼／表號與個人解讀；主表 note_path 填同一路徑。
5. 把同一 paper_id 加入相關專案 matrix.csv，再從根目錄執行：

```bash
python3 scripts/validate.py
```

看到 PASS 表示格式與內部參照通過。驗證不核實論文存在、DOI 真偽、結論正確性或內容是否適合公開，這些仍須人工閱讀確認。

## 一致性規則

- paper_id 永久不變，citekey 可在補齊資料後修正。
- 一篇一列；有 DOI 先依正規化 DOI 去重，無 DOI 再人工比對標題／作者／年分。
- UTF-8、逗號分隔；多值以 | 分隔。空值為空白，不填 NA。
- 閱讀狀態為 inbox → screened → reading → read；排除用 excluded 並記理由。需要重讀可退回 reading。
- 原文證據、自己的解讀與新研究想法分段保存；統計關聯不可直接寫成因果。
- 正式書目只存主表；專案矩陣不重新維護作者與期刊等資訊。
- 表格可用試算表編輯，但 CSV 保持唯一主檔；詳細匯入方式見 docs/workflow.md。

## 公開使用

此 repository 目前公開。只放可公開分享的書目、自行撰寫筆記與規則，全文使用合法連結，未發表想法與私人內容留在 private/。詳見 docs/publication-policy.md。目前未設定開源授權。

## 維護

新增標籤先更新 schema/tags.json；新增專案先更新 schema/projects.json 並複製既有專案矩陣欄頭。修改欄位時同步更新 fields.json、主表欄頭、字典及驗證器，記錄於 CHANGELOG.md。每次整理後執行驗證，再人工檢查證據與公開範圍。

本版為 1.0.0。透過私人視覺化介面瀏覽；新增文獻可直接在 ChatGPT 提供 PDF、DOI 或連結，並指定研究專案。由助理核對、去重、整理後更新。

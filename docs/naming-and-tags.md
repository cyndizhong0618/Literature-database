# 命名與標籤

paper_id 使用 lit- 加六位數，從 lit-000001 起依現有最大值加一，不因排序、刪除或改題而重新編號。citekey 使用首位作者 ASCII 姓氏＋出版年＋短主題，例如 wang2026privacy；同鍵依建立順序加 a、b。這只是命名示意，不代表真實論文。unknown 年用 nd，無作者用 anon；核對後可改 citekey，但 paper_id 保持不變。筆記路徑以 paper_id 命名，可避免改引用鍵造成斷鏈。

資料夾與其他檔名用小寫英文 kebab-case；日期用 YYYY-MM-DD。正文與筆記可用繁體中文，論文題目維持原文。

標籤格式為 namespace:value，清單以 | 分隔。topic=議題，theory=理論，construct=變項，method=方法，context=情境。不用標籤承載閱讀狀態或研究專案。只標記文獻實際涵蓋內容，例如你的研究使用歸因理論，不表示所有相關文獻都應標 theory:attribution。

schema/tags.json 為受控詞彙唯一來源。新增標籤前先找同義詞；確需新增時先更新詞彙檔並於 CHANGELOG.md 說明。不得同時建立 message-concreteness、concreteness 等同義標籤。新增研究方向只需更新 schema/projects.json 並新增 projects/<code>/README.md、matrix.csv。

第一版詞彙是起點，不代表已完成理論選擇，也不預設 trait compatibility 已納入最終網紅模型。

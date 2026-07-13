# 富蘭克林教育機構一頁式網站

依照 `mockup/Sample2.jpg` 製作的響應式招生網站，包含課程介紹、課後時間軸、成果輪播、家長回饋與預約諮詢 CTA。

網站使用完全相對路徑與一般 JavaScript 腳本，可直接雙擊根目錄的 `index.html` 離線瀏覽；Vite 僅作為可選的開發伺服器。

## 開發

```bash
npm install
npm run dev
```

若只需本機查看，也可以直接開啟 `index.html`，不需要啟動伺服器。

## 正式建置

```bash
npm run build
```

建置結果會安全覆寫到 `dist/`，不轉譯、不雜湊，也不改寫資源路徑。建置程序會同步檢查所有相對資源是否存在，以及內嵌腳本是否能正確解析。

## 主要檔案

- `index.html`：頁面內容與語意結構
- `src/styles.css`：完整響應式視覺樣式
- `index.html` 內嵌腳本：行動版選單與學習現場輪播互動（含滑鼠拖曳捲動）
- `public/images/`：Logo、吉祥物及網站照片

## 素材管線

- `scripts/grade_classroom_photos.py`：教室照片批次調色（暖化白平衡、提亮、壓低紅色椅子飽和度），從 `source-assets/classroom-pregrade/` 的未調色快照重跑，不會重複疊加；完成後自動重產 hero 裁切。
- `scripts/create_hero_crops.py`：從 `classroom-hero.webp` 產出桌機／平板／手機三種 hero 裁切。
- `scripts/subset_display_font.py`：掃描 `index.html` 全部字元，從 `source-assets/fonts/jf-openhuninn-2.1.ttf` 重產標題字型子集（需 `pip install fonttools brotli`）。標題文案改字後需重跑，否則新字會 fallback 成黑體。
- `scripts/subset_noto_font.py`：同樣掃描 `index.html`，重產內文字型子集。**任何中文文案增刪後兩支都要重跑。**

## 視覺慣例

素材依角色分工，新增元素時請沿用：

- **插畫物件**用生成的手繪 webp（緞帶、裝飾物、圖示）；**邊緣與 UI**用 inline SVG／data-URI（撕紙邊、波浪、聯絡圖示、箭頭）；**氛圍色塊**用純 CSS。
- 標題左右的小裝飾必須是**單一實心剪影**。像 `decor-sparkle-trail-v1` 這種細碎散點的素材，縮到標題尺寸會糊成灰塵，只適合 3rem 以上的區塊點綴。
- 標題的字級掛在 `.section-title-row` 上，h2 與裝飾一律用 **em** 相對它。新增裝飾請沿用 em，不要寫 rem——否則 1280px 以下 `html` 的 `font-size` 不再隨 vw 縮放，裝飾會跟標題文字脫鉤。各圖的透明留白量不同，em 值是逐個調到「看起來一樣重」，不是數字一致。
- 頁面色彩節奏刻意讓冷色出現三次（hero 綠波、孩子的一天、分校據點），避免整頁塌成一片米色。
- 標題兩側的空白帶（標題區 42.5rem、容器 73.75rem，各餘約 15.6rem）用 `.heading-flourish` 填裝飾。它是 `z-index: -1` + `pointer-events: none`，永遠畫在文字底層、不吃點擊；960px 以下空白帶消失，整組隱藏。新增時務必確認上不戳撕紙邊、下不被卡片的不透明底蓋掉半截。

## 上線前需確認

所有待替換的佔位內容都標了 `data-placeholder` 屬性，`grep -n 'data-placeholder' index.html` 可一次列出。

- **費用區**：所有數字（每週堂數、一期堂數／時數、一期費用、每堂單價）皆為佔位。
- **師資區**：老師姓名、職稱、資歷為佔位；照片位是刻意設計的手繪相框。**照片上線前必須取得每位老師的肖像授權**；未授權者保留相框即可，不要用 AI 生成人臉。
- **分校區與 footer**：斗六／斗南兩校的地址、電話、營業時間為佔位；`tel:` 連結也是假號碼。
- **學習現場輪播**：目前只有課堂互動照，教室環境照到位後直接追加 `.gallery-card` 即可。
- Email 仍是 mockup 示意內容。
- footer 的四個社群圖示是**停用狀態**（`<a>` 沒有 `href`，帶 `aria-disabled`）。拿到真實網址後補上 `href`、移除 `aria-disabled` 與 `title` 即可。先前它們是 `href="#"`，點下去會跳回頁首。
- 導覽列右側與 hero、CTA 的三顆「加 LINE 詢問」按鈕**目前點了沒有反應**，等 LINE 官方帳號連結。
- CTA 區的「加入 LINE 詢問」按鈕暫以 `hidden` 隱藏（`index.html` 內附註解），補上 LINE 官方帳號連結後移除 hidden 並改回連結即可。

另：`JFOpenHuninn-Display-Subset.woff2` 目前被 preload 但實際上沒有任何元素渲染得到它（所有套用它的規則都被 id／類別選擇器覆寫回 Noto 900）。若確定不用，移除 `@font-face`、preload 與 `.display-font` 可省下約 90KB。

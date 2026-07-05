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
- `index.html` 內嵌腳本：行動版選單與成果輪播互動
- `public/images/`：Logo、吉祥物及網站照片

## 素材管線

- `scripts/grade_classroom_photos.py`：教室照片批次調色（暖化白平衡、提亮、壓低紅色椅子飽和度），從 `source-assets/classroom-pregrade/` 的未調色快照重跑，不會重複疊加；完成後自動重產 hero 裁切。
- `scripts/create_hero_crops.py`：從 `classroom-hero.webp` 產出桌機／平板／手機三種 hero 裁切。
- `scripts/subset_display_font.py`：掃描 `index.html` 全部字元，從 `source-assets/fonts/jf-openhuninn-2.1.ttf` 重產標題字型子集（需 `pip install fonttools brotli`）。標題文案改字後需重跑，否則新字會 fallback 成黑體。

## 上線前需確認

目前地址、電話、Email、營業時間與社群連結依 mockup 示意內容建立。正式上線前，請換成機構的真實資訊。CTA 區的「加入 LINE 詢問」按鈕暫以 `hidden` 隱藏（`index.html` 內附註解），補上 LINE 官方帳號連結後移除 hidden 並改回連結即可。

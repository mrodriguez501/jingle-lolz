# 🎄 jingle-lolz

**Savor 25 delicious morsels of internet glory.**

> One new door unlocks each day, December 1–25, 2026. Open it to discover a marvelous treasure from days of yore.

A self-contained, festive viral-video Advent calendar. Each numbered door swings open to reveal a QR code and a clickable **Watch the surprise** link. The mobile version has a full-size reveal panel, so viewers can watch on the same phone without scanning a QR code.

[Open the live calendar](https://mrodriguez501.github.io/jingle-lolz/)

## 📁 Repository contents

```text
jingle-lolz/
├── .github/
│   └── workflows/
│       └── deploy-pages.yml        # Validate and deploy to GitHub Pages
├── site/
│   ├── index.html                  # PUBLISHED mobile-friendly daily calendar
│   └── .nojekyll                   # Publish static files without Jekyll processing
├── variants/
│   ├── mobile-daily.html           # Same as published version
│   ├── desktop-daily.html          # Wider desktop layout, with date locks
│   ├── mobile-all-unlocked.html    # Mobile test: all 25 doors unlocked
│   └── desktop-all-unlocked.html   # Desktop test: all 25 doors unlocked
├── data/
│   ├── videos.json                 # Structured 25-video playlist + backups
│   ├── videos.csv                  # Spreadsheet-friendly answer key
│   └── ANSWER_KEY.md              # Day-by-day clickable links (SPOILERS)
├── scripts/
│   ├── validate.py                 # Standard-library checks used in GitHub Actions
│   └── sync_videos.py              # Optional QR / link regeneration tool
├── .gitignore
└── README.md
```

## 🗓️ Countdown behavior

- The release schedule is **December 1–25, 2026**, at **12:00 a.m. America/New_York (Eastern Time)**.
- December 1 opens Day 1; December 2 opens Days 1–2; and so on until all 25 doors are available December 25.
- Previously unlocked doors stay accessible. Opened-door progress is stored in that visitor's browser (`localStorage`).
- The calendar checks the date again if the tab stays open overnight.
- **Before December 1 all 25 doors are locked.** After December 25, 2026 all 25 remain available indefinitely.
- This is a **client-side**, not tamper-proof lock. A person inspecting the site source or changing their device clock can access future links. It does not hide video URLs from technically inclined users.
- Video playback occurs externally on **YouTube** and **Vimeo**. You must have internet access to watch them. Third-party uploads may disappear, be region-restricted, or ask viewers to sign in.

## 🧪 Test a door before December 1

Open `variants/mobile-all-unlocked.html` in a browser. Click Door 1, confirm the QR code appears, then click **Watch the surprise** and check that the video plays. Try Day 11 to check the backup link. The live calendar follows the Eastern Time release schedule.

## 🎥 The 25 videos and how to change them

The complete title / date / primary URL / fallback URL list is available in:

- [`data/ANSWER_KEY.md`](data/ANSWER_KEY.md) — readable, clickable day-by-day key
- [`data/videos.csv`](data/videos.csv) — spreadsheet-friendly export
- [`data/videos.json`](data/videos.json) — data file to edit if you want to swap videos

**The HTML currently contains embedded QR codes and URLs.** Changing only `videos.json` will **not** update the calendar. To update a video:

1. Change that day's `url` (and `backupUrl` if appropriate) in `data/videos.json`.
2. Run:

   ```bash
   python -m pip install 'qrcode[pil]'
   python scripts/sync_videos.py
   python scripts/validate.py
   ```

3. Update the human-readable `data/ANSWER_KEY.md` and `data/videos.csv` to match. (The sync script updates the calendar HTML and QR images, not the prose answer key or CSV.)
4. Commit and push to `main` to trigger the deployment workflow.

## ✅ Verify before sharing

```bash
python scripts/validate.py
```

This checks 25 sequential doors, HTTPS video links, backup parity, embedded QR PNGs, the 2026 date logic, and the four variants. It is also run automatically by GitHub Actions. It **does not** guarantee a YouTube/Vimeo video will play on every phone, so spot-check several videos yourself after deployment.

## ⚠️ Spoilers

The answer key and video URLs are visible in the public repository, and the live page embeds the URLs. Share the calendar link with viewers who want to avoid spoilers.

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| GitHub Pages page is 404 | Verify Settings → Pages source is **GitHub Actions** and check the Actions run completed; wait briefly for the URL to become available. |
| Workflow didn't run | Check the branch is named `main` and `.github/workflows/deploy-pages.yml` exists in the pushed repo. You can also trigger it from **Actions → Run workflow**. |
| Website shows an outdated version | Refresh the published URL; check the latest Actions run and `site/index.html` were pushed. |
| Doors don't open on an iPhone | Use the hosted GitHub Pages URL in Safari/Chrome, not an HTML preview inside a messaging app. |
| Video asks for sign-in or doesn't load | Try the **backup** link if shown, or update `data/videos.json` and regenerate the QR images. |

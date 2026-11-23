# 🎄 jingle-lolz

**Savor 25 delicious morsels of internet glory.**

> One new door unlocks each day, December 1–25, 2026. Open it to discover a marvelous treasure from days of yore.

A self-contained, festive viral-video Advent calendar. Each numbered door swings open to reveal a QR code and a clickable **Watch the surprise** link. The mobile version has a full-size reveal panel, so viewers can watch on the same phone without scanning a QR code.

**Ready to publish with GitHub Pages + GitHub Actions. No Node, build step, backend, API keys, or third-party QR service needed.**

## 🚀 Publish to GitHub Pages with Actions

1. Download and **unzip** the repository ZIP. Keep the directory structure, including the hidden `.github` folder.
2. On GitHub, create a repository such as `jingle-lolz`. Make it empty (don't initialize it with a GitHub README or `.gitignore`). A public repo is simplest for free GitHub Pages hosting.
3. Open a terminal in the extracted **`jingle-lolz` directory** and run:

   ```bash
   git init
   git add .
   git commit -m "Publish jingle-lolz Advent calendar"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/jingle-lolz.git
   git push -u origin main
   ```

   Replace `YOUR_USERNAME` with your GitHub username. Authenticate with GitHub using your existing Git setup or Git Credential Manager.

4. In the GitHub repository, go to **Settings → Pages → Build and deployment → Source → GitHub Actions**.
5. Open the **Actions** tab. If the initial workflow ran before Pages was configured and failed, choose **Deploy jingle-lolz to GitHub Pages → Run workflow** to rerun it.
6. Once deployment succeeds, open the URL shown in the workflow under **github-pages**, usually:

   `https://YOUR_USERNAME.github.io/jingle-lolz/`

7. Text that website URL to friends or family. **Send the website link, not the ZIP or HTML attachment.**

A new push to `main` automatically validates and republishes the site. The workflow at `.github/workflows/deploy-pages.yml` deploys **only the `site/` directory**.

> [GitHub's current Pages deployment instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

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
├── docs/
│   ├── previews/                   # Design preview for project documentation
│   └── legacy-printables/          # OLD paper calendar PDFs (see warning below)
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

## 🧪 Try every door immediately (without publishing spoilers)

Open `variants/mobile-all-unlocked.html` or `variants/desktop-all-unlocked.html` directly in Chrome, Edge, or Safari on your computer.

To **temporarily deploy** the preview version, copy `variants/mobile-all-unlocked.html` to `site/index.html`, commit, and push. **Important:** This will let everybody open all 25 days—don't deploy the preview to your real Advent site by accident. Restore `variants/mobile-daily.html` to `site/index.html` and push again when ready.

**Recommended:** Keep the preview local, and publish `site/index.html` unchanged as the daily countdown.

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

Note: the current packaging preserves all the final confirmed selections, including **Day 11** goat scream (with backup), **Day 14** Marcel on Vimeo (with backup), **Day 23** woman slips on ice, and **Day 25** the original undubbed talking cats.

## ✅ Verify before sharing

```bash
python scripts/validate.py
```

This checks 25 sequential doors, HTTPS video links, backup parity, embedded QR PNGs, the 2026 date logic, and the four variants. It is also run automatically by GitHub Actions. It **does not** guarantee a YouTube/Vimeo video will play on every phone, so spot-check several videos yourself after deployment.

## ⚠️ Spoilers and earlier PDF versions

**The video key and URLs are not secrets.** Anyone with access to a public GitHub repository can view the complete list, and all URLs are embedded in the publicly served HTML. Send people the **Pages URL**, not the repository URL, if you want to preserve the fun.

`docs/legacy-printables/` contains the original **paper** advent calendar and original PDF answer key from an earlier revision. **Those PDFs are outdated**: they may show old versions of some videos, so don't use them as the authoritative list. The current answers are in `data/ANSWER_KEY.md`.

The repository hosts links to third-party videos, **not the video files themselves**. Copyright to those videos remains with their respective owners. No warranties about availability or age appropriateness are implied.

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| GitHub Pages page is 404 | Verify Settings → Pages source is **GitHub Actions** and check the Actions run completed; wait briefly for the URL to become available. |
| Workflow didn't run | Check the branch is named `main` and `.github/workflows/deploy-pages.yml` exists in the pushed repo. You can also trigger it from **Actions → Run workflow**. |
| Website shows an outdated version | Refresh the published URL; check the latest Actions run and `site/index.html` were pushed. |
| Doors don't open on an iPhone | Use the hosted GitHub Pages URL in Safari/Chrome, not an HTML preview inside a messaging app. |
| Video asks for sign-in or doesn't load | Try the **backup** link if shown, or update `data/videos.json` and regenerate the QR images. |
| Want the all-unlocked version online | Replace `site/index.html` with the appropriate `variants/*-all-unlocked.html`, commit, and redeploy (remember to switch back). |

---

Created for **jingle-lolz**, the 2026 internet nostalgia Advent calendar. Enjoy one ridiculous masterpiece a day.

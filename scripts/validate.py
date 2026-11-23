#!/usr/bin/env python3
"""Dependency-free checks for the published calendar and all variants."""
from pathlib import Path
import base64
import json
import re
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / "site/index.html",
    ROOT / "variants/mobile-daily.html",
    ROOT / "variants/mobile-all-unlocked.html",
    ROOT / "variants/desktop-daily.html",
    ROOT / "variants/desktop-all-unlocked.html",
]


def parse_embedded_videos(path):
    text = path.read_text(encoding="utf-8")
    marker = "const VIDEOS = "
    assert text.count(marker) == 1, f"{path}: expected one video array"
    start = text.index(marker) + len(marker)
    videos, _ = json.JSONDecoder().raw_decode(text[start:])
    return text, videos


def validate_url(url):
    u = urlparse(url)
    assert u.scheme == "https", f"Expected HTTPS URL: {url}"
    assert u.netloc in {"www.youtube.com", "youtube.com", "youtu.be", "vimeo.com", "www.vimeo.com"}, f"Unexpected host: {url}"


def main():
    data = json.loads((ROOT / "data/videos.json").read_text(encoding="utf-8"))
    assert len(data) == 25, f"Expected 25 entries, found {len(data)}"
    assert [v["day"] for v in data] == list(range(1, 26)), "Day sequence must be 1..25"
    assert len({v["url"] for v in data}) == 25, "Primary video URLs should be unique"
    for video in data:
        assert video["date"] == f'2026-12-{video["day"]:02}', "Date mismatch"
        assert video["title"].strip(), "Video title missing"
        validate_url(video["url"])
        if video.get("backupUrl"):
            validate_url(video["backupUrl"])

    for path in FILES:
        text, videos = parse_embedded_videos(path)
        assert len(videos) == 25, f"{path}: expected 25 embedded videos"
        assert "jingle-lolz" in text, f"{path}: site title missing"
        for expected, video in zip(data, videos):
            assert video["day"] == expected["day"], f"{path}: day mismatch"
            assert video["url"] == expected["url"], f"{path}: day {expected['day']} video mismatch"
            assert video.get("backupUrl") == expected.get("backupUrl"), f"{path}: day {expected['day']} backup mismatch"
            qr = video["qr"]
            assert qr.startswith("data:image/png;base64,"), f"{path}: day {video['day']} QR missing"
            raw = base64.b64decode(qr.split(",", 1)[1], validate=True)
            assert raw.startswith(b"\x89PNG\r\n\x1a\n"), f"{path}: day {video['day']} invalid QR PNG"
        if "daily" in path.name or path.name == "index.html":
            assert "America/New_York" in text, f"{path}: Eastern unlock logic missing"
            assert "20261201" in text and "20261225" in text, f"{path}: 2026 unlock boundaries missing"
        if "all-unlocked" in path.name:
            assert "All Doors Unlocked" in text, f"{path}: preview title missing"
        print(f"PASS {path.relative_to(ROOT)}: 25 entries and QR images verified")

    assert (ROOT / 'site/index.html').read_bytes() == (ROOT / 'variants/mobile-daily.html').read_bytes(), "site/index.html and mobile-daily variant differ"
    assert (ROOT / '.github/workflows/deploy-pages.yml').exists(), "Missing deployment workflow"
    print("PASS Published site is the daily-unlock mobile-first version")
    print("PASS Video data matches all four variants")
    print("All checks passed (does not validate third-party video playback).")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, ValueError, KeyError) as exc:
        print(f"VALIDATION FAILED: {exc}", file=sys.stderr)
        sys.exit(1)

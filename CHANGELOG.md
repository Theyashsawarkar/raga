# Changelog

Newest first. Releases are tags (`vX.Y.Z`).

## v0.1.1 -- 2026-10-21

- Documentation for open source: a logo and banner, a full README (features,
  install, usage, configuration, troubleshooting, the whole Vyom family),
  CONTRIBUTING, SECURITY and CODE_OF_CONDUCT, issue and pull request
  templates, and CI (compiles, checks plugin.toml and that every key is
  documented).

## v0.1.0 -- 2026-10-19

- First release, as its own repository: youTube music and video. Replaces music-search.py in Vayu.
- **Search as you type** (yt-dlp, no Invidious), with thumbnails, durations, channels and views.
- Music goes **into MPD's queue through rmpc and plays at once**; video opens in **mpv**, capped at 1080p.
- `Shift+Enter` plays the other way; `Ctrl+Enter` only queues the music.
- Which queue entry plays is read from the queue itself, before and after adding: `rmpc addyt` exits 0 even when its download failed.

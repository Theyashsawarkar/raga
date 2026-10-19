# raga

**raga** (राग, "melody") — YouTube music and video. A tool for [Vyom](https://github.com/Theyashsawarkar/vyom), the keyboard-driven panels of [Vayu](https://github.com/Theyashsawarkar/vayu); in Vayu it replaces music-search.py.

> Search YouTube and play: music straight into MPD's queue (rmpc), or a video in mpv. Thumbnails, durations, channels.

## Features

- **Search as you type** (yt-dlp, no Invidious), with thumbnails, durations, channels and views.
- Music goes **into MPD's queue through rmpc and plays at once**; video opens in **mpv**, capped at 1080p.
- `Shift+Enter` plays the other way; `Ctrl+Enter` only queues the music.
- Which queue entry plays is read from the queue itself, before and after adding: `rmpc addyt` exits 0 even when its download failed.

## Keys

| Key | Action |
|---|---|
| `Enter` | Play the selected result (music: in MPD via rmpc; video: in mpv) |
| `Shift+Enter` | Play it the other way (as video / as music) |
| `Ctrl+Enter` | Add the music to the queue without playing it |
| `Ctrl+M` | Switch between music and video |
| `Esc` | close |

Every Vyom panel also has: `Up`/`Down` (or `Ctrl+K`/`Ctrl+J`) to move, `Page Up`/`Page Down`, `Tab` to switch to the next tool.

## Requirements

- [Vyom](https://github.com/Theyashsawarkar/vyom) 0.2 or newer (Python 3.11+, GTK 4, gtk4-layer-shell, a layer-shell compositor)
- `yt-dlp`
- optional: rmpc + MPD (music)
- optional: mpv (video)

## Install

```sh
git clone https://github.com/Theyashsawarkar/raga ~/.local/share/vyom/plugins/raga
vyom reload        # or log out and in
vyom raga         # open it (again: close it)
```

Bind it to a key, e.g. in sway:

```
bindsym $mod+<key> exec vyom raga
```

Update: `git -C ~/.local/share/vyom/plugins/raga pull && vyom reload`. `vyom list` shows every installed tool and why one would be skipped.

## Configuration

In `~/.config/vyom/config.toml` (all optional):

```toml
[plugin.raga]
# mode: music or video to start in (default: music)
# player_command: opened after music starts (e.g. your rmpc launcher) (default: )
```

## License

MIT.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/banner-light.svg">
    <img alt="raga" src="assets/banner-dark.svg" width="560">
  </picture>
</p>

<p align="center">
  <b>Search YouTube and play: music straight into MPD's queue (rmpc), or a video in mpv. Thumbnails, durations, channels.</b><br>
  YouTube music and video. A tool for <a href="https://github.com/Theyashsawarkar/vyom">Vyom</a>, keyboard-driven panels for Wayland.
</p>

<p align="center">
  <a href="https://github.com/Theyashsawarkar/raga/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/Theyashsawarkar/raga/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://github.com/Theyashsawarkar/raga/releases"><img alt="Release" src="https://img.shields.io/github/v/release/Theyashsawarkar/raga?color=cba6f7&label=release"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-f5e0dc"></a>
  <a href="https://github.com/Theyashsawarkar/vyom"><img alt="Vyom 0.3+" src="https://img.shields.io/badge/vyom-0.3%2B-89b4fa"></a>
  <img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-a6e3a1">
  <img alt="Wayland" src="https://img.shields.io/badge/wayland-layer--shell-94e2d5">
</p>

<!-- No screenshot: music & video shows personal data (your own data). -->

> *Raga* (राग) is Sanskrit for "melody": the melody you were looking for.

raga is youTube music and video for [Vyom](https://github.com/Theyashsawarkar/vyom): one keyboard-driven panel that opens instantly, with live data, a preview and a key for everything. It runs on any compositor with the layer-shell protocol (sway, Hyprland, river, niri, Wayfire, labwc…). In [Vayu](https://github.com/Theyashsawarkar/vayu), the desktop it was built for, it replaces music-search.py.

## Contents

- [Features](#features)
- [Install](#install)
- [Usage](#usage)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [The Vyom family](#the-vyom-family)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Search as you type** (yt-dlp, no Invidious), with thumbnails, durations, channels and views.
- Music **plays in [nāda](https://github.com/Theyashsawarkar/nada)** (the music player: it lines up what comes next, shows the lyrics, `D` downloads it), or without nāda goes into MPD's queue through rmpc; video opens in **mpv**, capped at 1080p.
- `Shift+Enter` plays the other way; `Ctrl+Enter` only queues the music.
- With rmpc, which queue entry plays is read from the queue itself, before and after adding: `rmpc addyt` exits 0 even when its download failed.
- Keyboard first: every action has a key, shown in the footer; the mouse works too.
- Never freezes the panel: slow commands run in the background.

## Install

### Requirements

- [Vyom](https://github.com/Theyashsawarkar/vyom) 0.3 or newer (Python 3.11+, PyGObject, GTK 4, [gtk4-layer-shell](https://github.com/wmww/gtk4-layer-shell), a Nerd Font)
- `yt-dlp`
- optional: nāda, or rmpc + MPD (music)
- optional: mpv (video)

### Install

```sh
git clone https://github.com/Theyashsawarkar/raga ~/.local/share/vyom/plugins/raga
vyom reload           # pick it up (or log out and in)
vyom raga            # open it; run it again to close
```

Give it a key in your compositor, e.g. sway:

```sh
bindsym $mod+<key> exec vyom raga
```

### Update and uninstall

```sh
git -C ~/.local/share/vyom/plugins/raga pull && vyom reload     # update
rm -rf ~/.local/share/vyom/plugins/raga && vyom reload          # uninstall
```

## Usage

Open it with `vyom raga` (or your key). Type to search; the footer always shows the keys for what's selected.

| Key | Action |
|---|---|
| `Enter` | Play the selected result (music: in nāda, or MPD via rmpc; video: in mpv) |
| `Shift+Enter` | Play it the other way (as video / as music) |
| `Ctrl+Enter` | Add the music to the queue without playing it |
| `Esc` | Close the panel |

Every Vyom panel also has `Up`/`Down` (or `Ctrl+K`/`Ctrl+J`) to move, `Page Up`/`Page Down` to jump, `Tab`/`Shift+Tab` to switch to the next/previous tool, and `Ctrl+Tab`/`Ctrl+Shift+Tab` (or `Ctrl+H`/`Ctrl+L`) to switch tabs, or `Ctrl` with the number shown on a tab.

## Configuration

Everything is optional, in `~/.config/vyom/config.toml` under `[plugin.raga]`:

| Setting | Default | What it does |
|---|---|---|
| `mode` | music | Music or video to start in |
| `nada_command` | nada | The music player music goes to (empty: use rmpc) |
| `player_command` | (none) | With rmpc: opened after music starts (e.g. your rmpc launcher) |

Run `vyom reload` after editing.

## Troubleshooting

- **Nothing opens.** `vyom list` shows every installed tool, and why one is skipped (a missing requirement, or a Vyom that's too old).
- **It opened, then something failed.** Look for a `Traceback` in the daemon's log, `journalctl --user -u vyom -u vyom-daemon -b` (without systemd: `~/.local/state/vyom/daemon.log`), and [open an issue](https://github.com/Theyashsawarkar/raga/issues/new/choose) with it.
- **No blur or rounded corners.** That's the compositor: on SwayFX, add `layer_effects "vyom" { blur enable; corner_radius 20; shadows enable }`.

## The Vyom family

Each tool is its own repository, so you install only the ones you want:

| Tool | | What it does |
|---|---|---|
| [dvara](https://github.com/Theyashsawarkar/dvara) | द्वार, gateway | The app launcher |
| [ganit](https://github.com/Theyashsawarkar/ganit) | गणित, mathematics | The calculator and converter |
| [smriti](https://github.com/Theyashsawarkar/smriti) | स्मृति, memory | Clipboard history |
| [bhava](https://github.com/Theyashsawarkar/bhava) | भाव, feeling, emotion | The emoji picker |
| [tarang](https://github.com/Theyashsawarkar/tarang) | तरंग, wave | Wi‑Fi and the hotspot |
| [setu](https://github.com/Theyashsawarkar/setu) | सेतु, bridge | Bluetooth |
| [doot](https://github.com/Theyashsawarkar/doot) | दूत, messenger | Your phone, through KDE Connect |
| [patra](https://github.com/Theyashsawarkar/patra) | पात्र, vessel | Docker containers |
| [suchana](https://github.com/Theyashsawarkar/suchana) | सूचना, notice | Notifications |
| [raga](https://github.com/Theyashsawarkar/raga) (this one) | राग, melody | YouTube music and video |
| [mudra](https://github.com/Theyashsawarkar/mudra) | मुद्रा, gesture | Keybinding search |
| [urja](https://github.com/Theyashsawarkar/urja) | ऊर्जा, energy | The battery at a glance |
| [vishram](https://github.com/Theyashsawarkar/vishram) | विश्राम, rest | The power menu |
| [kendra](https://github.com/Theyashsawarkar/kendra) | केन्द्र, centre | Quick settings |

## Contributing

Bug reports, ideas and pull requests are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md) for the development setup and the few rules every tool follows, and [CHANGELOG.md](CHANGELOG.md) for what changed in each release. Please report security issues privately ([SECURITY.md](SECURITY.md)).

## License

[MIT](LICENSE).

"""raga (राग, "melody"): YouTube music and video for Vyom.

Search as you type (yt-dlp, no Invidious), with thumbnails, durations
and channels. Music plays in nāda (the music player: it streams the song,
lines up what comes next, shows the lyrics, and can download it) or,
without nāda, goes into MPD's queue through rmpc. A video opens in mpv
(capped at 1080p). With rmpc, which entry plays is taken from the queue
itself, before and after adding: `rmpc addyt` exits 0 even when its
download failed.
"""
import concurrent.futures
import json
import logging
import os
import urllib.request

from vyom import Hint, Row, Section, ui, util
from vyom import Plugin as Base

from . import vim

# KEYBINDS (generated from raga/vim.py by scripts/keybinds.py; don't edit by hand)
# keybind: Vyom/raga:insert | Enter | Play the selected result (music: in nāda, or MPD via rmpc; video: in mpv)
# keybind: Vyom/raga:insert | Shift+Enter | Play it the other way (as video / as music)
# keybind: Vyom/raga:insert | Ctrl+Enter | Add the music to the queue without playing it (on either tab)
# keybind: Vyom/raga:normal | Enter | Play the selected result (music: in nāda, or MPD via rmpc; video: in mpv)
# keybind: Vyom/raga:normal | o | Play it the other way (as video / as music)
# keybind: Vyom/raga:normal | y y | Copy the selected result's YouTube link
# keybind: Vyom/raga leader:normal | Space t m / Space t v | Switch to Music / Video
# keybind: Vyom/raga leader:normal | Space a q | Add the music to the queue without playing it
# keybind: Vyom/raga leader:normal | Space o b | Open the selected result on YouTube in the browser
# keybind: Vyom/raga leader:normal | Space y y | Copy the selected result's YouTube link
# keybind: Vyom/raga leader:normal | Space y t | Copy the selected result's title
# keybind: Vyom/raga leader:normal | Space r | Search YouTube again (skips what's remembered for this search)
# END KEYBINDS

VIDEO_FORMAT = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
os.environ.setdefault("MPD_HOST", os.path.join(os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}"),
                                               "mpd/socket"))
THUMBS = os.path.join(util.CACHE, "raga")

log = logging.getLogger("vyom.raga")


def duration(s):
    if not s:
        return "live"
    s = int(s)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


def views(n):
    if not n:
        return ""
    for div, suf in ((1e9, "B"), (1e6, "M"), (1e3, "K")):
        if n >= div:
            return f"{n / div:.1f}{suf} views".replace(".0", "")
    return f"{n} views"


def thumb(vid):
    """YouTube's hqdefault.jpg: a fixed, unsigned URL (480x360)."""
    path = os.path.join(THUMBS, f"{vid}.jpg")
    if os.path.exists(path):
        return path
    try:
        with urllib.request.urlopen(f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg", timeout=5) as r:
            data = r.read()
        os.makedirs(THUMBS, exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)
        return path
    except Exception as e:   # offline, or no thumbnail: the row just has none
        log.debug("thumbnail for %s: %s", vid, e)
        return None


class Plugin(Base):
    name, title, icon, color = "raga", "Music & video", "\U000f075a", "pink"
    placeholder = "Search YouTube…"
    preview = True
    preview_width = 320
    debounce = 700           # yt-dlp takes ~2 s: search when typing pauses
    keep_query = True
    hints = [Hint("Enter", "play"), Hint("o", "other way"), Hint("Space a q", "queue"), Hint("y y", "copy link")]
    insert_hints = [Hint("Enter", "play"), Hint("Shift+Enter", "other way"), Hint("Ctrl+Enter", "queue"),
                    Hint("Esc", "normal mode")]
    modal = True             # Vyom's vim keys (ADR 0008); raga/vim.py
    start_mode = "insert"    # search-first
    key_groups = vim.GROUPS
    empty_text = "Type to search YouTube"
    tabs = [("music", "Music"), ("video", "Video")]   # H / L, Space t m / t v (Vyom)

    def __init__(self, vyom, conf):
        super().__init__(vyom, conf)
        self.tab = self.conf.get("mode", "music")
        self.cache = {}

    def opened(self, args):
        super().opened(args)
        if args and args[0] in ("music", "video"):
            self.select_tab(args[0])

    def search(self, q):
        q = q.strip()
        if len(q) < 2:
            return []
        if q not in self.cache:
            code, out = util.run(["yt-dlp", f"ytsearch12:{q}", "--flat-playlist", "--dump-json", "--no-warnings"],
                                 timeout=25)
            res = []
            for line in out.splitlines():
                try:
                    res.append(json.loads(line))
                except ValueError:
                    pass
            with concurrent.futures.ThreadPoolExecutor(8) as ex:
                for d, path in zip(res, ex.map(lambda d: thumb(d.get("id", "")), res), strict=False):
                    d["_thumb"] = path
            self.cache[q] = res
            if len(self.cache) > 30:
                self.cache.pop(next(iter(self.cache)))
        res = self.cache[q]
        if not res:
            return [Row("Nothing found", "or yt-dlp couldn't reach YouTube", icon="\U000f075a", color="gray",
                        data=None)]
        rows = [Section("Play as music (MPD)" if self.tab == "music" else "Play as video (mpv)")]
        for d in res:
            rows.append(Row(d.get("title") or "?", " · ".join(x for x in (d.get("channel") or d.get("uploader"),
                                                                            views(d.get("view_count"))) if x),
                            icon=d.get("_thumb") or "\U000f075a", color="pink", meta=duration(d.get("duration")),
                            data=d))
        return rows

    def build_preview(self, row):
        d = row.data
        if not d:
            return None
        parts = []
        if d.get("_thumb"):
            parts.append(ui.picture(d["_thumb"], 170))
        parts += [ui.title(d.get("title") or "?"), ui.meta(d.get("channel") or d.get("uploader") or ""),
                  ui.kv([("Length", duration(d.get("duration"))), ("Views", views(d.get("view_count")) or "-")]),
                  ui.buttons([("Play music", lambda: self.play(d, "music"), "primary" if self.tab == "music" else ""),
                              ("Watch video", lambda: self.play(d, "video"), "primary" if self.tab == "video" else "")])]
        return ui.vbox(*parts, spacing=10)

    # ------------------------------------------------------------ playing
    def play(self, d, mode, queue_only=False):
        vid, title = d.get("id"), (d.get("title") or "?").replace("\n", " ")
        url = f"https://youtube.com/watch?v={vid}"
        self.close()
        if mode == "video":
            util.notify("YouTube video", f"Playing: {title}", icon="video-x-generic", app="raga")
            util.spawn(["mpv", "--no-terminal", "--force-window=yes", f"--ytdl-format={VIDEO_FORMAT}", url])
            return
        if not util.have(self.conf.get("nada_command", "nada")):   # nāda says what it plays itself
            util.notify("YouTube music", f"{'Queueing' if queue_only else 'Adding'}: {title}", icon="audio-x-generic",
                        app="raga")
        import threading
        threading.Thread(target=self.play_music, args=(url, title, queue_only), daemon=True).start()

    def queue_files(self):
        code, out = util.run(["rmpc", "queue"], timeout=10)
        try:
            return {e["file"]: e.get("metadata", {}).get("pos") for e in json.loads(out)} if code == 0 else {}
        except (ValueError, KeyError, TypeError):
            return {}

    def play_music(self, url, title, queue_only):
        nada = self.conf.get("nada_command", "nada")
        if nada and util.have(nada):
            # nāda resolves the stream, plays it and lines up what comes next
            code, out, err = util.run_full([nada, "add", "--next" if queue_only else "--play", url], timeout=30)
            if code != 0:
                util.notify("YouTube music failed", (err.strip().splitlines() or ["nāda didn't answer"])[-1][:200],
                            urgency="critical", app="raga")
            return
        if not util.have("rmpc"):
            util.notify("YouTube music", "needs nāda (the music player) or rmpc to play music", urgency="critical",
                        app="raga")
            return
        before = self.queue_files()
        code, out, err = util.run_full(["rmpc", "addyt", "--position", "0", url], timeout=90)
        after = self.queue_files()
        new = [f for f in after if f not in before]
        if len(new) != 1:   # addyt's exit code lies: trust the queue
            msg = (err.strip().splitlines() or ["the download failed"])[-1]
            util.notify("YouTube music failed", msg[:200], urgency="critical", app="raga")
            return
        if not queue_only:
            util.run(["rmpc", "play", str(after[new[0]])], timeout=10)
            opener = self.conf.get("player_command")
            if opener:
                util.spawn(opener)
        util.notify("YouTube music", f"{'Queued' if queue_only else 'Playing'}: {title}", app="raga")

    def activate(self, row, mods):
        if not row.data:
            return False
        if "ctrl" in mods:          # the queue is music's, on either tab
            self.play(row.data, "music", queue_only=True)
            return False
        mode = self.tab
        if "shift" in mods:
            mode = "video" if mode == "music" else "music"
        self.play(row.data, mode)
        return False

    # ================================================================ keys
    # The modes, counts and sequences are Vyom's; raga/vim.py is its keys.
    def keys(self, tab):
        return vim.keys(tab)

    def chosen(self):
        row = self.panel.selected_row() if self.panel else None
        return row.data if row is not None and row.data else None

    def waits(self, action, n):
        """Typed before the results arrived (a search, Esc, o): it runs on
        what they select, not on the row that was there a moment ago."""
        modal = self.panel.modal if self.panel else None
        if modal is not None and self.panel.searching:
            modal.deferred.append((vim.B("<CR>", action), n))
            return True
        return False

    def v_other(self, n, _a):
        if self.waits("other", n):
            return
        row = self.panel.selected_row()
        if row is not None and row.data:
            self.activate(row, {"shift"})

    def v_queue(self, n, _a):
        if self.waits("queue", n):
            return
        row = self.panel.selected_row()
        if row is not None and row.data:
            self.activate(row, {"ctrl"})

    def v_copy(self, _n, arg):
        d = self.chosen()
        if d is None:
            return
        text = (d.get("title") or "?") if arg == "title" else f"https://youtube.com/watch?v={d.get('id')}"
        util.copy(text)
        self.set_status(f"copied {text}", kind="ok")

    def v_browser(self, _n, _a):
        d = self.chosen()
        if d is not None:
            util.spawn(["xdg-open", f"https://youtube.com/watch?v={d.get('id')}"])
            self.close()

    def v_research(self, _n, _a):
        q = self.panel.query().strip() if self.panel else ""
        self.cache.pop(q, None)
        self.refresh()
        self.set_status("searching again…")


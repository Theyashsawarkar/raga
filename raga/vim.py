"""raga's vim keys, as data. The modes, counts, sequences, which-key strip,
help (?) and palette (Space Space) are Vyom's (vyom/keys.py, vyom/modal.py;
Vyom ADR 0008); this file is only what raga adds. Space groups follow
Vayu's shared letters: t tabs (Vyom's: Space t m / t v), a add, y copy,
o open outside, r refresh.

An action "verb:arg" runs Plugin.v_<verb>(count, arg) in raga/__init__.py,
or Vyom's own (activate, insert, moved...).
"""
from vyom.keys import Bind

B = Bind

GROUPS = {}

INSERT = [
    ("Enter", "Play the selected result (music: in nāda, or MPD via rmpc; video: in mpv)"),
    ("Shift+Enter", "Play it the other way (as video / as music)"),
    ("Ctrl+Enter", "Add the music to the queue without playing it (on either tab)"),
]

NORMAL = [
    B("<CR>", "activate", "Play the selected result (music: in nāda, or MPD via rmpc; video: in mpv)"),
    B("o", "other", "Play it the other way (as video / as music)"),
    B("<S-CR>", "other", "", hidden=True),
    B("<C-CR>", "queue", "", hidden=True),
    B("yy", "copy:url", "Copy the selected result's YouTube link"),
]

LEADER = [
    B(" aq", "queue", "Add the music to the queue without playing it"),
    B(" ob", "browser", "Open the selected result on YouTube in the browser"),
    B(" yy", "copy:url", "Copy the selected result's YouTube link"),
    B(" yt", "copy:title", "Copy the selected result's title"),
    B(" r", "research", "Search YouTube again (skips what's remembered for this search)"),
]


def keys(tab):
    return NORMAL + LEADER


SECTIONS = [
    ("raga", "insert", "Insert mode (typing; raga opens in it)", INSERT),
    ("raga", "normal", "Normal mode", NORMAL),
    ("raga leader", "normal", "Leader (Space)", [("Space t m / Space t v", "Switch to Music / Video")] + LEADER),
]

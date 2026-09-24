"""A leaderboard in the terminal: entries on top, sorted high to low, an input line at the bottom.

    Board(score, log="log.txt").run()          score(text) -> float

Type a caption, optionally followed by "# GROUP", e.g. "a dog # 14". A group's
new entry replaces its old one; entries without a group show as "--" and each
one stays. Each row reads  GID | SCORE | CAPTION  with a bar behind the caption
proportional to its score, and the group that entered last is shown knocked out.
Focus moves with Up and Down through the rows and on to the input line below
them; Tab jumps between the input line and the row picked last, the top row
if none. On a picked row, Backspace or Delete removes it and Escape returns to
the input line. Ctrl-C or Ctrl-D leaves. A caption longer than the line wraps;
a caption another group already entered, ignoring case, spacing and
punctuation, turns the line red and is not accepted. Every accepted entry is
appended to the log file, if one is given, as time, group, score and caption.
"""
import curses
import datetime
import re

LAST, PICK, BAR_A, BAR_B, BAR_LAST, DIM, RULE, WARN = 1, 2, 3, 4, 5, 6, 7, 8
PREFIX = "| 0.0000 |"  # the fixed middle of a row


def parse(line):
    text, sep, gid = line.rpartition("#")
    if not sep:
        text, gid = line, ""
    return text.strip(), gid.strip() or "--"


def fit(text, width):
    return text if len(text) <= width else text[: max(width - 3, 0)] + "..."


def canon(text):
    """The caption as the duplicate check sees it: lower case, letters and digits, single spaces."""
    return " ".join(re.sub(r"[^\w\s]", " ", text.lower()).split())


class Board:
    def __init__(self, score, title="", log=None):
        self.score, self.title, self.log = score, title, log
        self.entries = {}  # key -> (gid, text, score); a "--" entry gets a key of its own
        self.last = None
        self.picked = None  # key of the row the arrow keys or Tab chose last
        self.on_input = True  # focus: the input line, or the picked row
        self.count = 0

    def duplicate(self, line):
        """The group that already entered this caption, or None."""
        text, gid = parse(line)
        c = canon(text)
        if not c:
            return None
        for key, (g, t, _) in self.entries.items():
            if key != gid and canon(t) == c:
                return g
        return None

    def enter(self, line):
        """Add the line's caption; False if it is empty or another group already has it."""
        text, gid = parse(line)
        if not text or self.duplicate(line) is not None:
            return False
        self.count += 1
        key = gid if gid != "--" else f"--{self.count}"
        self.entries[key] = (gid, text, self.score(text))
        self.last = key
        if self.log:
            with open(self.log, "a") as f:
                f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}\t{gid}\t{self.entries[key][2]:.4f}\t{text}\n")
        return True

    def index(self):
        """The picked row's position, or None."""
        keys = [k for k, *_ in self.rows()]
        return keys.index(self.picked) if self.picked in keys else None

    def move(self, step):
        rows = self.rows()
        if not rows:
            return
        if self.on_input:
            if step < 0:
                self.on_input, self.picked = False, rows[-1][0]
            return
        i = (self.index() if self.index() is not None else 0) + step
        if i >= len(rows):
            self.on_input = True
        else:
            self.picked = rows[max(i, 0)][0]

    def tab(self):
        rows = self.rows()
        if self.on_input and rows:
            self.on_input = False
            if self.index() is None:
                self.picked = rows[0][0]
        else:
            self.on_input = True

    def remove(self):
        i = self.index()
        if self.on_input or i is None:
            return
        if self.last == self.picked:
            self.last = None
        del self.entries[self.picked]
        rows = self.rows()
        if rows:
            self.picked = rows[min(i, len(rows) - 1)][0]
        else:
            self.picked, self.on_input = None, True

    def rows(self):
        """(key, gid, text, score), highest score first."""
        return sorted(((k, *v) for k, v in self.entries.items()), key=lambda r: -r[3])

    def run(self):
        curses.wrapper(self._loop)

    def _loop(self, screen):
        curses.use_default_colors()
        curses.set_escdelay(25)
        # 256-colour palette: bars alternate deep blue and slate under white text,
        # the newest entry's bar is a bright blue; its id is black on cyan, the
        # picked row's id black on amber; the score column and rules are grey
        curses.init_pair(LAST, 16, 51)
        curses.init_pair(PICK, 16, 214)
        curses.init_pair(BAR_A, 231, 24)
        curses.init_pair(BAR_B, 231, 60)
        curses.init_pair(BAR_LAST, 231, 33)
        curses.init_pair(DIM, 245, -1)
        curses.init_pair(RULE, 240, -1)
        curses.init_pair(WARN, 203, -1)
        buffer = ""
        while True:
            self._draw(screen, buffer)
            key = screen.get_wch()
            if key in ("\x03", "\x04"):  # ctrl-c, ctrl-d
                return
            if key == curses.KEY_UP:
                self.move(-1)
            elif key == curses.KEY_DOWN:
                self.move(1)
            elif key == "\t":
                self.tab()
            elif key == "\x1b":
                self.on_input = True
            elif key == curses.KEY_RESIZE:
                continue
            elif not self.on_input:
                if key in ("\x7f", "\b", curses.KEY_BACKSPACE, curses.KEY_DC):
                    self.remove()
                elif key in ("\n", "\r", curses.KEY_ENTER):
                    self.on_input = True
                elif isinstance(key, str) and key.isprintable():  # typing returns to the line
                    self.on_input = True
                    buffer += key
            elif key in ("\n", "\r", curses.KEY_ENTER):
                if self.enter(buffer):
                    buffer = ""
            elif key in ("\x7f", "\b", curses.KEY_BACKSPACE):
                buffer = buffer[:-1]
            elif isinstance(key, str) and key.isprintable():
                buffer += key

    def _draw(self, screen, buffer):
        screen.erase()
        lines, cols = screen.getmaxyx()
        rows = self.rows()
        gid_w = max([3] + [len(g) for _, g, _, _ in rows])
        x = gid_w + 1 + len(PREFIX)          # where the bar starts: the space before the caption
        bar_w = max(cols - x - 1, 9)
        top = max((s for _, _, _, s in rows), default=0) or 1
        screen.addnstr(0, 0, self.title, cols - 1, curses.color_pair(DIM))
        # the input line wraps at the terminal edge; the box grows by whole lines
        prompt = "> "
        width = max(cols - 1, 4)
        typed = prompt + buffer
        chunks = [typed[i:i + width] for i in range(0, len(typed), width)] or [""]
        box = len(chunks)
        dup = self.duplicate(buffer) if self.on_input else None
        for i, (key, gid, text, score) in enumerate(rows[: max(lines - 4 - box, 0)]):
            y, last, picked = i + 1, key == self.last, not self.on_input and key == self.picked
            mark = curses.color_pair(PICK) | curses.A_BOLD if picked else curses.color_pair(LAST) | curses.A_BOLD if last else 0
            screen.addstr(y, 0, f"{gid:>{gid_w}} ", mark)
            screen.addstr(y, gid_w + 1, f"| {score:.4f} |", curses.color_pair(DIM))
            shown = " " + fit(text, bar_w - 1).ljust(bar_w - 1)
            bar = round(score / top * bar_w)
            tone = BAR_LAST if last else (BAR_A, BAR_B)[i % 2]
            screen.addstr(y, x, shown[:bar], curses.color_pair(tone) | (curses.A_BOLD if picked else 0))
            screen.addstr(y, x + bar, shown[bar:], curses.A_BOLD if picked else 0)
        # the input box: a rule above, the wrapped line, a rule below that
        # carries the warning when the caption is a duplicate
        top_y, bottom_y = lines - 2 - box, lines - 1
        screen.addstr(top_y, 0, "─" * (cols - 1), curses.color_pair(RULE))
        screen.addstr(bottom_y, 0, "─" * (cols - 1), curses.color_pair(RULE))
        if dup is not None:
            who = "an earlier entry" if dup == "--" else f"group {dup}'s caption"
            screen.addnstr(bottom_y, 2, f" duplicate of {who} ", cols - 3, curses.color_pair(WARN) | curses.A_BOLD)
        tone = curses.color_pair(WARN) if dup is not None else 0 if self.on_input else curses.color_pair(DIM)
        for j, chunk in enumerate(chunks):
            screen.addnstr(top_y + 1 + j, 0, chunk, cols - 1, tone)
        screen.move(top_y + box, min(len(chunks[-1]), cols - 1))
        try:
            curses.curs_set(1 if self.on_input else 0)
        except curses.error:
            pass
        screen.refresh()

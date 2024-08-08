from stopwatch import Stopwatch
import datetime
import pathlib
from collections.abc import Callable

POM_ARCHIVE_DIR: str = "~/Documents/pomodoro_archive"
POM_FILENAME: str = "~/Documents/pomodoro.txt"
POM_ARCHIVE_MASK: str = POM_ARCHIVE_DIR + "/pomodoro_daily_{}{}{}.txt"

def create_pomodoro_archive_filename(dt: datetime.datetime) -> str:
    return POM_ARCHIVE_MASK.format(dt.year, dt.month, dt.day)


# ---- Manager -------------------------------------------------------------------------------------

class Manager():
    def __init__(self, filename: str | None = None) -> None:
        self.watches: dict[str, Stopwatch] = {}
        self.last_active: str = ""
        self.running = True

        pomodoro_archive_dir = pathlib.Path(POM_ARCHIVE_DIR).expanduser()
        if not pomodoro_archive_dir.is_dir():
            pomodoro_archive_dir.mkdir()

        if filename is None:
            self.savepath = pathlib.Path(POM_FILENAME).expanduser()
        else:
            self.savepath = pathlib.Path(filename).expanduser()

        now = datetime.datetime.now()
        self.daily = pathlib.Path(create_pomodoro_archive_filename(now)).expanduser()
        self.commands: dict[str, Callable[[list[str], Manager], None]] = {}
        self.shorts: dict[str, str] = {}

        if self.savepath.exists():
            with open(self.savepath, "r") as savefile:
                for line in savefile:
                    w = Stopwatch.deserialise(line)
                    self.watches[w.name] = w

    def add_command(self, keyword: str, command: Callable[[list[str], "Manager"], None]):
        self.commands[keyword] = command

    def get_categories(self) -> list[str]:
        cats = []
        for w in self.watches.values():
            if w.category not in cats:
                cats.append(w.category)

        return cats

    def sum_by_categories(self) -> dict[str, datetime.timedelta]:
        cats:dict[str, datetime.timedelta] = {}

        for w in self.watches.values():
            if w.category not in cats:
                cats[w.category] = w.get_elapsed()
            else:
                cats[w.category] = cats[w.category] + w.get_elapsed()

        return cats

    def add_shortcut(self, shortcut: str, keyword: str):
        self.shorts[shortcut] = keyword

    def exec(self, cmd_input: str):
        words = cmd_input.split()
        if (len(words) == 0):
            return;

        if words[0].lower() in self.shorts:
            cmd = self.commands[self.shorts[words[0]]]
            cmd(words, self)
            return
        elif words[0].lower() in self.commands:
            cmd = self.commands[words[0]]
            cmd(words, self)
        else:
            print(f"\33[31mERROR: Unknown command '{cmd_input}' \33[0m\a")


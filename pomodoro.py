from collections.abc import Callable
import pathlib
import datetime

from stopwatch import Stopwatch, format_timedelta

# ---- Manager -------------------------------------------------------------------------------------

class Manager():
    def __init__(self) -> None:
        self.watches: dict[str, Stopwatch] = {}
        self.last_active: str = ""
        self.running = True
        self.savepath = pathlib.Path("~/Documents/pomodoro.txt").expanduser()
        now = datetime.datetime.now()
        self.daily = pathlib.Path(f"~/Documents/pomodoro_daily_{now.year}{now.month}{now.day}.txt").expanduser()
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

        if words[0] in self.shorts:
            cmd = self.commands[self.shorts[words[0]]]
            cmd(words, self)
            return
        elif words[0] in self.commands:
            cmd = self.commands[words[0]]
            cmd(words, self)
        else:
            print(f"Unknown command '{cmd_input}'")

# ---- CLI commands --------------------------------------------------------------------------------

def get_watch(key: str, manager: Manager) -> Stopwatch | None:
    """Returns a watch by name or index."""
    try:
        idx = int(key)
        keys = list(manager.watches.keys())
        return manager.watches[keys[idx]]
    except:
        if key in manager.watches:
            return manager.watches[key]
        return None

def print_watches(_: list[str], manager: Manager):
    """Prints all available watches (active and inactive).
    Including status and already elapsed time.
    """

    print(f"{len(manager.watches)} watches")
    for i,w in enumerate(manager.watches.values()):
        if w.archived:
            continue
        print(f"[{i:3}] {w}")
    print(f"last active: '{manager.last_active}'")

def new_watch(words: list[str], manager: Manager):
    """Creates a new watch

    Usage: new <watch_name>
    """
    if len(words) < 2:
        print("no watch name given")
        return

    if words[1] in manager.watches:
        print("error, watch with that name already exists")
        return

    manager.watches[words[1]] = Stopwatch(words[1])
    print(f"creating new watch '{words[1]}'")
    manager.last_active = words[1]
    save(words, manager)

def start_watch(words: list[str], manager: Manager):
    """Restarts a watch with the given name.
    If the watch doesn't exist, a new one is created.

    Usage: start <watch_name>
    """
    w = get_watch(words[1], manager)

    if w is None:
        new_watch(words, manager)
        w = get_watch(words[1], manager)

    if w is not None:
        w.cont()
        return
    print("FATAL ERROR: something went wrong")

def cont_watch(words: list[str], manager: Manager):
    """Restarts a watch with the given name.

    Usage: cont <watch_name/watch_index>
    """

    if len(words) < 2:
        print("no watch name or index given")
        return

    w = get_watch(words[1], manager)
    if w is not None:
        w.cont()
        manager.last_active = words[1]
        print(f"continuing '{w.name}'")
    else:
        print("error, can't find watch with that name")
    save(words, manager)

def pause_watch(words: list[str], manager: Manager):
    """Pauses the given watch.

    Usage: pause <watch_name/watch_index>
    """

    if len(words) < 2:
        print("no watch name or index given")
        return

    w = get_watch(words[1], manager)
    if w is not None:
        w.pause()
        print(f"pausing '{w.name}', elapsed: {format_timedelta(w.get_elapsed())}")
    else:
        print("error, can't find watch with that name")
    save(words, manager)

def save(_: list[str], manager: Manager):
    """Saves the status"""
    with open(manager.savepath, 'w') as savefile:
        savefile.writelines([w.serialise() + "\n" for w in manager.watches.values()])

def quit_program(_: list[str], manager: Manager):
    """Saves the status and taken time of all watches and quits the program."""
    manager.running = False
    save(_, manager)

def print_help(_: list[str], manager: Manager):
    """Prints this help message."""
    print("")
    for c in manager.commands:
        cmd = manager.commands[c]

        alias = ""
        for short in manager.shorts:
            if manager.shorts[short] == c:
                alias = alias + ", " + short

        print(f" {c}{alias}:")
        if cmd.__doc__ is not None:
            lines = [l.strip() for l in cmd.__doc__.split('\n')]
            end = len(lines)-1
            while(lines[end] == ""):
                end = end - 1
            for line in lines[:end+1]:
                print(f"    {line}")
            print("")
        else:
            print("    <no documentation>\n")

def archive_watch(words: list[str], manager: Manager):
    """Archives (hides) a watch."""
    w = get_watch(words[1], manager)
    if w is not None:
        w.archived = True
    else:
        print("ERROR: couldn't find watch to archive")
    save(words, manager)

def print_categories(_: list[str], manager: Manager):
    """Prints total times for all categories"""

    cats = manager.sum_by_categories()

    for c in cats:
        print(f"{c:24} {format_timedelta(cats[c])}")

def daily_archive(words: list[str], manager: Manager):
    """Prints all watches and moves them to a backup file.
    This function is meant to be used to compile daily / monthly / etc. progress.
    """
    print_watches(words, manager)
    print_categories(words, manager)
    with open(manager.daily, 'w') as savefile:
        savefile.writelines([w.serialise() + "\n" for w in manager.watches.values()])
    manager.watches.clear()
    

# ---- main ----------------------------------------------------------------------------------------

def main():
    manager = Manager()

    manager.add_command("print", print_watches)
    manager.add_command("new", new_watch)
    manager.add_command("start", start_watch)
    manager.add_command("stop", pause_watch)
    manager.add_command("cont", cont_watch)
    manager.add_command("quit", quit_program)
    manager.add_command("help", print_help)
    manager.add_command("archive", archive_watch)
    manager.add_command("daily", daily_archive)
    manager.add_command("pcats", print_categories)

    manager.add_shortcut("q", "quit")
    manager.add_shortcut("p", "print")
    manager.add_shortcut("n", "new")
    manager.add_shortcut("s", "start")
    manager.add_shortcut("h", "help")
    manager.add_shortcut("a", "archive")

    while(manager.running):
        cmd = input("> ")
        manager.exec(cmd)


main()



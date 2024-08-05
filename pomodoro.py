from collections.abc import Callable
import pathlib
import datetime

from stopwatch import Stopwatch

# ---- Manager -------------------------------------------------------------------------------------

class Manager():
    def __init__(self) -> None:
        self.watches: dict[str, Stopwatch] = {}
        self.last_active: str = ""
        self.running = True
        self.savepath = pathlib.Path("~/Documents/pomodoro.txt").expanduser()
        now = datetime.datetime.now()
        self.weekly = pathlib.Path(f"~/Documents/pomodoro_weekly_{now.year}{now.month}{now.day}.txt").expanduser()
        self.commands: dict[str, Callable[[list[str], Manager], None]] = {}
        self.shorts: dict[str, str] = {}

        if self.savepath.exists():
            with open(self.savepath, "r") as savefile:
                for line in savefile:
                    w = Stopwatch.deserialise(line)
                    self.watches[w.name] = w

    def add_command(self, keyword: str, command: Callable[[list[str], "Manager"], None]):
        self.commands[keyword] = command

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
    i = 0
    for w in manager.watches.values():
        if w.archived:
            continue
        print(f"[{i:3}] {w}")
        i += 1
    print(f"last active: '{manager.last_active}'")

def start_watch(words: list[str], manager: Manager):
    """Starts a new watch with the given name.
    If a watch with that name already exists, prints a warning and does nothing.
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

def cont_watch(words: list[str], manager: Manager):
    """Resumes a taking time by the given watch."""

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

def pause_watch(words: list[str], manager: Manager):
    """Pauses the given watch."""

    if len(words) < 2:
        print("no watch name or index given")
        return

    w = get_watch(words[1], manager)
    if w is not None:
        w.pause()
        print(f"pausing '{w.name}', elapsed: {w.get_elapsed()}")
    else:
        print("error, can't find watch with that name")

def quit_program(_: list[str], manager: Manager):
    """Saves the status and taken time of all watches and quits the program."""
    manager.running = False
    with open(manager.savepath, 'w') as savefile:
        savefile.writelines([w.serialise() + "\n" for w in manager.watches.values()])

def print_help(_: list[str], manager: Manager):
    """Prints this help message."""
    print("")
    for c in manager.commands:
        cmd = manager.commands[c]

        alias = ""
        for short in manager.shorts:
            if manager.shorts[short] == c:
                alias = alias + ", " + short

        print(f" \33[1m{c}{alias}:\33[0m")
        if cmd.__doc__ is not None:
            lines = cmd.__doc__.split('\n')
            for line in lines:
                print(f"    {line.strip()}")
            print("")
        else:
            print("    <no documentation>\n")

def archive_watch(words: list[str], manager: Manager):
    """Archiving (hiding) a watch."""
    w = get_watch(words[1], manager)
    w.archived = True

def weekly_archive(words: list[str], manager: Manager):
    """Printing all watches and moving them to a backup file.
    This function is meant to be used to compile weekly / monthly / etc. progress.
    """
    print_watches(words, manager)
    with open(manager.weekly, 'w') as savefile:
        savefile.writelines([w.serialise() + "\n" for w in manager.watches.values()])
    manager.watches.clear()
    

# ---- main ----------------------------------------------------------------------------------------

def main():
    manager = Manager()

    manager.add_command("print", print_watches)
    manager.add_command("start", start_watch)
    manager.add_command("pause", pause_watch)
    manager.add_command("cont", cont_watch)
    manager.add_command("quit", quit_program)
    manager.add_command("help", print_help)
    manager.add_command("archive", archive_watch)
    manager.add_command("weekly", weekly_archive)

    manager.add_shortcut("q", "quit")
    manager.add_shortcut("p", "print")
    manager.add_shortcut("c", "cont")
    manager.add_shortcut("h", "help")
    manager.add_shortcut("a", "archive")
    manager.add_shortcut("w", "weekly")
    manager.add_shortcut("wa", "weekly")

    while(manager.running):
        cmd = input("> ")
        manager.exec(cmd)


main()



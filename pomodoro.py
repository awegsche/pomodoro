from collections.abc import Callable
from manager import Manager

from stopwatch import Stopwatch, format_timedelta
from stats import get_weekly_stats, get_weekly_cats

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
        print(f"continuing {w.name}, {format_timedelta(w.get_elapsed())}")
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
    manager.add_command("wstats", get_weekly_stats)
    manager.add_command("wcats", get_weekly_cats)

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



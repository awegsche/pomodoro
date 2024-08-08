from datetime import datetime, timedelta

from manager import Manager, create_pomodoro_archive_filename
from stopwatch import format_timedelta

WSTATS_BORDER = ""
DSTATS_BORDER = ""
TABLE_BORDER = "+-" + "-" * 24 + "-+-" + "-" * 9 + "+"

def get_weekly_cats(_: list[str], _manager: Manager):
    """Prints weekly category statistics.
    Sums elapsed times for categories for each weekday from Monday until now and the sum of
    the whole week.
    """
    now = datetime.now()

    # count back to monday
    day = now - timedelta(days = now.weekday())
    week_cats: dict[str, timedelta] = {}

    def do_for_manager(day: datetime, manager: Manager):
        cats = manager.sum_by_categories()

        print(day.strftime("%a") + f" [{len(cats)} categories]")
        print("")
        print(TABLE_BORDER)
        for c in cats:
            print(f"| {c:24} | {format_timedelta(cats[c])} |")
            if c not in week_cats:
                week_cats[c] = cats[c]
            else:
                week_cats[c] = week_cats[c] + cats[c]
        print(TABLE_BORDER)
        print(DSTATS_BORDER)
        print("")

    
    for i in range(now.weekday()+1):
        manager = Manager(filename=create_pomodoro_archive_filename(day))
        do_for_manager(day, manager)
        day = day + timedelta(days=1)


    print("")
    print(WSTATS_BORDER)
    print("WEEKLY STATS:")
    print(f"{len(week_cats)} categories")
    print(TABLE_BORDER)
    for c in week_cats:
        print(f"| {c:24} | {format_timedelta(week_cats[c])} |")
    print(TABLE_BORDER)
    print(WSTATS_BORDER)
    print("")

    if len(_manager.watches) > 0:
        print("Found unsaved watches (not included in statistics):")
        do_for_manager(now, _manager)

def get_weekly_stats(_: list[str], _manager: Manager):
    """Prints weekly statistics.
    Sums elapsed times for same name watches for each weekday from Monday until now and the sum of
    the whole week.
    """
    now = datetime.now()

    # count back to monday
    day = now - timedelta(days = now.weekday())
    week_cats: dict[str, timedelta] = {}

    print("\n")

    def do_for_manager(day: datetime, manager: Manager):
        print(day.strftime("%a") + f" [{len(manager.watches)} watches]")
        print(TABLE_BORDER)
        for w in manager.watches.values():
            print(f"| {w.name:24} | {format_timedelta(w.get_elapsed())} |")
            if w.name not in week_cats:
                week_cats[w.name] = w.get_elapsed()
            else:
                week_cats[w.name] = week_cats[w.name] + w.get_elapsed()
        print(TABLE_BORDER)
        print(DSTATS_BORDER)
        print("")
    
    for i in range(now.weekday()+1):
        manager = Manager(filename=create_pomodoro_archive_filename(day))
        do_for_manager(day, manager)

        day = day + timedelta(days=1)


    print("")
    print(WSTATS_BORDER)
    print("WEEKLY STATS:")
    print(f"{len(week_cats)} watches")
    print(TABLE_BORDER)
    for c in week_cats:
        print(f"| {c:24} | {format_timedelta(week_cats[c])} |")
    print(TABLE_BORDER)
    print(WSTATS_BORDER)
    print("")

    if len(_manager.watches) > 0:
        print("Found unsaved watches (not included in statistics):")
        do_for_manager(now, _manager)

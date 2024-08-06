from datetime import datetime, timedelta

from manager import Manager, create_pomodoro_archive_filename
from stopwatch import format_timedelta

def get_weekly_cats(_: list[str], _manager: Manager):
    """Prints weekly category statistics.
    Sums elapsed times for categories for each weekday from Monday until now and the sum of
    the whole week.
    """
    now = datetime.now()

    # count back to monday
    day = now - timedelta(days = now.weekday())
    week_cats: dict[str, timedelta] = {}
    
    for i in range(now.weekday()+1):
        manager = Manager(filename=create_pomodoro_archive_filename(day))
        cats = manager.sum_by_categories()

        print(day.strftime("%a"))
        print("===")
        print(f"{len(cats)} categories")
        for c in cats:
            print(f"{c:24} {format_timedelta(cats[c])}")
            if c not in week_cats:
                week_cats[c] = cats[c]
            else:
                week_cats[c] = week_cats[c] + cats[c]
        day = day + timedelta(days=1)
        print(" ".join("_" * 20))
        print("")


    print("weekly stats:")
    print(f"{len(week_cats)} categories")
    for c in week_cats:
        print(f"{c:24} {format_timedelta(week_cats[c])}")

def get_weekly_stats(_: list[str], _manager: Manager):
    """Prints weekly statistics.
    Sums elapsed times for same name watches for each weekday from Monday until now and the sum of
    the whole week.
    """
    now = datetime.now()

    # count back to monday
    day = now - timedelta(days = now.weekday())
    week_cats: dict[str, timedelta] = {}
    
    for i in range(now.weekday()+1):
        manager = Manager(filename=create_pomodoro_archive_filename(day))

        print(day.strftime("%a"))
        print("===")
        print(f"{len(manager.watches)} watches")
        for w in manager.watches.values():
            print(f"{w.name:24} {format_timedelta(w.get_elapsed())}")
            if w.name not in week_cats:
                week_cats[w.name] = w.get_elapsed()
            else:
                week_cats[w.name] = week_cats[w.name] + w.get_elapsed()
        day = day + timedelta(days=1)
        print(" ".join("_" * 20))
        print("")


    print("weekly stats:")
    print(f"{len(week_cats)} watches")
    for c in week_cats:
        print(f"{c:24} {format_timedelta(week_cats[c])}")

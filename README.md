# pomodoro

## Introduction

Keeps track of your activities using different stopwatches.
Saves start times and total elapsed times in `~/Documents/pomodoro.txt`
and doesn't need to permanently run to record times.

## Usage

Start the program with
```shell
python pomodoro.py
```

Then, you can use the following commands to create, start, stop and resume stopwatches:
```

 print, p:
    Prints all available watches (active and inactive).
    Including status and already elapsed time.

 new, n:
    Creates a new watch

    Usage: new <watch_name>

 start, s:
    Restarts a watch with the given name.
    If the watch doesn't exist, a new one is created.

    Usage: start <watch_name>

 stop:
    Pauses the given watch.

    Usage: pause <watch_name/watch_index>

 cont:
    Restarts a watch with the given name.

    Usage: cont <watch_name/watch_index>

 quit, q:
    Saves the status and taken time of all watches and quits the program.

 help, h:
    Prints this help message.

 archive, a:
    Archives (hides) a watch.

 daily:
    Prints all watches and moves them to a backup file.
    This function is meant to be used to compile daily / monthly / etc. progress.

 pcats:
    Prints total times for all categories

 wstats:
    Prints weekly statistics.
    Sums elapsed times for same name watches for each weekday from Monday until now and the sum of
    the whole week.

 wcats:
    Prints weekly category statistics.
    Sums elapsed times for categories for each weekday from Monday until now and the sum of
    the whole week.
```

# Pomodoro ⏱️

## What is Pomodoro?

**Pomodoro** is your personal activity tracker, designed to help you stay focused and organized!  
Easily manage multiple stopwatches for different tasks, track your progress, and keep a record of your productivity—all without needing to keep the app running in the background.

All your data is safely stored in `~/Documents/pomodoro.txt`, so you never lose track of your hard work.

---

## 🚀 Getting Started

Fire up Pomodoro with:
```shell
python pomodoro.py
```

Once running, you can control everything with simple commands:

---

## 🛠️ Commands

- **print, p**  
  _Show all your watches (active & inactive), their status, and elapsed time._

- **new, n**  
  _Create a brand new watch._  
  **Usage:** `new <watch_name>`

- **start, s**  
  _Start or restart a watch. If it doesn’t exist, it’s created for you!_  
  **Usage:** `start <watch_name>`

- **stop**  
  _Pause a running watch._  
  **Usage:** `pause <watch_name/watch_index>`

- **cont**  
  _Continue a paused watch._  
  **Usage:** `cont <watch_name/watch_index>`

- **quit, q**  
  _Save all your progress and exit Pomodoro._

- **help, h**  
  _Show this help message anytime._

- **archive, a**  
  _Archive (hide) a watch you no longer need._

- **daily**  
  _Print all watches and move them to a backup file. Perfect for daily or monthly reviews!_

- **pcats**  
  _See total times for all your categories._

- **wstats**  
  _Get weekly stats: see how much time you’ve spent on each watch, broken down by weekday and total._

- **wcats**  
  _Weekly category stats: track your time by category for each day and the whole week._

---

## 💡 Why Use Pomodoro?

- **No background process needed:** Track time without keeping the app open.
- **Simple, command-driven interface:** Focus on your work, not on learning a new tool.
- **Perfect for daily, weekly, or monthly reviews:** Stay on top of your productivity.

---

Stay productive and make every second count

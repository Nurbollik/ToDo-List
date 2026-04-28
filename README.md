# Planterra 🪷

> A desktop thoughts & tasks planner built with Python and CustomTkinter.

**Authors:** Bekbolotov Nurbolot · Arapbaev Nurzhigit · Kadyrov Sulaiman

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Screenshots](#screenshots)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the App](#running-the-app)
- [Project Structure](#project-structure)
- [Data Storage](#data-storage)
- [Localization](#localization)
- [References](#references)

---

## About

Most to-do apps dump everything into a single flat list. Planterra takes a different approach — it organizes tasks inside named **"thoughts"**, which act as independent topic-based workspaces. Need to keep work tasks, study goals, and personal errands completely separate? Create a thought for each. Switch between them from the sidebar with one click.

The app runs entirely on your machine. No accounts, no cloud sync — all data lives in a local `tasks.json` file that persists between sessions.

---

## Features

| Feature | Description |
|---|---|
| **Thoughts (workspaces)** | Create named sections; each has its own independent task list |
| **Task priorities** | Assign Urgent / Normal / Low priority; tasks are sorted automatically |
| **Pin to top** | Star important tasks so they always appear first |
| **Filters** | Instantly switch between All, Active, and Completed views |
| **Edit & Delete** | Inline editing dialog and one-click deletion |
| **Clear completed** | Remove all done tasks from the current thought in one action |
| **Calendar integration** | Click any date in the built-in calendar to create a date-labelled thought |
| **Dark / Light theme** | Toggle at any time; preference is saved automatically |
| **5 interface languages** | Russian, English, Kyrgyz, Spanish, Chinese — switch without restarting |
| **Persistent storage** | Tasks, thoughts, theme, and language are all saved locally in JSON |

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core language |
| [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | Modern themed GUI framework |
| Pillow (PIL) | Image loading for the empty-state illustration |
| JSON | Local data persistence |
| `calendar` (stdlib) | Calendar grid generation |
| `datetime` (stdlib) | Task timestamps and date selection |
| `os` (stdlib) | Cross-platform file path resolution |

---

## Getting Started

### Prerequisites

- Python **3.10** or newer — [download here](https://www.python.org/downloads/)

### Installation

Clone or download the repository, then install the two dependencies:

```bash
pip install customtkinter pillow
```

### Running the App

```bash
python main.py
```

> **Tip:** Place an `empty.png` image (120×120 px) in the project folder to show a custom illustration when a thought has no tasks. If the file is absent, the app falls back to a 🌿 emoji.

---

## Project Structure

```
planterra/
├── main.py           # Entry point — launches the app
├── ui.py             # All UI classes (main window, calendar, edit dialog)
├── data_manager.py   # Load / save JSON data + priority migration logic
├── config.py         # Colors, badges, language dictionaries, constants
├── tasks.json        # Local data file (auto-created on first run)
└── empty.png         # Optional empty-state illustration (120×120 px)
```

**`main.py`** — just calls `TodoApp().mainloop()`.

**`ui.py`** — contains three classes:
- `TodoApp` — the main application window with sidebar, task list, filters, and toolbar.
- `CalendarWindow` — a modal calendar that creates date-labelled thoughts on day click.
- `EditTaskDialog` — a small modal for renaming an existing task.

**`data_manager.py`** — handles reading and writing `tasks.json`. Also migrates old localized priority strings (e.g. `"Срочная"`, `"Urgent"`) to the canonical internal keys (`"urgent"`, `"normal"`, `"low"`), so saved data stays valid across language switches.

**`config.py`** — single source of truth for all visual constants and every translated string. Adding a new language means adding one new dictionary here and registering it in `ALL_LANGS`.

---

## Data Storage

All application state is stored in `tasks.json` in the project folder. The file is created automatically on first launch if it does not exist.

Example structure:

```json
{
  "thoughts": ["Work", "Study", "📅 28.04.2025"],
  "tasks": [
    {
      "id": 1,
      "text": "Finish the report",
      "done": false,
      "priority": "urgent",
      "created": "28.04.2025 10:30",
      "thought": "Work",
      "pinned": true
    }
  ],
  "theme": "dark",
  "lang": "en"
}
```

Priority values stored in JSON are always **canonical** (`urgent` / `normal` / `low`), regardless of the display language. This means you can switch the interface language and all existing tasks will display correctly.

---

## Localization

The app ships with five languages switchable at runtime from the toolbar:

| Code | Language |
|---|---|
| `ru` | Russian |
| `en` | English |
| `ky` | Kyrgyz |
| `es` | Spanish |
| `zh` | Chinese (Simplified) |

All translated strings live in `config.py` (`LANG_RU`, `LANG_EN`, etc.) under a shared set of keys. The active language dictionary is stored in `app.L` and referenced throughout `ui.py`. Switching language rebuilds the entire UI immediately — no restart required.

To add a new language, create a new dictionary following the same key structure and register it in `ALL_LANGS` and `LANG_ORDER`.

---

## References

**Libraries & Frameworks**

- CustomTkinter — GitHub: https://github.com/TomSchimansky/CustomTkinter
- CustomTkinter — Official Documentation & Tutorial: https://customtkinter.tomschimansky.com/
- Pillow (PIL) — https://python-pillow.org
- Python 3 Standard Library (`calendar`, `datetime`, `json`, `os`) — https://docs.python.org/3/library/

**Video Tutorial**

- *Python CustomTkinter Full Course* — YouTube: https://youtu.be/Y01r643ckfI?si=X8688I-W1pfSQYIV
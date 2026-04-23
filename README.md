# Planterra 🪷 — Thoughts & Tasks Planner

## Group Members

> _Add your group member names here_

---

## Project Description

Planterra is a desktop task management application built with Python and CustomTkinter. It lets users organize their tasks inside named "thoughts" — topic-based workspaces — making it easy to group related to-dos together. The app supports priorities, pinning, filtering, a built-in calendar, dark/light themes, and bilingual (Russian/English) interface switching.

---

## Problem Statement

Most to-do applications treat tasks as a flat, undifferentiated list. This makes it hard to separate tasks by context — for example, keeping work tasks, study goals, and personal errands in the same place without confusion. Users also often switch between languages or prefer different visual themes, yet many lightweight apps offer no such flexibility.

---

## Solution Overview

Planterra introduces the concept of **"thoughts"** — named sections that act as independent workspaces for tasks. Each thought has its own task list with priority levels, completion tracking, and pin-to-top support. The calendar lets users create date-labelled thoughts instantly by clicking a day. All state is persisted locally in a JSON file, so data survives between sessions. The entire UI rebuilds dynamically when the user switches language or theme, with no restart required.

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core programming language |
| CustomTkinter | Modern themed GUI framework |
| Pillow (PIL) | Image loading for empty-state illustration |
| JSON | Local data persistence |
| `calendar` (stdlib) | Calendar grid generation |
| `datetime` (stdlib) | Task timestamps and date selection |
| `os` (stdlib) | File path resolution |

---

## Instructions to Run the Project

### 1. Prerequisites

Make sure Python 3.10 or newer is installed.

### 2. Install dependencies

```bash
pip install customtkinter pillow
```

### 3. Run the application

Place `main.py` and `tasks.json` in the same folder, then run:

```bash
python main.py
```

> **Note:** `tasks.json` is created automatically on first launch if it does not exist. Optionally place an `empty.png` image (120×120 px) in the same folder to show a custom illustration when a thought has no tasks.

---

## Key Features

- **Thoughts (workspaces)** — Create named sections to group related tasks; each thought has its own independent task list.
- **Task priorities** — Assign Urgent / Normal / Low priority to any task; tasks are sorted automatically.
- **Pin to top** — Pin important tasks so they always appear at the top of the list.
- **Filters** — Quickly switch between All, Active, and Completed views.
- **Edit & Delete** — Inline editing dialog and one-click task deletion.
- **Clear completed** — Remove all done tasks from the current thought in one click.
- **Calendar integration** — Open the built-in calendar and click any date to create a date-labelled thought instantly.
- **Dark / Light theme** — Toggle between themes at any time; preference is saved automatically.
- **Bilingual UI (RU / EN)** — Switch the entire interface language between Russian and English without restarting.
- **Persistent storage** — All tasks, thoughts, theme, and language settings are saved locally in `tasks.json`.

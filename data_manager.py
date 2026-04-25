import json
import os
from config import DATA_FILE, PRIORITY_MIGRATION

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

            if isinstance(data, list):
                new_data = {"thoughts": [" "], "tasks": [], "theme": "light", "lang": "ru"}
                for task in data:
                    task["thought"] = " "
                    task["priority"] = PRIORITY_MIGRATION.get(task.get("priority", "normal"), "normal")
                    new_data["tasks"].append(task)
                return new_data

            if "theme" not in data:
                data["theme"] = "light"

            # Если язык не сохранен ставим русский по умолчанию
            if "lang" not in data:
                data["lang"] = "ru"

            # Мигрируем старые локализованные приоритеты в канонические ключи
            if "tasks" in data:
                for task in data["tasks"]:
                    old = task.get("priority", "normal")
                    task["priority"] = PRIORITY_MIGRATION.get(old, "normal")

            return data

    return {"thoughts": [" "], "tasks": [], "theme": "light", "lang": "ru"}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
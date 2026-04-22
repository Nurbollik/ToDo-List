import json
import os
from config import DATA_FILE

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

            if isinstance(data, list):
                new_data = {"thoughts": [" "], "tasks": [], "theme": "light", "lang": "ru"}
                for task in data:
                    task["thought"] = " "
                    new_data["tasks"].append(task)
                return new_data

            if "theme" not in data:
                data["theme"] = "light"

            # Если язык не сохранен ставим русский по умолчанию
            if "lang" not in data:
                data["lang"] = "ru"

            return data

    return {"thoughts": [" "], "tasks": [], "theme": "light", "lang": "ru"}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
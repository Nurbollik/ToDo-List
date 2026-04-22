import json
import os
from config import DATA_FILE

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            if isinstance(data, list):
                new_data = {"thoughts": ["Главная мысль"], "tasks": []}
                for task in data:
                    task["thought"] = "Главная мысль"
                    new_data["tasks"].append(task)
                return new_data
            
            return data
            
    return {"thoughts": ["Главная мысль"], "tasks": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
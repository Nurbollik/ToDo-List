import json
import os
from config import DATA_FILE

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            if isinstance(data, list):
                new_data = {"thoughts": ["Главная мысль"], "tasks": [], "theme": "light"}
                for task in data:
                    task["thought"] = "Главная мысль"
                    new_data["tasks"].append(task)
                return new_data
            
            if "theme" not in data:
                data["theme"] = "light"
                
            return data
            
    return {"thoughts": ["Главная мысль"], "tasks": [], "theme": "light"}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
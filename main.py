import customtkinter as ctk
import json
import os
from datetime import datetime
from PIL import Image, ImageTk

ctk.set_appearance_mode("light")

DATA_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")

COLORS = {
    "bg": "#F9FAFB",
    "surface": "#FFFFFF",
    "primary": "#34D399",
    "primary_hover": "#10B981",
    "text_main": "#1F2937",
    "text_muted": "#9CA3AF",
    "danger": "#F87171",
    "danger_bg": "#FEE2E2",
    "border": "#E5E7EB",
    "sidebar_active": "#ECFDF5",
    "warning": "#F59E0B",
    "warning_bg": "#FEF3C7"
}

BADGES = {
    "Срочная": {"bg": "#FEE2E2", "text": "#EF4444"},
    "Обычная": {"bg": "#F3F4F6", "text": "#6B7280"},
    "Низкая": {"bg": "#D1FAE5", "text": "#059669"}
}

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

class EditTaskDialog(ctk.CTkToplevel):
    def __init__(self, parent, current_text):
        super().__init__(parent)
        self.title("Редактировать задачу")
        self.geometry("450x180")
        self.configure(fg_color=COLORS["bg"])
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.result = None
        self.font_main = ctk.CTkFont(family="Segoe UI", size=14)

        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (450 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (180 // 2)
        self.geometry(f"+{x}+{y}")

        self.entry = ctk.CTkEntry(
            self, font=self.font_main, height=40, corner_radius=8,
            fg_color=COLORS["surface"], border_color=COLORS["primary"], text_color=COLORS["text_main"]
        )
        self.entry.pack(fill="x", padx=20, pady=(30, 20))
        self.entry.insert(0, current_text)
        self.entry.focus()
        self.entry.bind("<Return>", lambda e: self.save())

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20)

        cancel_btn = ctk.CTkButton(
            btn_frame, text="Отмена", fg_color="#F3F4F6", text_color="#4B5563",
            hover_color="#E5E7EB", font=self.font_main, command=self.cancel
        )
        cancel_btn.pack(side="right", padx=(10, 0))

        save_btn = ctk.CTkButton(
            btn_frame, text="Сохранить", fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"], font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            command=self.save
        )
        save_btn.pack(side="right")

        self.wait_window()

    def save(self):
        self.result = self.entry.get().strip()
        self.destroy()

    def cancel(self):
        self.destroy()

class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("To-DO: Мысли и Задачи")
        self.geometry("800x750")
        self.minsize(700, 600)
        self.configure(fg_color=COLORS["bg"])

        self.data = load_data()
        
        if "thoughts" in self.data:
            self.thoughts = self.data["thoughts"]
        else:
            self.thoughts = ["Главная мысль"]
            
        if "tasks" in self.data:
            self.tasks = self.data["tasks"]
        else:
            self.tasks = []

        if len(self.thoughts) > 0:
            self.current_thought = self.thoughts[0]
        else:
            self.current_thought = "Главная мысль"
        
        max_id = 0
        for t in self.tasks:
            if t["id"] > max_id:
                max_id = t["id"]
        self.next_id = max_id + 1
        
        self.filter_mode = "Все"

        self.font_main = ctk.CTkFont(family="Segoe UI", size=14)
        self.font_bold = ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        self.font_strike = ctk.CTkFont(family="Segoe UI", size=14, overstrike=True)
        self.font_small = ctk.CTkFont(family="Segoe UI", size=11)

        self._build_ui()
        self.render_sidebar()
        self.render_tasks()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=0, minsize=220)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, fg_color=COLORS["surface"], corner_radius=0, border_width=1, border_color=COLORS["border"])
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(
            self.sidebar_frame, text="Мои мысли 🧠", 
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"), text_color=COLORS["text_main"]
        ).pack(pady=(20, 10), padx=20, anchor="w")

        self.thoughts_scroll = ctk.CTkScrollableFrame(self.sidebar_frame, fg_color="transparent")
        self.thoughts_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        add_thought_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        add_thought_frame.pack(fill="x", padx=10, pady=20)

        self.thought_entry = ctk.CTkEntry(
            add_thought_frame, placeholder_text="Новая мысль...", height=35,
            fg_color=COLORS["bg"], border_color=COLORS["border"], text_color=COLORS["text_main"]
        )
        self.thought_entry.pack(side="left", fill="x", expand=True)
        self.thought_entry.bind("<Return>", lambda e: self.add_thought())

        ctk.CTkButton(
            add_thought_frame, text="+", width=35, height=35, 
            fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], command=self.add_thought
        ).pack(side="right", padx=(5, 0))

        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew")

        header_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        self.header_title = ctk.CTkLabel(
            header_frame, text=self.current_thought,
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"), text_color=COLORS["text_main"]
        )
        self.header_title.pack(side="left")

        self.counter_label = ctk.CTkLabel(header_frame, text="", text_color=COLORS["text_muted"], font=self.font_main)
        self.counter_label.pack(side="right", pady=(5, 0))

        self.filter_var = ctk.StringVar(value="Все")
        self.filter_seg = ctk.CTkSegmentedButton(
            self.main_area, values=["Все", "Активные", "Выполненные"], variable=self.filter_var,
            command=self.set_filter, font=self.font_main, corner_radius=8,
            fg_color=COLORS["surface"], selected_color=COLORS["primary"],
            selected_hover_color=COLORS["primary_hover"], text_color=COLORS["text_main"]
        )
        self.filter_seg.pack(fill="x", padx=20, pady=(0, 15))

        input_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        input_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.entry = ctk.CTkEntry(
            input_frame, placeholder_text="Что нужно сделать?", font=self.font_main, height=40,
            corner_radius=8, fg_color=COLORS["surface"], border_color=COLORS["border"], text_color=COLORS["text_main"]
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<Return>", lambda e: self.add_task())

        self.priority_var = ctk.StringVar(value="Обычная")
        self.priority_menu = ctk.CTkOptionMenu(
            input_frame, values=["Срочная", "Обычная", "Низкая"], variable=self.priority_var,
            font=self.font_main, width=120, height=40, corner_radius=8,
            fg_color=COLORS["surface"], button_color=COLORS["surface"], button_hover_color="#F3F4F6", text_color=COLORS["text_main"]
        )
        self.priority_menu.pack(side="left", padx=(0, 10))

        add_btn = ctk.CTkButton(
            input_frame, text="+", font=ctk.CTkFont(size=20, weight="bold"), width=40, height=40,
            corner_radius=8, fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], command=self.add_task
        )
        add_btn.pack(side="left")

        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_area, fg_color="transparent")
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        bottom_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=20, pady=(0, 20))

        clear_btn = ctk.CTkButton(
            bottom_frame, text="Очистить выполненные", fg_color=COLORS["surface"], text_color=COLORS["primary"],
            border_width=1, border_color=COLORS["primary"], hover_color="#ECFDF5",
            font=self.font_bold, height=45, corner_radius=8, command=self.clear_done
        )
        clear_btn.pack(fill="x")

    def _save_state(self):
        self.data["thoughts"] = self.thoughts
        self.data["tasks"] = self.tasks
        save_data(self.data)

    def render_sidebar(self):
        for widget in self.thoughts_scroll.winfo_children():
            widget.destroy()

        for thought in self.thoughts:
            if thought == self.current_thought:
                bg_color = COLORS["sidebar_active"]
                text_color = COLORS["primary"]
                font = self.font_bold
            else:
                bg_color = "transparent"
                text_color = COLORS["text_main"]
                font = self.font_main

            th_frame = ctk.CTkFrame(self.thoughts_scroll, fg_color=bg_color, corner_radius=8)
            th_frame.pack(fill="x", pady=2)

            btn = ctk.CTkButton(
                th_frame, text=thought, fg_color="transparent", text_color=text_color,
                font=font, hover_color=COLORS["sidebar_active"], anchor="w",
                command=lambda t=thought: self.select_thought(t)
            )
            btn.pack(side="left", fill="x", expand=True, padx=5, pady=5)

            if len(self.thoughts) > 1:
                del_btn = ctk.CTkButton(
                    th_frame, text="✕", width=25, height=25, fg_color="transparent", text_color=COLORS["danger"],
                    hover_color=COLORS["danger_bg"], command=lambda t=thought: self.delete_thought(t)
                )
                del_btn.pack(side="right", padx=5)

    def select_thought(self, thought):
        self.current_thought = thought
        self.header_title.configure(text=self.current_thought)
        self.render_sidebar()
        self.render_tasks()

    def add_thought(self):
        new_thought = self.thought_entry.get().strip()
        if new_thought != "":
            if new_thought not in self.thoughts:
                self.thoughts.append(new_thought)
                self.thought_entry.delete(0, "end")
                self._save_state()
                self.select_thought(new_thought)

    def delete_thought(self, thought):
        self.thoughts.remove(thought)
        
        new_tasks = []
        for t in self.tasks:
            if "thought" in t:
                if t["thought"] != thought:
                    new_tasks.append(t)
            else:
                new_tasks.append(t)
                
        self.tasks = new_tasks
        self._save_state()
        
        if self.current_thought == thought:
            self.select_thought(self.thoughts[0])
        else:
            self.render_sidebar()

    def set_filter(self, mode):
        self.filter_mode = mode
        self.render_tasks()

    def sort_tasks(self, current_tasks):
        priority_weight = {"Срочная": 0, "Обычная": 1, "Низкая": 2}
        
        def sort_key(t):
            is_done = t["done"]
            
            is_pinned = False
            if "pinned" in t:
                if t["pinned"] == True:
                    is_pinned = True
                    
            not_pinned = not is_pinned
            
            if t["priority"] in priority_weight:
                priority = priority_weight[t["priority"]]
            else:
                priority = 1
                
            task_id_negative = -t["id"]
            
            return (is_done, not_pinned, priority, task_id_negative)
            
        current_tasks.sort(key=sort_key)

    def add_task(self):
        text = self.entry.get().strip()
        if text == "":
            self.entry.focus()
            return

        task = {
            "id": self.next_id,
            "text": text,
            "done": False,
            "priority": self.priority_var.get(),
            "created": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "thought": self.current_thought,
            "pinned": False
        }
        self.tasks.append(task)
        self.next_id += 1
        self.entry.delete(0, "end")
        self._save_state()
        self.render_tasks()

    def toggle_task(self, task_id):
        for t in self.tasks:
            if t["id"] == task_id:
                if t["done"] == True:
                    t["done"] = False
                else:
                    t["done"] = True
                break
        self._save_state()
        self.render_tasks()

    def toggle_pin(self, task_id):
        for t in self.tasks:
            if t["id"] == task_id:
                if "pinned" in t:
                    if t["pinned"] == True:
                        t["pinned"] = False
                    else:
                        t["pinned"] = True
                else:
                    t["pinned"] = True
                break
        self._save_state()
        self.render_tasks()

    def edit_task(self, task_id):
        for t in self.tasks:
            if t["id"] == task_id:
                dialog = EditTaskDialog(self, t["text"])
                if dialog.result != None:
                    t["text"] = dialog.result
                    self._save_state()
                    self.render_tasks()
                break

    def delete_task(self, task_id):
        new_tasks = []
        for t in self.tasks:
            if t["id"] != task_id:
                new_tasks.append(t)
        self.tasks = new_tasks
        self._save_state()
        self.render_tasks()

    def clear_done(self):
        new_tasks = []
        for t in self.tasks:
            is_current_thought = False
            if "thought" in t:
                if t["thought"] == self.current_thought:
                    is_current_thought = True
                    
            if t["done"] == True and is_current_thought == True:
                continue
            
            new_tasks.append(t)
            
        self.tasks = new_tasks
        self._save_state()
        self.render_tasks()

    def render_tasks(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        current_thought_tasks = []
        for t in self.tasks:
            if "thought" in t:
                if t["thought"] == self.current_thought:
                    current_thought_tasks.append(t)
            else:
                if self.current_thought == "Главная мысль":
                    current_thought_tasks.append(t)

        self.sort_tasks(current_thought_tasks)

        done_count = 0
        for t in current_thought_tasks:
            if t["done"] == True:
                done_count += 1
                
        total_tasks = len(current_thought_tasks)
        self.counter_label.configure(text=f"Выполнено: {done_count} из {total_tasks}")

        visible = []
        if self.filter_mode == "Активные":
            for t in current_thought_tasks:
                if t["done"] == False:
                    visible.append(t)
        elif self.filter_mode == "Выполненные":
            for t in current_thought_tasks:
                if t["done"] == True:
                    visible.append(t)
        else:
            visible = current_thought_tasks

        if len(visible) == 0:
            empty_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
            empty_frame.pack(fill="both", expand=True, pady=60)

            img_path = os.path.join(os.path.dirname(__file__), "empty.png")
            try:
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    ctk_img = ctk.CTkImage(light_image=img, size=(120, 120))
                    img_lbl = ctk.CTkLabel(empty_frame, image=ctk_img, text="")
                    img_lbl.pack(pady=(0, 15))
                else:
                    ctk.CTkLabel(empty_frame, text="🌿", font=ctk.CTkFont(size=60)).pack(pady=(0, 10))
            except Exception:
                pass

            ctk.CTkLabel(
                empty_frame, text="В этой мысли пока пусто", 
                font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"), text_color=COLORS["text_main"]
            ).pack()

            ctk.CTkLabel(
                empty_frame, text="Добавьте свою первую задачу выше", 
                font=self.font_main, text_color=COLORS["text_muted"]
            ).pack()
            return

        for task in visible:
            self._render_task(task)

    def _render_task(self, task):
        is_pinned = False
        if "pinned" in task:
            if task["pinned"] == True:
                is_pinned = True

        if is_pinned == True and task["done"] == False:
            border_col = COLORS["warning"]
            b_width = 2
        else:
            border_col = COLORS["border"]
            b_width = 1

        frame = ctk.CTkFrame(
            self.scrollable_frame, fg_color=COLORS["surface"], 
            corner_radius=10, border_width=b_width, border_color=border_col
        )
        frame.pack(fill="x", padx=10, pady=(0, 8))

        check = ctk.CTkCheckBox(
            frame, text="", width=24, height=24, corner_radius=6,
            fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], border_color=COLORS["border"],
            command=lambda tid=task["id"]: self.toggle_task(tid)
        )
        
        if task["done"] == True:
            check.select()
            
        check.pack(side="left", padx=(15, 5), pady=15)

        text_frame = ctk.CTkFrame(frame, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True, padx=5)

        if task["done"] == True:
            lbl_font = self.font_strike
            lbl_color = COLORS["text_muted"]
        else:
            lbl_font = self.font_main
            lbl_color = COLORS["text_main"]

        ctk.CTkLabel(text_frame, text=task["text"], font=lbl_font, text_color=lbl_color, anchor="w", justify="left").pack(fill="x")

        if "created" in task:
            ctk.CTkLabel(text_frame, text=task["created"], font=self.font_small, text_color=COLORS["text_muted"], anchor="w").pack(fill="x")

        if task["priority"] in BADGES:
            p_colors = BADGES[task["priority"]]
        else:
            p_colors = BADGES["Обычная"]
            
        badge = ctk.CTkLabel(
            frame, text=task["priority"], font=self.font_small, fg_color=p_colors["bg"],
            text_color=p_colors["text"], corner_radius=6, width=70, height=24
        )
        badge.pack(side="left", padx=(10, 5))

        if is_pinned == True:
            pin_icon = "★"
            pin_color = COLORS["warning"]
        else:
            pin_icon = "☆"
            pin_color = COLORS["text_muted"]
        
        pin_btn = ctk.CTkButton(
            frame, text=pin_icon, width=30, height=30, fg_color="transparent", text_color=pin_color,
            hover_color=COLORS["warning_bg"], font=ctk.CTkFont(size=18), 
            command=lambda tid=task["id"]: self.toggle_pin(tid)
        )
        pin_btn.pack(side="left", padx=2)

        edit_btn = ctk.CTkButton(
            frame, text="✎", width=30, height=30, fg_color="transparent", text_color=COLORS["text_muted"],
            hover_color="#F3F4F6", font=self.font_main, command=lambda tid=task["id"]: self.edit_task(tid)
        )
        edit_btn.pack(side="left", padx=2)

        del_btn = ctk.CTkButton(
            frame, text="✕", width=30, height=30, fg_color="transparent", text_color=COLORS["danger"],
            hover_color=COLORS["danger_bg"], font=self.font_main, command=lambda tid=task["id"]: self.delete_task(tid)
        )
        del_btn.pack(side="left", padx=(2, 10))


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
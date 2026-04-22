import customtkinter as ctk
import json
import os
from datetime import datetime
from PIL import Image, ImageTk

# Настройка внешнего вида окна
ctk.set_appearance_mode("light")

DATA_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")

# Мягкая зелено-белая палитра
COLORS = {
    "bg": "#F9FAFB",  # Очень светлый серый/белый для фона
    "surface": "#FFFFFF",  # Белый для карточек
    "primary": "#34D399",  # Мягкий зеленый (Изумрудный)
    "primary_hover": "#10B981",  # Чуть более темный зеленый для наведения
    "text_main": "#1F2937",  # Темно-серый для текста (мягче черного)
    "text_muted": "#9CA3AF",  # Светло-серый для неактивного текста
    "danger": "#F87171",  # Мягкий красный для удаления
    "danger_bg": "#FEE2E2",  # Очень светлый красный для фона кнопки удаления
    "border": "#E5E7EB"  # Цвет границ
}

# Цвета для бейджей приоритетов (адаптированы под мягкий стиль)
BADGES = {
    "Срочная": {"bg": "#FEE2E2", "text": "#EF4444"},
    "Обычная": {"bg": "#F3F4F6", "text": "#6B7280"},
    "Низкая": {"bg": "#D1FAE5", "text": "#059669"}
}


def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


class EditTaskDialog(ctk.CTkToplevel):
    """Кастомное окно для редактирования задачи"""

    def __init__(self, parent, current_text):
        super().__init__(parent)
        self.title("Редактировать задачу")
        self.geometry("450x180")
        self.configure(fg_color=COLORS["bg"])
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()  # Блокируем основное окно

        self.result = None
        self.font_main = ctk.CTkFont(family="Segoe UI", size=14)

        # Центрируем окно относительно родительского
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (450 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (180 // 2)
        self.geometry(f"+{x}+{y}")

        # Поле ввода
        self.entry = ctk.CTkEntry(
            self,
            font=self.font_main,
            height=40,
            corner_radius=8,
            fg_color=COLORS["surface"],
            border_color=COLORS["primary"],
            text_color=COLORS["text_main"]
        )
        self.entry.pack(fill="x", padx=20, pady=(30, 20))
        self.entry.insert(0, current_text)
        self.entry.focus()
        self.entry.bind("<Return>", lambda e: self.save())

        # Кнопки
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20)

        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Отмена",
            fg_color="#F3F4F6",
            text_color="#4B5563",
            hover_color="#E5E7EB",
            font=self.font_main,
            command=self.cancel
        )
        cancel_btn.pack(side="right", padx=(10, 0))

        save_btn = ctk.CTkButton(
            btn_frame,
            text="Сохранить",
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
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

        self.title("To-DO")
        self.geometry("550x750")
        self.minsize(450, 600)
        self.configure(fg_color=COLORS["bg"])

        self.tasks = load_tasks()
        self.next_id = max((t["id"] for t in self.tasks), default=0) + 1
        self.filter_mode = "Все"

        # Шрифты
        self.font_main = ctk.CTkFont(family="Segoe UI", size=14)
        self.font_bold = ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        self.font_strike = ctk.CTkFont(family="Segoe UI", size=14, overstrike=True)
        self.font_small = ctk.CTkFont(family="Segoe UI", size=11)

        self._build_ui()
        self.render()

    def _build_ui(self):
        # --- Шапка ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            header_frame,
            text="Мои задачи",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=COLORS["text_main"]
        ).pack(side="left")

        self.counter_label = ctk.CTkLabel(
            header_frame,
            text="",
            text_color=COLORS["text_muted"],
            font=self.font_main
        )
        self.counter_label.pack(side="right", pady=(5, 0))

        # --- Фильтры ---
        self.filter_var = ctk.StringVar(value="Все")
        self.filter_seg = ctk.CTkSegmentedButton(
            self,
            values=["Все", "Активные", "Выполненные"],
            variable=self.filter_var,
            command=self.set_filter,
            font=self.font_main,
            corner_radius=8,
            fg_color=COLORS["surface"],
            selected_color=COLORS["primary"],
            selected_hover_color=COLORS["primary_hover"],
            unselected_color=COLORS["surface"],
            unselected_hover_color="#F3F4F6",
            text_color=COLORS["text_main"]
        )
        self.filter_seg.pack(fill="x", padx=20, pady=(0, 15))

        # --- Зона ввода новой задачи ---
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Что нужно сделать?",
            font=self.font_main,
            height=40,
            corner_radius=8,
            fg_color=COLORS["surface"],
            border_color=COLORS["border"],
            text_color=COLORS["text_main"]
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<Return>", lambda e: self.add_task())

        self.priority_var = ctk.StringVar(value="Обычная")
        self.priority_menu = ctk.CTkOptionMenu(
            input_frame,
            values=["Срочная", "Обычная", "Низкая"],
            variable=self.priority_var,
            font=self.font_main,
            dropdown_font=self.font_main,
            width=120,
            height=40,
            corner_radius=8,
            fg_color=COLORS["surface"],
            button_color=COLORS["surface"],
            button_hover_color="#F3F4F6",
            text_color=COLORS["text_main"],
            dropdown_fg_color=COLORS["surface"],
            dropdown_text_color=COLORS["text_main"],
            dropdown_hover_color="#F3F4F6"
        )
        self.priority_menu.pack(side="left", padx=(0, 10))

        add_btn = ctk.CTkButton(
            input_frame,
            text="+",
            font=ctk.CTkFont(size=20, weight="bold"),
            width=40,
            height=40,
            corner_radius=8,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            command=self.add_task
        )
        add_btn.pack(side="left")

        # --- Список задач ---
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # --- Нижняя панель ---
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=20, pady=(0, 20))

        clear_btn = ctk.CTkButton(
            bottom_frame,
            text="Очистить выполненные",
            fg_color=COLORS["surface"],
            text_color=COLORS["primary"],
            border_width=1,
            border_color=COLORS["primary"],
            hover_color="#ECFDF5",  # Супер-светлый зеленый
            font=self.font_bold,
            height=45,
            corner_radius=8,
            command=self.clear_done
        )
        clear_btn.pack(fill="x")

    def set_filter(self, mode):
        self.filter_mode = mode
        self.render()

    def sort_tasks(self):
        priority_weight = {"Срочная": 0, "Обычная": 1, "Низкая": 2}
        self.tasks.sort(key=lambda t: (t["done"], priority_weight.get(t["priority"], 1), -t["id"]))

    def add_task(self):
        text = self.entry.get().strip()
        if not text:
            self.entry.focus()
            return

        task = {
            "id": self.next_id,
            "text": text,
            "done": False,
            "priority": self.priority_var.get(),
            "created": datetime.now().strftime("%d.%m.%Y %H:%M"),
        }
        self.tasks.append(task)
        self.next_id += 1
        self.entry.delete(0, "end")
        self.sort_tasks()
        save_tasks(self.tasks)
        self.render()

    def toggle(self, task_id):
        for t in self.tasks:
            if t["id"] == task_id:
                t["done"] = not t["done"]
                break
        self.sort_tasks()
        save_tasks(self.tasks)
        self.render()

    def edit_task(self, task_id):
        for t in self.tasks:
            if t["id"] == task_id:
                # Вызов нашего нового красивого окна
                dialog = EditTaskDialog(self, t["text"])
                if dialog.result:
                    t["text"] = dialog.result
                    save_tasks(self.tasks)
                    self.render()
                break

    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        save_tasks(self.tasks)
        self.render()

    def clear_done(self):
        self.tasks = [t for t in self.tasks if not t["done"]]
        save_tasks(self.tasks)
        self.render()

    def render(self):
        # Очистка
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        done_count = sum(1 for t in self.tasks if t["done"])
        self.counter_label.configure(text=f"Выполнено: {done_count} из {len(self.tasks)}")

        visible = self.tasks
        if self.filter_mode == "Активные":
            visible = [t for t in self.tasks if not t["done"]]
        elif self.filter_mode == "Выполненные":
            visible = [t for t in self.tasks if t["done"]]

        # --- Отображение заглушки, если список пуст ---
        if not visible:
            empty_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
            empty_frame.pack(fill="both", expand=True, pady=60)

            img_path = os.path.join(os.path.dirname(__file__), "empty.png")
            try:
                # Пытаемся загрузить картинку empty.png
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    ctk_img = ctk.CTkImage(light_image=img, size=(120, 120))
                    img_lbl = ctk.CTkLabel(empty_frame, image=ctk_img, text="")
                    img_lbl.pack(pady=(0, 15))
                else:
                    # Резервный вариант, если картинки нет
                    ctk.CTkLabel(empty_frame, text="🌿", font=ctk.CTkFont(size=60)).pack(pady=(0, 10))
            except Exception:
                pass

            ctk.CTkLabel(
                empty_frame,
                text="Список пуст",
                font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
                text_color=COLORS["text_main"]
            ).pack()

            ctk.CTkLabel(
                empty_frame,
                text="Время выпить чаю и отдохнуть",
                font=self.font_main,
                text_color=COLORS["text_muted"]
            ).pack()
            return

        for task in visible:
            self._render_task(task)

    def _render_task(self, task):
        frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color=COLORS["surface"],
            corner_radius=10,
            border_width=1,
            border_color=COLORS["border"]
        )
        frame.pack(fill="x", padx=10, pady=(0, 8))

        check = ctk.CTkCheckBox(
            frame,
            text="",
            width=24,
            height=24,
            corner_radius=6,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            border_color=COLORS["border"],
            command=lambda tid=task["id"]: self.toggle(tid)
        )
        if task["done"]:
            check.select()
        check.pack(side="left", padx=(15, 5), pady=15)

        text_frame = ctk.CTkFrame(frame, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True, padx=5)

        lbl_font = self.font_strike if task["done"] else self.font_main
        lbl_color = COLORS["text_muted"] if task["done"] else COLORS["text_main"]

        ctk.CTkLabel(text_frame, text=task["text"], font=lbl_font, text_color=lbl_color, anchor="w",
                     justify="left").pack(fill="x")

        if task.get("created"):
            ctk.CTkLabel(text_frame, text=task["created"], font=self.font_small, text_color=COLORS["text_muted"],
                         anchor="w").pack(
                fill="x")

        p_colors = BADGES.get(task["priority"], BADGES["Обычная"])
        badge = ctk.CTkLabel(
            frame,
            text=task["priority"],
            font=self.font_small,
            fg_color=p_colors["bg"],
            text_color=p_colors["text"],
            corner_radius=6,
            width=70,
            height=24
        )
        badge.pack(side="left", padx=(10, 5))

        edit_btn = ctk.CTkButton(
            frame, text="✎", width=30, height=30, fg_color="transparent", text_color=COLORS["text_muted"],
            hover_color="#F3F4F6",
            font=self.font_main,
            command=lambda tid=task["id"]: self.edit_task(tid)
        )
        edit_btn.pack(side="left", padx=2)

        del_btn = ctk.CTkButton(
            frame, text="✕", width=30, height=30, fg_color="transparent", text_color=COLORS["danger"],
            hover_color=COLORS["danger_bg"],
            font=self.font_main,
            command=lambda tid=task["id"]: self.delete_task(tid)
        )
        del_btn.pack(side="left", padx=(2, 10))


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
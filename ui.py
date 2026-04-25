import customtkinter as ctk
import os
import calendar
from datetime import datetime
from PIL import Image

from config import COLORS, BADGES, ALL_LANGS, LANG_ORDER, LANG_DISPLAY
from data_manager import load_data, save_data


class CalendarWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Берём переводы из родительского окна
        L = self.parent.L

        self.title(L["calendar_title"])
        self.geometry("600x650")
        self.configure(fg_color=COLORS["bg"])
        self.transient(parent)
        self.grab_set()

        self.now = datetime.now()
        self.viewYear = self.now.year
        self.viewMonth = self.now.month

        self.fontMain = ctk.CTkFont(family="Segoe UI", size=14)
        self.fontBold = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")

        self.buildCalendarUi()

        self.bind("<MouseWheel>", self.onMouseWheel)
        self.bind("<Button-4>", self.onMouseWheel)
        self.bind("<Button-5>", self.onMouseWheel)

    def onMouseWheel(self, event):
        if hasattr(event, "delta") and event.delta != 0:
            if event.delta > 0:
                self.prevMonth()
            else:
                self.nextMonth()
        elif hasattr(event, "num"):
            if event.num == 4:
                self.prevMonth()
            elif event.num == 5:
                self.nextMonth()

    def buildCalendarUi(self):
        for widget in self.winfo_children():
            widget.destroy()

        L = self.parent.L

        headerFrame = ctk.CTkFrame(self, fg_color="transparent")
        headerFrame.pack(fill="x", padx=20, pady=20)

        ctk.CTkButton(
            headerFrame, text="<", width=40, fg_color=COLORS["surface"],
            text_color=COLORS["text_main"], hover_color=COLORS["border"],
            command=self.prevMonth
        ).pack(side="left")

        monthName = L["months"][self.viewMonth - 1]
        self.titleLabel = ctk.CTkLabel(
            headerFrame, text=f"{monthName} {self.viewYear}",
            font=self.fontBold, text_color=COLORS["text_main"]
        )
        self.titleLabel.pack(side="left", expand=True)

        ctk.CTkButton(
            headerFrame, text=">", width=40, fg_color=COLORS["surface"],
            text_color=COLORS["text_main"], hover_color=COLORS["border"],
            command=self.nextMonth
        ).pack(side="right")

        daysFrame = ctk.CTkFrame(self, fg_color="transparent")
        daysFrame.pack(fill="both", expand=True, padx=20, pady=10)

        weekDays = L["weekdays"]
        for i in range(len(weekDays)):
            daysFrame.grid_columnconfigure(i, weight=1)
            ctk.CTkLabel(
                daysFrame, text=weekDays[i],
                font=self.fontMain, text_color=COLORS["text_muted"]
            ).grid(row=0, column=i, pady=10)

        monthCalendar = calendar.monthcalendar(self.viewYear, self.viewMonth)
        rowIdx = 1
        for week in monthCalendar:
            for colIdx in range(7):
                day = week[colIdx]
                if day == 0:
                    ctk.CTkLabel(daysFrame, text="").grid(row=rowIdx, column=colIdx)
                else:
                    self.createDayButton(daysFrame, day, rowIdx, colIdx)
            rowIdx = rowIdx + 1

    def createDayButton(self, container, day, row, col):
        btnBg = COLORS["surface"]
        btnText = COLORS["text_main"]
        borderCol = COLORS["border"]

        if day == self.now.day:
            if self.viewMonth == self.now.month:
                if self.viewYear == self.now.year:
                    borderCol = COLORS["primary"]

        btn = ctk.CTkButton(
            container, text=str(day), fg_color=btnBg, text_color=btnText,
            border_width=1, border_color=borderCol, hover_color=COLORS["bg"],
            height=60, font=self.fontMain,
            command=lambda d=day: self.selectDate(d)
        )
        btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

    def selectDate(self, day):
        dateStr = f"📅 {day:02d}.{self.viewMonth:02d}.{self.viewYear}"
        if dateStr not in self.parent.thoughts:
            self.parent.thoughts.append(dateStr)
            self.parent.saveState()
        self.parent.selectThought(dateStr)
        self.destroy()

    def prevMonth(self):
        self.viewMonth = self.viewMonth - 1
        if self.viewMonth < 1:
            self.viewMonth = 12
            self.viewYear = self.viewYear - 1
        self.buildCalendarUi()

    def nextMonth(self):
        self.viewMonth = self.viewMonth + 1
        if self.viewMonth > 12:
            self.viewMonth = 1
            self.viewYear = self.viewYear + 1
        self.buildCalendarUi()


class EditTaskDialog(ctk.CTkToplevel):
    def __init__(self, parent, currentText):
        super().__init__(parent)

        # Берём переводы из родительского окна
        L = parent.L

        self.title(L["edit_dialog_title"])
        self.geometry("450x180")
        self.configure(fg_color=COLORS["bg"])
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.result = None
        self.fontMain = ctk.CTkFont(family="Segoe UI", size=14)

        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (450 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (180 // 2)
        self.geometry(f"+{x}+{y}")

        self.entry = ctk.CTkEntry(
            self, font=self.fontMain, height=40, corner_radius=8,
            fg_color=COLORS["surface"], border_color=COLORS["primary"],
            text_color=COLORS["text_main"]
        )
        self.entry.pack(fill="x", padx=20, pady=(30, 20))
        self.entry.insert(0, currentText)
        self.entry.focus()
        self.entry.bind("<Return>", lambda e: self.saveTask())

        btnFrame = ctk.CTkFrame(self, fg_color="transparent")
        btnFrame.pack(fill="x", padx=20)

        ctk.CTkButton(
            btnFrame, text=L["edit_cancel_btn"],
            fg_color=COLORS["surface"], text_color=COLORS["text_main"],
            hover_color=COLORS["border"], font=self.fontMain,
            border_width=1, border_color=COLORS["border"],
            command=self.cancelDialog
        ).pack(side="right", padx=(10, 0))

        ctk.CTkButton(
            btnFrame, text=L["edit_save_btn"],
            fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            command=self.saveTask
        ).pack(side="right")

        self.wait_window()

    def saveTask(self):
        self.result = self.entry.get().strip()
        self.destroy()

    def cancelDialog(self):
        self.destroy()


class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.data = load_data()

        # Загружаем тему
        if "theme" in self.data:
            self.theme = self.data["theme"]
        else:
            self.theme = "light"

        ctk.set_appearance_mode(self.theme)

        # Загружаем язык и сразу берём нужный словарь
        if "lang" in self.data:
            self.lang = self.data["lang"]
        else:
            self.lang = "ru"

        # self.L — текущий словарь переводов. Используем его везде в коде.
        self.L = ALL_LANGS[self.lang]

        self.title(self.L["app_title"])
        self.geometry("800x750")
        self.minsize(700, 600)
        self.configure(fg_color=COLORS["bg"])

        if "thoughts" in self.data:
            self.thoughts = self.data["thoughts"]
        else:
            self.thoughts = [" "]

        if "tasks" in self.data:
            self.tasks = self.data["tasks"]
        else:
            self.tasks = []

        if len(self.thoughts) > 0:
            self.currentThought = self.thoughts[0]
        else:
            self.currentThought = " "

        maxId = 0
        for t in self.tasks:
            if t["id"] > maxId:
                maxId = t["id"]
        self.nextId = maxId + 1

        self.filterMode = self.L["filter_all"]

        self.fontMain = ctk.CTkFont(family="Segoe UI", size=14)
        self.fontBold = ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        self.fontStrike = ctk.CTkFont(family="Segoe UI", size=14, overstrike=True)
        self.fontSmall = ctk.CTkFont(family="Segoe UI", size=11)

        self.buildUi()
        self.renderSidebar()
        self.renderTasks()

    def buildUi(self):
        self.grid_columnconfigure(0, weight=0, minsize=220)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Боковая панель
        self.sidebarFrame = ctk.CTkFrame(
            self, fg_color=COLORS["surface"], corner_radius=0,
            border_width=1, border_color=COLORS["border"]
        )
        self.sidebarFrame.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(
            self.sidebarFrame, text=self.L["app_logo"],
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color=COLORS["text_main"]
        ).pack(pady=(20, 10), padx=20, anchor="w")

        self.thoughtsScroll = ctk.CTkScrollableFrame(self.sidebarFrame, fg_color="transparent")
        self.thoughtsScroll.pack(fill="both", expand=True, padx=10, pady=10)

        addThoughtFrame = ctk.CTkFrame(self.sidebarFrame, fg_color="transparent")
        addThoughtFrame.pack(fill="x", padx=10, pady=20)

        self.thoughtEntry = ctk.CTkEntry(
            addThoughtFrame,
            placeholder_text=self.L["new_thought_placeholder"],
            height=35,
            fg_color=COLORS["bg"], border_color=COLORS["border"],
            text_color=COLORS["text_main"]
        )
        self.thoughtEntry.pack(side="left", fill="x", expand=True)
        self.thoughtEntry.bind("<Return>", lambda e: self.addThought())

        ctk.CTkButton(
            addThoughtFrame, text="+", width=35, height=35,
            fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
            command=self.addThought
        ).pack(side="right", padx=(5, 0))

        calBtn = ctk.CTkButton(
            self.sidebarFrame, text=self.L["calendar_btn"],
            fg_color=COLORS["surface"], text_color=COLORS["primary"],
            border_width=1, border_color=COLORS["primary"],
            hover_color=COLORS["bg"], font=self.fontBold, height=45,
            command=self.openCalendar
        )
        calBtn.pack(fill="x", padx=20, pady=(0, 20), side="bottom")

        # Основная область
        self.mainArea = ctk.CTkFrame(self, fg_color="transparent")
        self.mainArea.grid(row=0, column=1, sticky="nsew")

        headerFrame = ctk.CTkFrame(self.mainArea, fg_color="transparent")
        headerFrame.pack(fill="x", padx=20, pady=(20, 10))

        self.headerTitle = ctk.CTkLabel(
            headerFrame, text=self.currentThought,
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=COLORS["text_main"]
        )
        self.headerTitle.pack(side="left")

        # Кнопка смены языка — показываем следующий язык в цикле
        nextLangIndex = (LANG_ORDER.index(self.lang)) % len(LANG_ORDER)
        nextLangLabel = LANG_DISPLAY[LANG_ORDER[nextLangIndex]]
        self.langBtn = ctk.CTkButton(
            headerFrame, text=nextLangLabel, width=45, height=35,
            fg_color="transparent", text_color=COLORS["text_main"],
            hover_color=COLORS["border"],
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=self.toggleLang
        )
        self.langBtn.pack(side="right", padx=(5, 0))

        # Кнопка смены темы
        if self.theme == "light":
            themeText = "🌙"
        else:
            themeText = "☀️"

        self.themeBtn = ctk.CTkButton(
            headerFrame, text=themeText, width=35, height=35,
            fg_color="transparent", text_color=COLORS["text_main"],
            hover_color=COLORS["border"],
            font=ctk.CTkFont(size=20), command=self.toggleTheme
        )
        self.themeBtn.pack(side="right", padx=(15, 0))

        self.counterLabel = ctk.CTkLabel(
            headerFrame, text="", text_color=COLORS["text_muted"], font=self.fontMain
        )
        self.counterLabel.pack(side="right", pady=(5, 0))

        # Фильтры
        self.filterVar = ctk.StringVar(value=self.L["filter_all"])
        self.filterSeg = ctk.CTkSegmentedButton(
            self.mainArea,
            values=[self.L["filter_all"], self.L["filter_active"], self.L["filter_done"]],
            variable=self.filterVar,
            command=self.setFilter,
            font=self.fontMain, corner_radius=8,
            fg_color=COLORS["surface"], selected_color=COLORS["primary"],
            selected_hover_color=COLORS["primary_hover"], text_color=COLORS["text_main"]
        )
        self.filterSeg.pack(fill="x", padx=20, pady=(0, 15))

        # Поле ввода задачи
        inputFrame = ctk.CTkFrame(self.mainArea, fg_color="transparent")
        inputFrame.pack(fill="x", padx=20, pady=(0, 15))

        self.taskEntry = ctk.CTkEntry(
            inputFrame, placeholder_text=self.L["task_placeholder"],
            font=self.fontMain, height=40, corner_radius=8,
            fg_color=COLORS["surface"], border_color=COLORS["border"],
            text_color=COLORS["text_main"]
        )
        self.taskEntry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.taskEntry.bind("<Return>", lambda e: self.addTask())

        self.priorityVar = ctk.StringVar(value=self.L["priority_normal"])
        self.priorityMenu = ctk.CTkOptionMenu(
            inputFrame,
            values=[self.L["priority_urgent"], self.L["priority_normal"], self.L["priority_low"]],
            variable=self.priorityVar,
            font=self.fontMain, width=120, height=40, corner_radius=8,
            fg_color=COLORS["surface"], button_color=COLORS["surface"],
            button_hover_color=COLORS["bg"], text_color=COLORS["text_main"]
        )
        self.priorityMenu.pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            inputFrame, text="+", font=ctk.CTkFont(size=20, weight="bold"),
            width=40, height=40, corner_radius=8,
            fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
            command=self.addTask
        ).pack(side="left")

        self.scrollableFrame = ctk.CTkScrollableFrame(self.mainArea, fg_color="transparent")
        self.scrollableFrame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        bottomFrame = ctk.CTkFrame(self.mainArea, fg_color="transparent")
        bottomFrame.pack(fill="x", padx=20, pady=(0, 20))

        ctk.CTkButton(
            bottomFrame, text=self.L["clear_done_btn"],
            fg_color=COLORS["surface"], text_color=COLORS["primary"],
            border_width=1, border_color=COLORS["primary"],
            hover_color=COLORS["bg"], font=self.fontBold, height=45,
            corner_radius=8, command=self.clearDoneTasks
        ).pack(fill="x")

    def toggleTheme(self):
        if self.theme == "light":
            self.theme = "dark"
            self.themeBtn.configure(text="☀️")
        else:
            self.theme = "light"
            self.themeBtn.configure(text="🌙")

        ctk.set_appearance_mode(self.theme)
        self.data["theme"] = self.theme
        self.saveState()

    def toggleLang(self):
        # Переключаем язык по кругу: ru → en → ky → es → zh → ru
        currentIndex = LANG_ORDER.index(self.lang) if self.lang in LANG_ORDER else 0
        self.lang = LANG_ORDER[(currentIndex + 1) % len(LANG_ORDER)]

        self.L = ALL_LANGS[self.lang]
        self.data["lang"] = self.lang
        self.saveState()

        # Перестраиваем весь интерфейс с новыми строками
        for widget in self.winfo_children():
            widget.destroy()

        self.title(self.L["app_title"])
        self.filterMode = self.L["filter_all"]

        self.buildUi()
        self.renderSidebar()
        self.renderTasks()

    def saveState(self):
        self.data["thoughts"] = self.thoughts
        self.data["tasks"] = self.tasks
        save_data(self.data)

    def renderSidebar(self):
        for widget in self.thoughtsScroll.winfo_children():
            widget.destroy()

        for thought in self.thoughts:
            if thought == self.currentThought:
                bgColor = COLORS["sidebar_active"]
                textColor = COLORS["primary"]
                fontUsed = self.fontBold
            else:
                bgColor = "transparent"
                textColor = COLORS["text_main"]
                fontUsed = self.fontMain

            thFrame = ctk.CTkFrame(self.thoughtsScroll, fg_color=bgColor, corner_radius=8)
            thFrame.pack(fill="x", pady=2)

            ctk.CTkButton(
                thFrame, text=thought, fg_color="transparent", text_color=textColor,
                font=fontUsed, hover_color=COLORS["sidebar_active"], anchor="w",
                command=lambda t=thought: self.selectThought(t)
            ).pack(side="left", fill="x", expand=True, padx=5, pady=5)

            if len(self.thoughts) > 1:
                ctk.CTkButton(
                    thFrame, text="✕", width=25, height=25,
                    fg_color="transparent", text_color=COLORS["danger"],
                    hover_color=COLORS["danger_bg"],
                    command=lambda t=thought: self.deleteThought(t)
                ).pack(side="right", padx=5)

    def openCalendar(self):
        CalendarWindow(self)

    def selectThought(self, thought):
        self.currentThought = thought
        self.headerTitle.configure(text=self.currentThought)
        self.renderSidebar()
        self.renderTasks()

    def addThought(self):
        newThought = self.thoughtEntry.get().strip()
        if newThought != "":
            if newThought not in self.thoughts:
                self.thoughts.append(newThought)
                self.thoughtEntry.delete(0, "end")
                self.saveState()
                self.selectThought(newThought)

    def deleteThought(self, thought):
        self.thoughts.remove(thought)

        newTasks = []
        for t in self.tasks:
            if "thought" in t:
                if t["thought"] != thought:
                    newTasks.append(t)
            else:
                newTasks.append(t)

        self.tasks = newTasks
        self.saveState()

        if self.currentThought == thought:
            self.selectThought(self.thoughts[0])
        else:
            self.renderSidebar()

    def setFilter(self, mode):
        self.filterMode = mode
        self.renderTasks()

    def sortTasks(self, currentTasks):
        # Веса по каноническим ключам — не зависят от языка
        priorityWeight = {
            "urgent": 0,
            "normal": 1,
            "low": 2,
        }

        def sortKey(t):
            isDone = t["done"]

            isPinned = False
            if "pinned" in t:
                if t["pinned"] == True:
                    isPinned = True

            notPinned = not isPinned

            # Ищем вес приоритета
            if t["priority"] in priorityWeight:
                priority = priorityWeight[t["priority"]]
            else:
                priority = 1

            return (isDone, notPinned, priority, -t["id"])

        currentTasks.sort(key=sortKey)

    def addTask(self):
        text = self.taskEntry.get().strip()
        if text == "":
            self.taskEntry.focus()
            return

        # Переводим локализованный приоритет в канонический ключ
        localizedPriority = self.priorityVar.get()
        canonicalPriority = {
            self.L["priority_urgent"]: "urgent",
            self.L["priority_normal"]: "normal",
            self.L["priority_low"]: "low",
        }.get(localizedPriority, "normal")

        task = {
            "id": self.nextId,
            "text": text,
            "done": False,
            "priority": canonicalPriority,
            "created": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "thought": self.currentThought,
            "pinned": False
        }
        self.tasks.append(task)
        self.nextId += 1
        self.taskEntry.delete(0, "end")
        self.saveState()
        self.renderTasks()

    def toggleTask(self, taskId):
        for t in self.tasks:
            if t["id"] == taskId:
                if t["done"] == True:
                    t["done"] = False
                else:
                    t["done"] = True
                break
        self.saveState()
        self.renderTasks()

    def togglePin(self, taskId):
        for t in self.tasks:
            if t["id"] == taskId:
                if "pinned" in t:
                    if t["pinned"] == True:
                        t["pinned"] = False
                    else:
                        t["pinned"] = True
                else:
                    t["pinned"] = True
                break
        self.saveState()
        self.renderTasks()

    def editTask(self, taskId):
        for t in self.tasks:
            if t["id"] == taskId:
                dialog = EditTaskDialog(self, t["text"])
                if dialog.result != None:
                    t["text"] = dialog.result
                    self.saveState()
                    self.renderTasks()
                break

    def deleteTask(self, taskId):
        newTasks = []
        for t in self.tasks:
            if t["id"] != taskId:
                newTasks.append(t)
        self.tasks = newTasks
        self.saveState()
        self.renderTasks()

    def clearDoneTasks(self):
        newTasks = []
        for t in self.tasks:
            isCurrentThought = False
            if "thought" in t:
                if t["thought"] == self.currentThought:
                    isCurrentThought = True

            if t["done"] == True and isCurrentThought == True:
                continue

            newTasks.append(t)

        self.tasks = newTasks
        self.saveState()
        self.renderTasks()

    def renderTasks(self):
        for widget in self.scrollableFrame.winfo_children():
            widget.destroy()

        currentThoughtTasks = []
        for t in self.tasks:
            if "thought" in t:
                if t["thought"] == self.currentThought:
                    currentThoughtTasks.append(t)
            else:
                if self.currentThought == " ":
                    currentThoughtTasks.append(t)

        self.sortTasks(currentThoughtTasks)

        doneCount = 0
        for t in currentThoughtTasks:
            if t["done"] == True:
                doneCount += 1

        totalTasks = len(currentThoughtTasks)
        counterText = self.L["counter_text"].format(done=doneCount, total=totalTasks)
        self.counterLabel.configure(text=counterText)

        visibleTasks = []
        if self.filterMode == self.L["filter_active"]:
            for t in currentThoughtTasks:
                if t["done"] == False:
                    visibleTasks.append(t)
        elif self.filterMode == self.L["filter_done"]:
            for t in currentThoughtTasks:
                if t["done"] == True:
                    visibleTasks.append(t)
        else:
            visibleTasks = currentThoughtTasks

        if len(visibleTasks) == 0:
            emptyFrame = ctk.CTkFrame(self.scrollableFrame, fg_color="transparent")
            emptyFrame.pack(fill="both", expand=True, pady=60)

            imgPath = os.path.join(os.path.dirname(__file__), "empty.png")
            try:
                if os.path.exists(imgPath):
                    img = Image.open(imgPath)
                    ctkImg = ctk.CTkImage(light_image=img, size=(120, 120))
                    ctk.CTkLabel(emptyFrame, image=ctkImg, text="").pack(pady=(0, 15))
                else:
                    ctk.CTkLabel(emptyFrame, text="🌿", font=ctk.CTkFont(size=60)).pack(pady=(0, 10))
            except Exception:
                pass

            ctk.CTkLabel(
                emptyFrame, text=self.L["empty_title"],
                font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
                text_color=COLORS["text_main"]
            ).pack()

            ctk.CTkLabel(
                emptyFrame, text=self.L["empty_subtitle"],
                font=self.fontMain, text_color=COLORS["text_muted"]
            ).pack()
            return

        for task in visibleTasks:
            self.renderSingleTask(task)

    def renderSingleTask(self, task):
        isPinned = False
        if "pinned" in task:
            if task["pinned"] == True:
                isPinned = True

        taskFrame = ctk.CTkFrame(
            self.scrollableFrame, fg_color=COLORS["surface"],
            corner_radius=10, border_width=1, border_color=COLORS["border"]
        )
        taskFrame.pack(fill="x", padx=10, pady=(0, 8))

        check = ctk.CTkCheckBox(
            taskFrame, text="", width=24, height=24, corner_radius=6,
            fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
            border_color=COLORS["border"],
            command=lambda tid=task["id"]: self.toggleTask(tid)
        )
        if task["done"] == True:
            check.select()
        check.pack(side="left", padx=(15, 5), pady=15)

        ctk.CTkButton(
            taskFrame, text="✕", width=30, height=30, fg_color="transparent",
            text_color=COLORS["danger"], hover_color=COLORS["danger_bg"],
            font=self.fontMain, command=lambda tid=task["id"]: self.deleteTask(tid)
        ).pack(side="right", padx=(2, 15))

        ctk.CTkButton(
            taskFrame, text="✎", width=30, height=30, fg_color="transparent",
            text_color=COLORS["text_muted"], hover_color=COLORS["border"],
            font=self.fontMain, command=lambda tid=task["id"]: self.editTask(tid)
        ).pack(side="right", padx=2)

        if isPinned == True:
            pinIcon = "★"
            pinColor = COLORS["warning"]
        else:
            pinIcon = "☆"
            pinColor = COLORS["text_muted"]

        ctk.CTkButton(
            taskFrame, text=pinIcon, width=30, height=30, fg_color="transparent",
            text_color=pinColor, hover_color=COLORS["warning_bg"],
            font=ctk.CTkFont(size=18),
            command=lambda tid=task["id"]: self.togglePin(tid)
        ).pack(side="right", padx=2)

        # Бейдж приоритета: ключ canonical, отображаем локализованное название
        canonical = task.get("priority", "normal")
        pColors = BADGES.get(canonical, BADGES["normal"])
        localizedLabel = self.L.get("priority_" + canonical, canonical)

        ctk.CTkLabel(
            taskFrame, text=localizedLabel, font=self.fontSmall,
            fg_color=pColors["bg"], text_color=pColors["text"],
            corner_radius=6, width=70, height=24
        ).pack(side="right", padx=(10, 5))

        textFrame = ctk.CTkFrame(taskFrame, fg_color="transparent")
        textFrame.pack(side="left", fill="x", expand=True, padx=5)

        if task["done"] == True:
            lblFont = self.fontStrike
            lblColor = COLORS["text_muted"]
        else:
            lblFont = self.fontMain
            lblColor = COLORS["text_main"]

        ctk.CTkLabel(
            textFrame, text=task["text"], font=lblFont,
            text_color=lblColor, anchor="w", justify="left"
        ).pack(fill="x")

        if "created" in task:
            ctk.CTkLabel(
                textFrame, text=task["created"], font=self.fontSmall,
                text_color=COLORS["text_muted"], anchor="w"
            ).pack(fill="x")
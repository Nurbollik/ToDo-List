import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")

COLORS = {
    "bg": ("#F9FAFB", "#121212"),
    "surface": ("#FFFFFF", "#1E1E1E"),
    "primary": ("#34D399", "#3B82F6"),
    "primary_hover": ("#10B981", "#60A5FA"),
    "text_main": ("#1F2937", "#F3F4F6"),
    "text_muted": ("#9CA3AF", "#9CA3AF"),
    "danger": ("#F87171", "#EF4444"),
    "danger_bg": ("#FEE2E2", "#451A1A"),
    "border": ("#E5E7EB", "#333333"),
    "sidebar_active": ("#ECFDF5", "#172554"),
    "warning": ("#F59E0B", "#F59E0B"),
    "warning_bg": ("#FEF3C7", "#78350F")
}

BADGES = {
    "Срочная": {"bg": ("#FEE2E2", "#451A1A"), "text": ("#EF4444", "#FCA5A5")},
    "Обычная": {"bg": ("#F3F4F6", "#333333"), "text": ("#6B7280", "#D1D5DB")},
    "Низкая": {"bg": ("#D1FAE5", "#064E3B"), "text": ("#059669", "#6EE7B7")}
}

#переводы для интерфейса

LANG_RU = {
    # Общее
    "app_title": "Planterra - Планировщик мыслей и задач",
    "app_logo": "Planterra 🪷",

    # Сайдбар
    "new_thought_placeholder": "Новая мысль...",
    "calendar_btn": "📅 Календарь",

    # Основная область
    "filter_all": "Все",
    "filter_active": "Активные",
    "filter_done": "Выполненные",
    "task_placeholder": "Что нужно сделать?",
    "clear_done_btn": "Очистить выполненные",
    "counter_text": "Выполнено: {done} из {total}",

    # Приоритеты
    "priority_urgent": "Срочная",
    "priority_normal": "Обычная",
    "priority_low": "Низкая",

    # Диалог редактирования
    "edit_dialog_title": "Редактировать задачу",
    "edit_save_btn": "Сохранить",
    "edit_cancel_btn": "Отмена",

    # Пустой список
    "empty_title": "В этой мысли пока пусто",
    "empty_subtitle": "Добавьте свою первую задачу выше",

    # Календарь
    "calendar_title": "Календарь событий",
    "weekdays": ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
    "months": [
        "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
        "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ],

    # Кнопка смены языка
    "lang_btn": "EN",
}

LANG_EN = {
    # General
    "app_title": "Planterra - Thoughts & Tasks Planner",
    "app_logo": "Planterra 🪷",

    # Sidebar
    "new_thought_placeholder": "New thought...",
    "calendar_btn": "📅 Calendar",

    # Main area
    "filter_all": "All",
    "filter_active": "Active",
    "filter_done": "Completed",
    "task_placeholder": "What needs to be done?",
    "clear_done_btn": "Clear completed",
    "counter_text": "Done: {done} of {total}",

    # Priorities
    "priority_urgent": "Urgent",
    "priority_normal": "Normal",
    "priority_low": "Low",

    # Edit dialog
    "edit_dialog_title": "Edit task",
    "edit_save_btn": "Save",
    "edit_cancel_btn": "Cancel",

    # Empty state
    "empty_title": "Nothing here yet",
    "empty_subtitle": "Add your first task above",

    # Calendar
    "calendar_title": "Event Calendar",
    "weekdays": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "months": [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ],

    # Language button
    "lang_btn": "RU",
}

ALL_LANGS = {
    "ru": LANG_RU,
    "en": LANG_EN,
}
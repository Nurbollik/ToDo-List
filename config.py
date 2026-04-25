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

# Ключи — канонические: "urgent", "normal", "low"
BADGES = {
    "urgent": {"bg": ("#FEE2E2", "#451A1A"), "text": ("#EF4444", "#FCA5A5")},
    "normal": {"bg": ("#F3F4F6", "#333333"), "text": ("#6B7280", "#D1D5DB")},
    "low":    {"bg": ("#D1FAE5", "#064E3B"), "text": ("#059669", "#6EE7B7")}
}

# Порядок переключения языков и их отображаемые названия на кнопке
LANG_ORDER = ["ru", "en", "ky", "es", "zh"]
LANG_DISPLAY = {"ru": "RU", "en": "EN", "ky": "KY", "es": "ES", "zh": "中文"}

# Таблица миграции старых локализованных приоритетов → канонический ключ
PRIORITY_MIGRATION = {
    # Русский
    "Срочная": "urgent", "Обычная": "normal", "Низкая": "low",
    # Английский
    "Urgent": "urgent", "Normal": "normal", "Low": "low",
    # Кыргызский
    "Шашылыш": "urgent", "Кадимки": "normal", "Төмөн": "low",
    # Испанский
    "Urgente": "urgent", "Baja": "low",
    # Китайский
    "紧急": "urgent", "普通": "normal", "低": "low",
    # Уже канонические
    "urgent": "urgent", "normal": "normal", "low": "low",
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

    # Приоритеты (значения для отображения, ключи — canonical)
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
}

LANG_EN = {

    "app_title": "Planterra - Thoughts & Tasks Planner",
    "app_logo": "Planterra 🪷",

 
    "new_thought_placeholder": "New thought...",
    "calendar_btn": "📅 Calendar",

  
    "filter_all": "All",
    "filter_active": "Active",
    "filter_done": "Completed",
    "task_placeholder": "What needs to be done?",
    "clear_done_btn": "Clear completed",
    "counter_text": "Done: {done} of {total}",


    "priority_urgent": "Urgent",
    "priority_normal": "Normal",
    "priority_low": "Low",

    "edit_dialog_title": "Edit task",
    "edit_save_btn": "Save",
    "edit_cancel_btn": "Cancel",


    "empty_title": "Nothing here yet",
    "empty_subtitle": "Add your first task above",


    "calendar_title": "Event Calendar",
    "weekdays": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "months": [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ],
}

LANG_KY = {

    "app_title": "Planterra - Ой жана тапшырма пландоочусу",
    "app_logo": "Planterra 🪷",

    "new_thought_placeholder": "Жаңы ой...",
    "calendar_btn": "📅 Жылнаама",

    "filter_all": "Баары",
    "filter_active": "Активдүү",
    "filter_done": "Аткарылган",
    "task_placeholder": "Эмне кылуу керек?",
    "clear_done_btn": "Аткарылгандарды тазалоо",
    "counter_text": "Аткарылды: {done} / {total}",

    "priority_urgent": "Шашылыш",
    "priority_normal": "Кадимки",
    "priority_low": "Төмөн",

    "edit_dialog_title": "Тапшырманы өзгөртүү",
    "edit_save_btn": "Сактоо",
    "edit_cancel_btn": "Жокко чыгаруу",

    "empty_title": "Бул ойдо азырынча эч нерсе жок",
    "empty_subtitle": "Биринчи тапшырмаңызды жогорудан кошуңуз",

    "calendar_title": "Иш-чаралар жылнаамасы",
    "weekdays": ["Дш", "Шш", "Шр", "Бш", "Жм", "Иш", "Жк"],
    "months": [
        "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
        "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ],
}

LANG_ES = {
    "app_title": "Planterra - Planificador de pensamientos y tareas",
    "app_logo": "Planterra 🪷",


    "new_thought_placeholder": "Nuevo pensamiento...",
    "calendar_btn": "📅 Calendario",

    
    "filter_all": "Todos",
    "filter_active": "Activos",
    "filter_done": "Completados",
    "task_placeholder": "¿Qué hay que hacer?",
    "clear_done_btn": "Limpiar completados",
    "counter_text": "Completado: {done} de {total}",

    "priority_urgent": "Urgente",
    "priority_normal": "Normal",
    "priority_low": "Baja",

    "edit_dialog_title": "Editar tarea",
    "edit_save_btn": "Guardar",
    "edit_cancel_btn": "Cancelar",

  
    "empty_title": "Aún no hay nada aquí",
    "empty_subtitle": "Añade tu primera tarea arriba",

   
    "calendar_title": "Calendario de eventos",
    "weekdays": ["Lu", "Ma", "Mi", "Ju", "Vi", "Sá", "Do"],
    "months": [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ],
}

LANG_ZH = {
   
    "app_title": "Planterra - 想法与任务规划器",
    "app_logo": "Planterra 🪷",

   
    "new_thought_placeholder": "新想法...",
    "calendar_btn": "📅 日历",

    "filter_all": "全部",
    "filter_active": "进行中",
    "filter_done": "已完成",
    "task_placeholder": "需要做什么？",
    "clear_done_btn": "清除已完成",
    "counter_text": "已完成：{done} / {total}",

    "priority_urgent": "紧急",
    "priority_normal": "普通",
    "priority_low": "低",

    "edit_dialog_title": "编辑任务",
    "edit_save_btn": "保存",
    "edit_cancel_btn": "取消",

  
    "empty_title": "这里还没有内容",
    "empty_subtitle": "在上方添加您的第一个任务",

    "calendar_title": "活动日历",
    "weekdays": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
    "months": [
        "一月", "二月", "三月", "四月", "五月", "六月",
        "七月", "八月", "九月", "十月", "十一月", "十二月"
    ],
}

ALL_LANGS = {
    "ru": LANG_RU,
    "en": LANG_EN,
    "ky": LANG_KY,
    "es": LANG_ES,
    "zh": LANG_ZH,
}
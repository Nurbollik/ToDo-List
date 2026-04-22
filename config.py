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
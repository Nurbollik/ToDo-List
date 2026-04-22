import os

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
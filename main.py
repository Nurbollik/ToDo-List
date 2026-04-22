import customtkinter as ctk
from ui import TodoApp

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = TodoApp()
    app.mainloop()
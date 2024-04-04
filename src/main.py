# main.py

import customtkinter
import ui
from ui import LoginRegisterUI
from ui import MainWindowUI
import user_database as db
import auth
import game_logic as gl

if __name__== "__main__":
    db.create_users_table()
    db.create_characters_table()
    root = customtkinter.CTk()
    app_ui = ui.LoginRegisterUI(root)
    root.mainloop()
"""
Module: ui.py

Description:
    This module manages the application GUI by maintaining a root window and creating or destroying
    frames within that window as required for different UI displays. 

Dependencies:
    - tkinter: to display messages and some GUI displays
    - customtkinter: primary GUI management import.
    - auth.py: Authentication module for user management.
    - game_logic.py: Business module containing all D&D logic and functions.
    - random: generates random numbers to simmulate rolling dice.
    - user_database.py: Database module used to manage all database-related functionality.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter
import auth
import game_logic as gl
import user_database as db
import random

class LoginRegisterUI:
    def __init__(self, root):
        self.root = root
        self.initialize_ui()

    def initialize_ui(self):
        self.root.geometry("1280x720")
        self.root.title("RPG Character App")
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.open_login_frame()

    def open_login_frame(self):
        # Destroy existing frames
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = customtkinter.CTkFrame(master=self.root)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        header_frame = customtkinter.CTkFrame(master=main_frame)
        header_frame.pack(side="top", fill="x")

        body_frame = customtkinter.CTkFrame(master=main_frame)
        body_frame.pack(fill="both", expand=True)

        # Header
        customtkinter.CTkLabel(master=header_frame, text="RPG Character App", font=("Impact", 24)).pack(pady=(10, 0), padx=10)
        customtkinter.CTkLabel(master=header_frame, text="Login", font=("Roboto", 18)).pack(fill="both", expand=True, pady=(0, 10), padx=10)

        # Body
        self.inner_frame = customtkinter.CTkScrollableFrame(master=body_frame)
        self.inner_frame.pack(fill="both", expand=True)

        login_frame = customtkinter.CTkFrame(self.inner_frame, border_width=2)
        login_frame.pack(pady=10)

        self.entry_username = customtkinter.CTkEntry(master=login_frame, placeholder_text="Username")
        self.entry_username.pack(pady=12, padx=10)

        self.entry_password = customtkinter.CTkEntry(master=login_frame, placeholder_text="Password", show="*")
        self.entry_password.pack(pady=12, padx=10)

        button_login = customtkinter.CTkButton(master=login_frame, text="Login", command=self.attempt_login)
        button_login.pack(pady=12, padx=10)

        button_register = customtkinter.CTkButton(master=login_frame, text="Register", command=self.open_register_frame)
        button_register.pack(pady=12, padx=10)

    def attempt_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        success, user_object, message = auth.login(username, password)
        if success:
            print(message)
            self.current_user = user_object
            self.current_user.load_characters()
            main_ui = MainWindowUI(self.root, self.open_login_frame, self.current_user)
            main_ui.open_main_window()
        else:
            print(message)

    def open_register_frame(self):
        # Destroy existing frames
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create frames
        main_frame = customtkinter.CTkFrame(master=self.root)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        header_frame = customtkinter.CTkFrame(master=main_frame)
        header_frame.pack(side="top", fill="x")

        body_frame = customtkinter.CTkFrame(master=main_frame)
        body_frame.pack(fill="both", expand=True)

        # Header
        label = customtkinter.CTkLabel(master=header_frame, text="RPG Character App", font=("Impact", 24))
        label.pack(pady=(10, 0), padx=10)

        label = customtkinter.CTkLabel(master=header_frame, text="Register New Account", font=("Roboto", 18))
        label.pack(fill="both", expand=True, pady=(0, 10), padx=10)

        # Create a scrollableFrame within the body_frame
        self.inner_frame = customtkinter.CTkScrollableFrame(master=body_frame)
        self.inner_frame.pack(fill="both", expand=True)

        # Create a frame for login
        register_frame = customtkinter.CTkFrame(self.inner_frame, border_width=2)
        register_frame.pack(pady=10)

        entry_username = customtkinter.CTkEntry(master=register_frame, placeholder_text="Username")
        entry_username.pack(pady=12, padx=10)

        entry_password = customtkinter.CTkEntry(master=register_frame, placeholder_text="Password", show="*")
        entry_password.pack(pady=12, padx=10)

        entry_password_repeat = customtkinter.CTkEntry(master=register_frame, placeholder_text="Repeat password", show="*")
        entry_password_repeat.pack(pady=12, padx=10)

        entry_email = customtkinter.CTkEntry(master=register_frame, placeholder_text="Email")
        entry_email.pack(pady=12, padx=10)

        button_register = customtkinter.CTkButton(
            master=register_frame,
            text="Register",
            command=lambda: auth.register(
                entry_username.get(),
                entry_password.get(),
                entry_password_repeat.get(),
                entry_email.get(),
                self.open_login_frame
            )
        )
        button_register.pack(pady=(20, 12), padx=10)
        back_button = customtkinter.CTkButton(master=register_frame, text="Back", command=self.open_login_frame)
        back_button.pack(pady=10)
    
class MainWindowUI:
    def __init__(self, root, on_logout_callback, current_user=None):
        self.root = root
        self.current_user = current_user
        self.on_logout_callback = on_logout_callback
        self.class_level_subclass_rows = []
        self.class_selections = []
        self.expertise_vars = {}
        self.skill_buttons = {}

    def set_current_user(self, username):
        self.current_user = username 

    def open_main_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.main_frame = customtkinter.CTkFrame(master=self.root)
        self.main_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.header_frame = customtkinter.CTkFrame(master=self.main_frame)
        self.header_frame.pack(side="top", fill="x")
        self.body_frame = customtkinter.CTkFrame(master=self.main_frame)
        self.body_frame.pack(fill="both", expand=True)

        # Header
        label = customtkinter.CTkLabel(master=self.header_frame, text="RPG Character App", font=("Impact", 24))
        label.pack(pady=(10, 0), padx=10)
        label = customtkinter.CTkLabel(master=self.header_frame, text="Main Menu", font=("Roboto", 18))
        label.pack(fill="both", expand=True, pady=(0, 10), padx=10)

        # Scrollable
        self.inner_frame = customtkinter.CTkScrollableFrame(master=self.body_frame)
        self.inner_frame.pack(fill="both", expand=True)
        self.menu_frame = customtkinter.CTkFrame(self.inner_frame, border_width=2)
        self.menu_frame.pack(pady=10, padx=10)

        # Admin Stuff
        if self.current_user.is_admin:
            self.show_admin_button()

        # Menu Buttons
        character_creation_button = customtkinter.CTkButton(master=self.menu_frame, text="Character Creation", command=self.open_character_creation_frame)
        character_creation_button.pack(pady=12, padx=10)
        dice_roller_button = customtkinter.CTkButton(master=self.menu_frame, text="Dice Roller", command=self.open_dice_roller_frame)
        dice_roller_button.pack(pady=12, padx=10)
        character_lists_button = customtkinter.CTkButton(master=self.menu_frame, text="Character Lists", command=self.open_character_lists_frame)
        character_lists_button.pack(pady=12, padx=10)
        logout_button = customtkinter.CTkButton(master=self.menu_frame, text="Logout", command=self.logout)
        logout_button.pack(pady=12, padx=10)

    def show_admin_button(self):
        self.admin_button = customtkinter.CTkButton(
            master=self.inner_frame,
            text="Admin Panel",
            command=self.open_admin_panel
        )
        self.admin_button.pack(pady=10)

    def open_admin_panel(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_ui_instance = MainWindowUI(self.root, self.on_logout_callback, self.current_user)
        admin_ui = AdminUI(self.root, self.current_user, self.open_main_window, self)
        admin_ui.initialize_ui()
        
    def open_character_creation_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.main_frame = customtkinter.CTkFrame(master=self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.header_frame = customtkinter.CTkFrame(master=self.main_frame)
        self.header_frame.grid(row=0, column=0, sticky="ew")

        self.body_frame = customtkinter.CTkFrame(master=self.main_frame, fg_color="transparent")
        self.body_frame.grid(row=1, column=0, sticky="nsew")
        self.body_frame.grid_columnconfigure(1, weight=1)
        self.body_frame.grid_rowconfigure(1, weight=1)
        
        self.footer_frame = customtkinter.CTkFrame(master=self.main_frame, fg_color="transparent")
        self.footer_frame.grid(row=2, column=0, sticky="ew")

        self.upper_scrollable = customtkinter.CTkScrollableFrame(master=self.body_frame, fg_color="transparent")
        self.upper_scrollable.grid(row=0, column=1, sticky="nsew", padx=10, pady=(10, 0))
        self.lower_scrollable = customtkinter.CTkScrollableFrame(master=self.body_frame, fg_color="transparent")
        self.lower_scrollable.grid(row=1, column=1, sticky="nsew", padx=10, pady=(0, 10))

        self.character_creation_frame = customtkinter.CTkFrame(master=self.upper_scrollable, fg_color="transparent")
        self.character_creation_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.skills_frame = customtkinter.CTkFrame(master=self.body_frame)
        self.skills_frame.grid(row=0, column=0, rowspan=2, sticky="W", padx=10, pady=(20, 10))
        self.ability_frame = customtkinter.CTkFrame(master=self.lower_scrollable, fg_color="transparent")
        self.ability_frame.grid(row=1, column=0, columnspan=4, sticky="nsw")
        self.tooltip_frame = customtkinter.CTkFrame(master=self.lower_scrollable, fg_color="transparent")
        self.tooltip_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.feats_frame = customtkinter.CTkFrame(master=self.lower_scrollable, fg_color="transparent")
        self.feats_frame.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
        self.button_frame = customtkinter.CTkFrame(master=self.lower_scrollable)
        self.button_frame.grid(row=2, column=2, sticky="ew", padx=30, pady=(20, 10))
        self.selection_frame = customtkinter.CTkFrame(master=self.character_creation_frame)
        self.selection_frame.pack(expand=True, padx=10, pady=10)

        label = customtkinter.CTkLabel(master=self.header_frame, text="RPG Character App", font=("Impact", 24))
        label.pack(pady=(10, 0), padx=10)
        label = customtkinter.CTkLabel(master=self.header_frame, text="Character Creation", font=("Roboto", 18))
        label.pack(pady=(0, 10), padx=10)

        # Row 1 Name, Race, Background
        character_name_label = customtkinter.CTkLabel(master=self.selection_frame, text="Character Name:") 
        character_name_label.grid(row=0, column=0, padx=4, pady=10)
        self.character_name_entry = customtkinter.CTkEntry(master=self.selection_frame, placeholder_text="Aeva Wheeler")
        self.character_name_entry.grid(row=0, column=1, padx=4, pady=10)

        race_label = customtkinter.CTkLabel(master=self.selection_frame, text="Select Race:")
        race_label.grid(row=0, column=2, pady=10)
        race_options = gl.get_race_options()
        self.race_combobox = ttk.Combobox(master=self.selection_frame, values=race_options, state="readonly")
        self.race_combobox.grid(row=0, column=3, padx=5, pady=10)

        background_label = customtkinter.CTkLabel(master=self.selection_frame, text="Select Background:")
        background_label.grid(row=0, column=4, padx=4, pady=10)
        background_options = gl.get_background_options()
        self.background_combobox = ttk.Combobox(master=self.selection_frame, values=background_options, state="readonly")
        self.background_combobox.grid(row=0, column=5, padx=5, pady=10)
        
        # Row 2 Class, Levels taken in said class, subclass, "Add Multiclass" Button
        self.class_label = customtkinter.CTkLabel(master=self.selection_frame, text="Select Starting Class:")
        self.class_label.grid(row=1, column=0, pady=10)
        self.class_options = gl.get_class_options()
        self.class_combobox = ttk.Combobox(master=self.selection_frame, values=self.class_options, state="readonly")
        self.class_combobox.grid(row=1, column=1, padx=5, pady=10)

        self.levels_label = customtkinter.CTkLabel(master=self.selection_frame, text="Levels:")
        self.levels_label.grid(row=1, column=2, pady=10)
        self.levels_combobox = ttk.Combobox(master=self.selection_frame, values=list(range(1, 21)), state="readonly")
        self.levels_combobox.grid(row=1, column=3, padx=5, pady=10)

        self.subclass_label = customtkinter.CTkLabel(master=self.selection_frame, text="Select Subclass:")
        self.subclass_label.grid(row=1, column=4, pady=10)
        self.subclass_options = gl.get_subclass_options()
        self.subclass_combobox = ttk.Combobox(master=self.selection_frame, values=[], state="readonly")  # Initially empty until user is lvl 3
        self.subclass_combobox.grid(row=1, column=5, padx=5, pady=10)

        add_class_button = customtkinter.CTkButton(master=self.selection_frame, text="Add Multiclass", command=self.add_multiclass)
        add_class_button.grid(row=1, column=6, padx=5, pady=10)

        # setting defaults to Aeva
        self.race_combobox.set("Human")
        self.class_combobox.set("Rogue")
        self.levels_combobox.set(1)
        self.background_combobox.set("Spy")

        # Bind to key release event to handle the input and prevent user from editing the value
        def handle_keyrelease_event(event):
            # Check if the Combobox is focused
            if self.race_combobox == self.selection_frame.focus_get():
                # Get the current text in the Combobox
                typed = self.race_combobox.get()
                
                if typed:  # If something is typed
                    # Find the closest match in the options
                    match = next((s for s in race_options if s.lower().startswith(typed.lower())), None)
                    if match:
                        self.race_combobox.set(match)  # Set the Combobox value to the matched option
                    return "break"  # Stop further propagation of the key release event

                self.race_combobox.set(typed)
        
        self.race_combobox.bind('<KeyRelease>', handle_keyrelease_event)
        self.race_combobox.bind("<<ComboboxSelected>>", self.on_race_selection_change)
        self.background_combobox.bind("<<ComboboxSelected>>", self.on_background_selection_change)
        self.class_combobox.bind("<<ComboboxSelected>>", self.on_combobox_selected)
        self.levels_combobox.bind("<<ComboboxSelected>>", self.on_combobox_selected)
        self.subclass_combobox.bind("<<ComboboxSelected>>", self.update_subclass_description)
        
        # Skills
        skills_label = customtkinter.CTkLabel(master=self.skills_frame, text="Select Skills")
        skills_label.pack(padx=10, pady=10)
        self.selected_skills = []
        def update_selected_skills(skill_index, value):
            if value == 1:
                self.selected_skills.append(gl.get_skills()[skill_index])
                for skill in self.selected_skills:
                    self.change_description_text(self.tooltip, gl.get_skill_description(skill))
                    print(" ", skill)
            else:
                selected_skills.remove(gl.get_skills()[skill_index])
                for skill in self.selected_skills:
                    print(" ", skill)

        skills = []
        for index, skill in enumerate(gl.get_skills()):
            var = tk.IntVar()
            checkbox = customtkinter.CTkCheckBox(master=self.skills_frame, text=skill, variable=var)
            checkbox.configure(border_width=1)
            checkbox.pack(anchor="w")
            checkbox.bind("<Button-1>", lambda event, i=index, v=var: update_selected_skills(i, v.get()))
            skills.append(var)

        # Ability Scores
        self.ability_labels = []
        ability_scores = gl.get_ability_scores()

        for index, ability in enumerate(ability_scores):
            label = customtkinter.CTkLabel(master=self.ability_frame, text=ability)
            label.grid(row=0, column=index, padx=5, pady=5)
            self.ability_labels.append(label)

        self.ability_entries = []

        for index, ability in enumerate(ability_scores):
            # Creating a frame for each set of entry and buttons
            self.entry_frame = customtkinter.CTkFrame(master=self.ability_frame, border_width=0)
            self.entry_frame.grid(row=1, column=index, padx=5, pady=5, sticky="nsew")

            entry_scores = customtkinter.CTkEntry(master=self.entry_frame, width=130, border_width=0)
            entry_scores.insert(0, "8")
            entry_scores.grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky="nsew")
            self.ability_entries.append(entry_scores)

            # Ability Score adjustment buttons
            increase_button = customtkinter.CTkButton(master=self.entry_frame, text="▲", command=lambda i=index: self.increase_ability_score(i))
            decrease_button = customtkinter.CTkButton(master=self.entry_frame, text="▼", command=lambda i=index: self.decrease_ability_score(i))
            increase_button.configure(fg_color="transparent", height=1, width=1)
            decrease_button.configure(fg_color="transparent", height=1, width=1)
            increase_button.grid(row=0, column=2, sticky="nsew", padx=2, pady=0)
            decrease_button.grid(row=1, column=2, sticky="nsew", padx=2, pady=0)

        # Create Tooltip Desctiptions / cheatsheet
        tooltip_label = customtkinter.CTkLabel(self.tooltip_frame, text="Description", font=("Impact", 16))
        tooltip_label.pack(padx=10, pady=(10, 0))

        self.decription_text = "As you build your character keen an eye over here for more information. Select stuff to see what they do!\n\nSelect a Race, Background, and Class. If you are starting at level 3 or higher, select a Subclass as well."
        self.tooltip = customtkinter.CTkLabel(self.tooltip_frame, width=500, height=100, wraplength=500, text=self.decription_text)
        self.tooltip.pack(padx=10, pady=(0, 10))  

        # Feats
        feat_label1 = customtkinter.CTkLabel(self.feats_frame, text="Feats:", font=("roboto", 14))
        feat_label1.grid(row=0, column=0, padx=10, pady=(10, 0))
        feat_label2 = customtkinter.CTkLabel(self.feats_frame, text="(lvls 4, 8, 12, 16, and 19)", font=("Roboto", 12))
        feat_label2.grid(row=0, column=1, padx=10, pady=(10, 0))

        self.feats = gl.get_feats()
        self.feat_combobox = ttk.Combobox(self.feats_frame, values=self.feats, state="readonly")
        self.feat_combobox.grid(row=2, column=0, padx=10, pady=10)

        self.feat_selections = []
        add_feat_combobox_button = customtkinter.CTkButton(self.feats_frame, text="Add Another Feat", command=self.add_feat)
        add_feat_combobox_button.grid(row=2, column=1, padx=(5, 10), pady=10)

        self.feat_combobox.bind("<<ComboboxSelected>>", self.on_feat_combobox_selected)

        # Create Buttons: Roll Stats, Save Char, Generate Char
        roll_stats_button = customtkinter.CTkButton(self.button_frame, text="Roll Stats",command=self.roll_stats_and_reorder)
        roll_stats_button.pack(padx=(5, 10), pady=(20, 5))

        save_character_button = customtkinter.CTkButton(self.button_frame, text="Save Character", command=self.create_character)
        save_character_button.pack(padx=10, pady=5)

        auto_generate_button = customtkinter.CTkButton(self.button_frame, text="You Do It", command=self.auto_generate_character)
        auto_generate_button.pack(padx=10, pady=5)

        back_button = customtkinter.CTkButton(master=self.footer_frame, text="Back", command=self.open_main_window)
        back_button.pack(pady=10)

    def open_dice_roller_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.main_frame = customtkinter.CTkFrame(master=self.root)
        self.main_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.header_frame = customtkinter.CTkFrame(master=self.main_frame)
        self.header_frame.pack(side="top", fill="x")
        self.body_frame = customtkinter.CTkFrame(master=self.main_frame)
        self.body_frame.pack(side="top", fill="both", expand=True)
        self.footer_frame = customtkinter.CTkFrame(master=self.main_frame)
        self.footer_frame.pack(side="bottom", fill="x")

        # Header
        label = customtkinter.CTkLabel(master=self.header_frame, text="RPG Character App", font=("Impact", 24))
        label.pack(pady=(10, 0), padx=10)
        label = customtkinter.CTkLabel(master=self.header_frame, text="Dice Roller", font=("Roboto", 18))
        label.pack(fill="both", expand=True, pady=(0, 10), padx=10)

        # Scrollable
        self.inner_frame = customtkinter.CTkScrollableFrame(master=self.body_frame)
        self.inner_frame.pack(fill="both", expand=True)
        self.sub_inner_frame = customtkinter.CTkFrame(master=self.inner_frame)
        self.sub_inner_frame.pack(pady=50, padx=10)

        # Dice roller
        dice_roller_frame = customtkinter.CTkFrame(self.sub_inner_frame, fg_color="transparent")
        dice_roller_frame.grid(row=0, column=0, sticky="n")

        num_range = [str(i) for i in range(1,21)]
        self.num_dice_combobox = ttk.Combobox(master=dice_roller_frame, values=num_range, width=5)
        self.num_dice_combobox.set("1")  # Default value
        self.num_dice_combobox.pack(pady=5)

        roll_d20_button = customtkinter.CTkButton(master=dice_roller_frame, text="Roll d20", 
                                                command=lambda: self.roll_dice(20))
        roll_d20_button.pack(pady=5)
        roll_d12_button = customtkinter.CTkButton(master=dice_roller_frame, text="Roll d12", 
                                                command=lambda: self.roll_dice(12))
        roll_d12_button.pack(pady=5)
        roll_d10_button = customtkinter.CTkButton(master=dice_roller_frame, text="Roll d10", 
                                                command=lambda: self.roll_dice(10))
        roll_d10_button.pack(pady=5)
        roll_d8_button = customtkinter.CTkButton(master=dice_roller_frame, text="Roll d8", 
                                                command=lambda: self.roll_dice(8))
        roll_d8_button.pack(pady=5)
        roll_d6_button = customtkinter.CTkButton(master=dice_roller_frame, text="Roll d6", 
                                                command=lambda: self.roll_dice(6))
        roll_d6_button.pack(pady=5)
        roll_d4_button = customtkinter.CTkButton(master=dice_roller_frame, text="Roll d4", 
                                                command=lambda: self.roll_dice(4))
        roll_d4_button.pack(pady=5)
        flip_coin_button = customtkinter.CTkButton(master=dice_roller_frame, text="Flip Coin 1:H, 2:T", 
                                                command=lambda: self.roll_dice(2))
        flip_coin_button.pack(pady=5)
        roll_percentage_button = customtkinter.CTkButton(master=dice_roller_frame, text="Roll Percentage", 
                                                        command=lambda: self.roll_dice(100))
        roll_percentage_button.pack(pady=5)

        # Frame for dice roll results and total
        self.results_frame = customtkinter.CTkFrame(self.sub_inner_frame, fg_color="transparent")
        self.results_frame.grid(row=0, column=1, padx=10, sticky="n")

        # Space to show dice results
        result_label = customtkinter.CTkLabel(master=self.results_frame, text="Dice Roll Results:", font=("Roboto", 16))
        result_label.pack(pady=10)
        self.dice_result_text = customtkinter.CTkTextbox(master=self.results_frame, height=100, width=300)
        self.dice_result_text.pack()

        total_label = customtkinter.CTkLabel(master=self.results_frame, text="Total:")
        total_label.pack(pady=10)
        self.total_text = customtkinter.CTkTextbox(master=self.results_frame, height=1, width=60)
        self.total_text.pack(pady=10)

        clear_button = customtkinter.CTkButton(master=self.results_frame, text="Clear", command=self.clear_totals)
        clear_button.pack(pady=10)
        back_button = customtkinter.CTkButton(master=self.footer_frame, text="Back", command=self.open_main_window)
        back_button.pack(pady=10)

    def open_character_lists_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.current_user.load_characters()

        self.main_frame = customtkinter.CTkFrame(master=self.root)
        self.main_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.header_frame = customtkinter.CTkFrame(master=self.main_frame)
        self.header_frame.pack(side="top", fill="x")
        self.body_frame = customtkinter.CTkFrame(master=self.main_frame, bg_color="transparent", fg_color="transparent")
        self.body_frame.pack(side="top", fill="both", expand=True)
        self.footer_frame = customtkinter.CTkFrame(master=self.main_frame)
        self.footer_frame.pack(side="bottom", fill="x")

        # Header
        label = customtkinter.CTkLabel(master=self.header_frame, text="RPG Character App", font=("Impact", 24))
        label.pack(pady=(10, 0), padx=10)
        label = customtkinter.CTkLabel(master=self.header_frame, text="Character List", font=("Roboto", 18))
        label.pack(fill="both", expand=True, pady=(0, 10), padx=10)

        if hasattr(self, 'current_user') and self.current_user:
            character_list = self.current_user.get_characters()
        else:
            print("No current user set or user has no characters.")
            character_list = []

        self.create_character_button = customtkinter.CTkButton(master=self.body_frame, text="New Character", command=self.open_character_creation_frame)
        self.create_character_button.pack(padx=10, pady=10)
        self.character_list_frame = customtkinter.CTkScrollableFrame(master=self.body_frame, bg_color="transparent")
        self.character_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create buttons for each character
        for idx, character in enumerate(character_list):
            character_button = customtkinter.CTkButton(
                master=self.character_list_frame,
                text=(character),
                fg_color="transparent",
                bg_color="transparent",
                width=800,
                height=60,
                command=lambda c=character: self.open_character_sheet(c))
            character_button.grid(row=idx, column=0, sticky="w", pady=5)

            delete_character_button = customtkinter.CTkButton(
                master=self.character_list_frame, 
                text="Delete Character", 
                hover_color="red",
                command=lambda c=character: self.delete_character(c.character_id))
            delete_character_button.grid(row=idx, column=1, sticky="e", padx=50, pady=5)

        back_button = customtkinter.CTkButton(master=self.footer_frame, text="Back", command=self.open_main_window)
        back_button.pack(padx=10, pady=10)

    def open_character_sheet(self, character):
        self.character_name = character.name
        self.selected_race = character.race
        self.ability_scores = character.ability_scores
        self.selected_skills = character.skill_proficiencies
        self.is_jack_of_all_trades = character.is_jack_of_all_trades
        self.selected_background = character.background
        self.selected_feats = character.selected_feats

        class_objects = [(gl.get_class_by_name(class_name), level, None) for class_name, level in character.classes.items()]

        # Prepare character data for saving
        self.character_data = {
            'name': self.character_name,
            'race': self.selected_race,
            'background': self.selected_background,
            'ability_scores': self.ability_scores,
            'feats': self.selected_feats,
            'skill_proficiencies': self.selected_skills,  # Make sure this is set correctly
            'is_jack_of_all_trades': self.is_jack_of_all_trades,
            'classes': {cls.name: level for cls, level, _ in class_objects}
        }
    
        self.create_character_sheet(self.character_data)

    def delete_character(self, character_id):
        response = messagebox.askyesno("Delete Character", "Are you sure you want to delete this character? This action cannot be undone.")
        if response:
            self.current_user.remove_character(character_id)
            db.delete_character_from_db(character_id)
            self.open_character_lists_frame() 

    def logout(self):
        self.on_logout_callback()

    def display_dice_results(self, results):
        self.dice_result_text.delete("1.0", "end")
        self.total_text.delete("1.0", "end")
        for result in results:
            self.dice_result_text.insert("end", f"{result}\n")
        self.total_text.insert("1.0", f"{sum(results)}\n")
        self.dice_result_text.see("end")

    def clear_totals(self):
        self.dice_result_text.delete("1.0", "end")
        self.total_text.delete("1.0", "end")

    def on_combobox_selected(self, event):
        self.update_subclass_options(self.class_combobox, self.levels_combobox, self.subclass_combobox)
        self.update_class_description()
        self.starter_class = self.class_combobox.get()

    def update_subclass_options(self, class_combobox, levels_combobox, subclass_combobox):
        selected_class = class_combobox.get()
        selected_level = levels_combobox.get()

        if selected_class and selected_level and int(selected_level) >= 3:
            new_subclass_options = gl.get_subclass_options().get(selected_class, [])
            subclass_combobox['values'] = new_subclass_options
            subclass_combobox.set('')
        else:
            subclass_combobox.set('')
            subclass_combobox['values'] = []

    # Dynamically adds multiclass comboboxes on button press during character creation.
    def add_multiclass(self, event=None):
        new_row = len(self.class_selections) + 2

        new_class_combobox = ttk.Combobox(master=self.selection_frame, values=gl.get_class_options(), state="readonly")
        new_class_combobox.grid(row=new_row, column=1, padx=5, pady=10)
        new_levels_combobox = ttk.Combobox(master=self.selection_frame, values=list(range(1, 21)), state="readonly")
        new_levels_combobox.grid(row=new_row, column=3, padx=5, pady=10)
        new_subclass_combobox = ttk.Combobox(master=self.selection_frame, values=[], state="readonly")
        new_subclass_combobox.grid(row=new_row, column=5, padx=5, pady=10)

        new_class_combobox.bind("<<ComboboxSelected>>", lambda event, c=new_class_combobox, l=new_levels_combobox, s=new_subclass_combobox: self.update_subclass_options(c, l, s))
        new_levels_combobox.bind("<<ComboboxSelected>>", lambda event, c=new_class_combobox, l=new_levels_combobox, s=new_subclass_combobox: self.update_subclass_options(c, l, s))

        remove_button = customtkinter.CTkButton(
            master=self.selection_frame,
            text="Remove",
            hover_color="red",
            command=lambda: self.remove_multiclass(new_row, new_class_combobox, new_levels_combobox, new_subclass_combobox, remove_button))
        remove_button.grid(row=new_row, column=6, padx=5, pady=10)

        self.class_selections.append((new_class_combobox, new_levels_combobox, new_subclass_combobox, remove_button))

    def remove_multiclass(self, row, class_combobox, levels_combobox, subclass_combobox, remove_button):
        class_combobox.destroy()
        levels_combobox.destroy()
        subclass_combobox.destroy()
        remove_button.destroy()

        self.class_selections = [s for s in self.class_selections if s != (class_combobox, levels_combobox, subclass_combobox, remove_button)]

    # Helpers for Ability Score increase/decrease button
    def increase_ability_score(self, index):
        current_value = int(self.ability_entries[index].get())
        self.ability_entries[index].delete(0, "end")
        self.ability_entries[index].insert(0, str(current_value + 1))

    def decrease_ability_score(self, index):
        current_value = int(self.ability_entries[index].get())
        self.ability_entries[index].delete(0, "end")
        self.ability_entries[index].insert(0, str(current_value - 1))

    # Handles calling functions responsible for rolling 4d6 and throws out the lowest value, 
    # sums up the rest, and places the total in recommended spots based off class selection.
    def roll_stats_and_reorder(self):
        selected_class_name = self.class_combobox.get()
        selected_class = gl.get_class_by_name(selected_class_name)
        
        if selected_class:
            new_scores = gl.roll_stats(selected_class)
            for entry, score in zip(self.ability_entries, new_scores):
                entry.delete(0, "end")
                entry.insert(0, str(score))

    def on_class_combobox_selected(self, event):
        self.update_class_description()
        self.update_subclass_options(self.class_combobox, self.levels_combobox, self.subclass_combobox)

    def on_subclass_combobox_selected(self, event):
        self.update_subclass_description()

    def on_feat_combobox_selected(self, event):
        self.selected_feat = self.feat_combobox.get()
        self.description = gl.get_feat_descriptions(self.selected_feat)
        self.change_description_text(self.tooltip, self.description)
    
    def update_class_description(self, event=None):
        selected_class_name = self.class_combobox.get()
        selected_class = gl.DndClass.get_class_by_name(selected_class_name)
        if selected_class:
            equipment_str = ', '.join([', '.join(item) if isinstance(item, tuple) else item for item in selected_class.equipment])
            description = f"{selected_class.description}\n\nSkills: {', '.join(selected_class.skills)}\n\nSaves: {', '.join(selected_class.saving_throws)}\n\nProficiencies: {equipment_str}"
            self.tooltip.configure(text=description, anchor='w')

    def update_subclass_description(self, event=None):
        selected_subclass = self.subclass_combobox.get()
        if selected_subclass:
            selected_subclass_obj = gl.get_subclass_by_name(selected_subclass)
            if selected_subclass_obj:
                description = f"{selected_subclass_obj.subclass_description}"
                self.change_description_text(self.tooltip, description)

    # Called when user selects new options. Replaces descriptiosn and recommendations accordingly.
    def change_description_text(self, tooltip, text):
        self.text = text
        self.tooltip = tooltip
        self.tooltip.configure(text=text)

    def add_feat(self, event=None):
        new_row = len(self.feat_selections) + 3  

        new_feat_combobox = ttk.Combobox(master=self.feats_frame, values=self.feats, state="readonly")
        new_feat_combobox.grid(row=new_row, column=0, padx=10, pady=5)

        remove_feat_button = customtkinter.CTkButton(
            master=self.feats_frame,
            text="Remove",
            hover_color="red",
            command=lambda: self.remove_feat(new_row, new_feat_combobox, remove_feat_button)
            )
        remove_feat_button.grid(row=new_row, column=1, padx=5, pady=5)

        self.feat_selections.append((new_feat_combobox, remove_feat_button))
        new_feat_combobox.bind("<<ComboboxSelected>>", self.on_feat_combobox_selected)

    def remove_feat(self, row, feat_combobox, remove_button):
        feat_combobox.destroy()
        remove_button.destroy()

        self.feat_selections = [s for s in self.feat_selections if s != (feat_combobox, remove_button)]

        for index, (feat_cb, rm_btn) in enumerate(self.feat_selections, start=3):
            feat_cb.grid(row=index, column=0, padx=10, pady=5)
            rm_btn.grid(row=index, column=1, padx=5, pady=5)

    def on_race_selection_change(self, event=None):
        selected_race_name = self.race_combobox.get()
        selected_race_class = gl.get_race_map(selected_race_name)
        if selected_race_class:
            selected_race_instance = selected_race_class()
            self.change_description_text(self.tooltip, selected_race_instance.description)

    def on_background_selection_change(self, event=None):
        selected_background = self.background_combobox.get()
        if selected_background:
            self.change_description_text(self.tooltip, gl.get_background_descriptions(selected_background))
    # Generate a random character with random values.
    def auto_generate_character(self):
        self.character_name_entry.delete(0, "end")
        self.character_name_entry.insert(0, "Rand Oman")

        # Randomly select race, class, and background
        random_race = random.choice(gl.get_race_options())
        self.race_combobox.set(random_race)
        random_class = random.choice(gl.get_class_options())
        self.class_combobox.set(random_class)
        random_background = random.choice(gl.get_background_options())
        self.background_combobox.set(random_background)
        self.roll_stats_and_reorder()

        # Update tooltips and other related information based on the random selections.
        # Includes a little humor mostly for myself.
        self.tooltip.configure(text='''
        Wow... how creative of you...
        I'll make this once but you got to level it up yourself.

        <---------------
        Don't forget your skills...
        <---------------

        -------------->\nAnd your feats if you're lvl 4 or higher.
        -------------->
        ''')
        self.tooltip.configure(anchor="center")

    def calculate_class_levels_and_info(self, class_selections, is_opening_sheet=False, character=None):
        total_level = 0
        class_info = []
        class_objects = []

        if is_opening_sheet:
            for class_name, level in character.classes.items():
                class_object = gl.get_class_by_name(class_name)
                class_str = f"{class_name} {level}"
                class_info.append(class_str)
                class_objects.append((class_object, level, None))
        else:
            for class_combobox, levels_combobox, subclass_combobox, _ in class_selections:
                selected_class = class_combobox.get()
                selected_level = int(levels_combobox.get())
                selected_subclass = subclass_combobox.get()
                total_level += selected_level
                class_str = f"{selected_subclass} {selected_class} {selected_level}" if selected_subclass else f"{selected_class} {selected_level}"
                class_info.append(class_str)
                selected_class_object = gl.get_class_by_name(selected_class)
                class_objects.append((selected_class_object, selected_level, selected_subclass))

        class_info_str = ', '.join(class_info)
        return total_level, class_info_str, class_objects

    def create_character(self):
        self.character_name = self.character_name_entry.get()
        self.selected_race = self.race_combobox.get()
        self.selected_background = self.background_combobox.get()
        self.ability_scores = [int(entry.get()) for entry in self.ability_entries]
        self.selected_feats = self.feat_selections
        self.is_jack_of_all_trades = False

        # Prepare class selections data for calculate_class_levels_and_info method
        class_selections = [(self.class_combobox, self.levels_combobox, self.subclass_combobox, None)]
        class_selections.extend(self.class_selections)

        total_level, class_info_str, class_objects = self.calculate_class_levels_and_info(class_selections)

        # Skills change for Bards at lvl 2+. Adds +1 to all non-proficient skills.
        for cls, level, _ in class_objects:
            if cls.name == "Bard" and level >= 2:
                self.is_jack_of_all_trades = True

        self.current_ability_scores = self.ability_scores

        # Prepare character data for saving
        self.character_data = {
            'name': self.character_name,
            'race': self.selected_race,
            'background': self.selected_background,
            'ability_scores': self.ability_scores,
            'feats': self.selected_feats,
            'skill_proficiencies': self.selected_skills,  # Assuming selected_skills contains skill proficiencies
            'is_jack_of_all_trades': self.is_jack_of_all_trades,
            'classes': {cls.name: level for cls, level, _ in class_objects}
        }

        self.create_character_sheet(self.character_data)

        # Save the character data to the current user
        if hasattr(self, 'current_user') and self.current_user:
            self.current_user.add_character(self.character_data)
            self.current_user.display_characters() 
        else:
            print("Current user is not set.")

    def create_character_sheet(self, character_data):
        character_name = character_data['name']
        total_level = sum(character_data['classes'].values())
        selected_race = character_data['race']
        ability_scores = character_data['ability_scores']
        selected_skills = character_data['skill_proficiencies']
        is_jack_of_all_trades = character_data['is_jack_of_all_trades']
        class_objects = [(gl.get_class_by_name(cls_name), level, None) for cls_name, level in character_data['classes'].items()]
        class_info_str = ', '.join([f"{cls} {level}" for cls, level in character_data['classes'].items()])

        for widget in self.root.winfo_children():
            widget.pack_forget()

        self.current_ability_scores = ability_scores

        def increase_hp():
            self.curr_hp += 1
            label_hp.configure(text=f"(Health: {self.curr_hp} | {self.max_hp})")

        def decrease_hp():
            if self.curr_hp > 0:
                self.curr_hp -= 1
                label_hp.configure(text=f"(Health: {self.curr_hp} | {self.max_hp})")

        # Character Sheet frames
        self.main_frame = customtkinter.CTkFrame(master=self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.header_frame = customtkinter.CTkFrame(master=self.main_frame)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.body_frame = customtkinter.CTkFrame(master=self.main_frame, fg_color="transparent")
        self.body_frame.grid(row=1, column=0, sticky="nsew")
        self.body_frame.grid_columnconfigure(1, weight=1)
        self.body_frame.grid_rowconfigure(1, weight=1)
        self.footer_frame = customtkinter.CTkFrame(master=self.main_frame, fg_color="transparent")
        self.footer_frame.grid(row=2, column=0, sticky="ew")

        # Scrollable
        self.cosmetic_inner_frame = customtkinter.CTkFrame(master=self.body_frame, border_width=2, fg_color="transparent")
        self.cosmetic_inner_frame.pack(fill="both", expand=True)
        self.inner_frame = customtkinter.CTkScrollableFrame(master=self.cosmetic_inner_frame, fg_color="transparent")
        self.inner_frame.pack(fill="both", expand=True, padx=5, pady=5)

        label = customtkinter.CTkLabel(master=self.header_frame, text="RPG Character App", font=("Impact", 24))
        label.pack(pady=(10, 0), padx=10)
        label = customtkinter.CTkLabel(master=self.header_frame, text="Character Sheet", font=("Roboto", 18))
        label.pack(fill="both", expand=True, pady=(0, 10), padx=10)

        # Character information section
        self.character_info_frame = customtkinter.CTkFrame(master=self.inner_frame, border_width=0, fg_color="transparent")
        self.character_info_frame.pack(padx=10, pady=(10, 0))
        self.character_info_subframe = customtkinter.CTkFrame(master=self.character_info_frame, border_width=0, fg_color="transparent")
        self.character_info_subframe.grid(row=0, column=0, columnspan=3, sticky="nsew")

        # Character Info
        name_label = customtkinter.CTkLabel(master=self.character_info_subframe, text=f"Name: {character_name}", font=("Roboto", 18, "bold"))
        name_label.pack(fill="both", expand=True, padx=10, pady=(10, 0))
        display_text = f"{selected_race} {class_info_str}"
        character_info_label = customtkinter.CTkLabel(master=self.character_info_subframe, text=display_text, font=("Roboto", 16))
        character_info_label.pack(padx=10, pady=(10, 0))

        # Calculate proficiency bonus inside the method where total_level is accessible
        self.proficiency_bonus = (2 + (total_level - 1) // 4)

        # Ability scores section
        ability_scores_frame = customtkinter.CTkFrame(master=self.character_info_frame, border_width=0)
        ability_scores_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        ability_scores_label = customtkinter.CTkLabel(master=ability_scores_frame, text="Ability Scores", font=("Roboto", 16))
        ability_scores_label.grid(row=0, column=0, sticky="nsw")  # Span across multiple columns

        # Loop through ability scores to display them along with their modifiers
        mods = []
        for index, score in enumerate(ability_scores):
            ability_name = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"][index]
            col_position = index * 2  # Each ability takes up two columns
            label_score = customtkinter.CTkLabel(master=ability_scores_frame, text=f"{ability_name}: {score}", font=("Roboto", 14))
            label_score.grid(row=1, column=col_position, sticky="w", padx=5, pady=5)

            # Calculate and display the modifier for each ability score
            mod = self.calculate_ability_modifier(score)
            mods.append((ability_name, mod))
            operator = '+' if mod >= 0 else '-'
            modifier_score = customtkinter.CTkLabel(master=ability_scores_frame, text=f"({operator}{abs(mod)})", font=("Roboto", 18))
            modifier_score.grid(row=1, column=col_position + 1, sticky="w", padx=5, pady=5)


        # Armor Class
        dexterity_modifier = 0
        for mod_name, mod_value in mods:
            if "Dexterity_modifier" in mod_name:
                dexterity_modifier = mod_value

        base_ac = 10 + dexterity_modifier

        # HP
        self.hp_frame = customtkinter.CTkFrame(master=self.character_info_frame, border_width=0)
        self.hp_frame.grid(row=2, column=1, rowspan=2, sticky="nse")
        self.curr_hp = 0
        self.max_hp = 0
        self.constitution_modifier = next((mod_value for mod_name, mod_value in mods if mod_name == "Constitution"), 0)

        # Loop through each class to calculate HP
        for class_object, levels, subclass in class_objects:
            hit_die_value = int(class_object.hit_die[1:])
            # Max HP for the first level is max hit die value plus Constitution modifier
            if levels > 0:
                first_level_hp = hit_die_value + self.constitution_modifier
                self.max_hp += first_level_hp
            # Calculate HP for each level
            for level in range(2, levels + 1):
                subsequent_level_hp = ((hit_die_value // 2) + 1) + self.constitution_modifier
                self.max_hp += subsequent_level_hp

        self.curr_hp = self.max_hp

        # HP display
        label_hp = customtkinter.CTkLabel(master=self.hp_frame, text=f"(Health: {self.curr_hp} | {self.max_hp})", font=("Roboto", 18))
        label_hp.grid(row=0, column=0, sticky="w", padx=10)

        # Arrow buttons
        button_decrease_hp = customtkinter.CTkButton(master=self.hp_frame, text="▼", command=decrease_hp, fg_color="dark red", hover_color="red", border_width=1, border_color="black", font=("Roboto", 12), width=1, height=1)
        button_decrease_hp.grid(row=0, column=1, padx=5, pady=10)
        button_increase_hp = customtkinter.CTkButton(master=self.hp_frame, text="▲", command=increase_hp, fg_color="green", hover_color="lime", border_width=1, border_color="black", font=("Roboto", 12), width=1, height=1)
        button_increase_hp.grid(row=0, column=2, padx=5, pady=10)

        self.misc_frame = customtkinter.CTkFrame(master=self.character_info_frame, border_width=0)
        self.misc_frame.grid(row=2, column=0, sticky="ew")
        proficiency_bonus = (2 + (total_level - 1) // 4)
        self.label_proficiency_bonus = customtkinter.CTkLabel(master=self.misc_frame, text=f"(Proficiency Bonus: +{proficiency_bonus})", font=("Roboto", 18))
        self.label_proficiency_bonus.grid(row=0, column=0, sticky="w", padx=10)

        walk_speed = 30
        self.label_walk_speed = customtkinter.CTkLabel(master=self.misc_frame, text=f"(Speed: {walk_speed})", font=("Roboto", 18))
        self.label_walk_speed.grid(row=0, column=1, sticky="w", padx=10)

        initiative_bonus = self.calculate_ability_modifier(ability_scores[1])
        self.label_initiative_bonus = customtkinter.CTkLabel(master=self.misc_frame, text=f"(Initiative: +{initiative_bonus})", font=("Roboto", 18))
        self.label_initiative_bonus.grid(row=0, column=2, sticky="w", padx=10)

        self.armor_class_label = customtkinter.CTkLabel(master=self.misc_frame, text="", font=("Roboto", 18))
        self.armor_class_label.grid(row=0, column=3, sticky="w", padx=10)

        # Skills display section
        skills_frame = customtkinter.CTkFrame(master=self.inner_frame, fg_color="transparent")
        skills_frame.pack(side="left", padx=10, pady=10)
        skills_label_frame = customtkinter.CTkFrame(master=skills_frame, fg_color="transparent")
        skills_label_frame.pack(padx=10, pady=(10,5))

        label_skills = customtkinter.CTkLabel(master=skills_label_frame, text="Skills", font=("Roboto", 16))
        label_skills.pack(side="left", padx=(10,20), pady=10)

        label_expertise = customtkinter.CTkLabel(master=skills_label_frame, text="Expertise", font=("Roboto", 14))
        label_expertise.pack(side="right", padx=(20, 10), pady=10)

        # Calculate skill modifiers
        ability_modifiers = {
            "Strength": self.calculate_ability_modifier(ability_scores[0]),
            "Dexterity": self.calculate_ability_modifier(ability_scores[1]),
            "Constitution": self.calculate_ability_modifier(ability_scores[2]),
            "Intelligence": self.calculate_ability_modifier(ability_scores[3]),
            "Wisdom": self.calculate_ability_modifier(ability_scores[4]),
            "Charisma": self.calculate_ability_modifier(ability_scores[5])
        }

        self.skill_modifiers = {
            "Acrobatics": ability_modifiers["Dexterity"],
            "Animal Handling": ability_modifiers["Wisdom"],
            "Arcana": ability_modifiers["Intelligence"],
            "Athletics": ability_modifiers["Strength"],
            "Deception": ability_modifiers["Charisma"],
            "History": ability_modifiers["Intelligence"],
            "Insight": ability_modifiers["Wisdom"],
            "Intimidation": ability_modifiers["Charisma"],
            "Investigation": ability_modifiers["Intelligence"],
            "Medicine": ability_modifiers["Wisdom"],
            "Nature": ability_modifiers["Intelligence"],
            "Perception": ability_modifiers["Wisdom"],
            "Performance": ability_modifiers["Charisma"],
            "Persuasion": ability_modifiers["Charisma"],
            "Religion": ability_modifiers["Intelligence"],
            "Sleight of Hand": ability_modifiers["Dexterity"],
            "Stealth": ability_modifiers["Dexterity"],
            "Survival": ability_modifiers["Wisdom"]
        }

        # Create buttons for each skill with their modifier
        for skill, modifier in self.skill_modifiers.items():
            skill_frame = customtkinter.CTkFrame(master=skills_frame, fg_color="transparent")
            skill_frame.pack(anchor="w", padx=(10, 0), pady=1, fill='x')

            # Determine the modifier, including proficiency and expertise
            if skill in selected_skills:
                modifier += self.proficiency_bonus
            elif is_jack_of_all_trades:
                modifier += self.proficiency_bonus // 2
            modifier_sign = "+" if modifier >= 0 else ""
            if skill in selected_skills:
                skill_button_text = f"*{skill}: {modifier_sign}{modifier}"
            else:
                skill_button_text = f"{skill}: {modifier_sign}{modifier}"

            # Create the skill button with the initial modifier text
            skill_button = customtkinter.CTkButton(
                master=skill_frame,
                text=skill_button_text,
                fg_color="transparent",
                command=lambda s=skill: self.roll_skill(s, selected_skills, self.expertise_vars)
                )
            skill_button.pack(side="left", padx=5)
            self.skill_buttons[skill] = skill_button

            # Create the expertise checkbox
            expertise_var = tk.IntVar()
            self.expertise_vars[skill] = expertise_var
            expertise_checkbox = customtkinter.CTkCheckBox(
                master=skill_frame, text="",
                variable=expertise_var,
                border_width=1,
                command=lambda s=skill: self.update_skill_modifier(s, selected_skills, self.expertise_vars)
                )
            expertise_checkbox.pack(side="right", padx=5)

        # Dice roller section
        self.dice_frame = customtkinter.CTkFrame(master=self.inner_frame, fg_color="transparent")
        self.dice_frame.pack(side="left", padx=10, pady=10, anchor="n")

        dice_button_frame = customtkinter.CTkFrame(master=self.dice_frame)
        dice_button_frame.pack(side="left", padx=10, pady=10)

        # Dice roller buttons
        num_range = [str(i) for i in range(1, 21)]
        self.num_dice_combobox = ttk.Combobox(master=dice_button_frame, values=num_range, width=5)
        self.num_dice_combobox.set("1")
        self.num_dice_combobox.pack(pady=5)

        self.create_dice_button(dice_button_frame, "d20", 20)
        self.create_dice_button(dice_button_frame, "d12", 12)
        self.create_dice_button(dice_button_frame, "d10", 10)
        self.create_dice_button(dice_button_frame, "d8", 8)
        self.create_dice_button(dice_button_frame, "d6", 6)
        self.create_dice_button(dice_button_frame, "d4", 4)
        self.create_dice_button(dice_button_frame, "Flip Coin", 2, "Flip Coin 1:H, 2:T")
        self.create_dice_button(dice_button_frame, "Roll Percentage", 100, "Roll Percentage")

        # Result display
        self.results_frame = customtkinter.CTkFrame(master=self.dice_frame)
        self.results_frame.pack(side="right", padx=10, pady=(0, 10))

        result_label = customtkinter.CTkLabel(master=self.results_frame, text="Dice Roll Results:", font=("Roboto", 16))
        result_label.pack(pady=10)

        self.dice_result_text = customtkinter.CTkTextbox(master=self.results_frame, height=100, width=300)
        self.dice_result_text.pack()

        total_label = customtkinter.CTkLabel(master=self.results_frame, text="Total:")
        total_label.pack(pady=10)

        self.total_text = customtkinter.CTkTextbox(master=self.results_frame, height=1, width=60)
        self.total_text.pack(pady=10)

        self.clear_button = customtkinter.CTkButton(master=self.results_frame, text="Clear", command=self.clear_totals)
        self.clear_button.pack(pady=10)

        # Tabs for Inventory/actions/notes/etc
        self.tabcontrol = customtkinter.CTkTabview(master=self.inner_frame, border_width=2, fg_color="transparent")
        self.tabcontrol.pack(fill="both", expand=True, side="left", pady=10)
        self.inventory_tab = self.tabcontrol.add("Inventory")
                             
        # Inventory
        self.scrollable_inventory_frame = customtkinter.CTkScrollableFrame(master=self.inventory_tab)
        self.scrollable_inventory_frame.pack(fill="both", expand=True)

        self.armor_frame = customtkinter.CTkFrame(master=self.scrollable_inventory_frame)
        self.armor_frame.pack(pady=10)

        # Armor Type Selection
        self.initialize_inventory_section()

        # Footer
        back_button = customtkinter.CTkButton(master=self.footer_frame, text="Back", command=self.open_main_window)
        back_button.pack(pady=10)

    # Helpers for create_character_sheet
    def calculate_skill_modifier(self, skill_name, selected_skills, expertise_vars):
        base_modifier = self.skill_modifiers[skill_name]
        if skill_name in selected_skills:
            base_modifier += self.proficiency_bonus
        if expertise_vars[skill_name].get() == 1:
            base_modifier += self.proficiency_bonus  # Add again for expertise
        elif self.is_jack_of_all_trades and skill_name not in selected_skills:
            base_modifier += self.proficiency_bonus // 2  # Add half proficiency for Jack of All Trades
        return base_modifier

    def roll_skill(self, skill_name, selected_skills, expertise_vars):
        modifier = self.calculate_skill_modifier(skill_name, selected_skills, expertise_vars)
        roll_result = random.randint(1, 20)
        total = roll_result + modifier
        self.dice_result_text.insert("end", f"{skill_name} Roll: {roll_result} + Modifier: {modifier} = Total: {total}\n")
        self.dice_result_text.see("end")

    def update_skill_modifier(self, skill_name, selected_skills, expertise_vars):
        modifier = self.calculate_skill_modifier(skill_name, selected_skills, expertise_vars)
        modifier_sign = "+" if modifier >= 0 else ""
        if skill_name in selected_skills:
            skill_button_text = f"*{skill_name}: {modifier_sign}{modifier}"
        else:
            skill_button_text = f"{skill_name}: {modifier_sign}{modifier}"
        self.skill_buttons[skill_name].configure(text=skill_button_text)

    def create_dice_button(self, frame, text, sides, special_text=None):
        button_text = special_text if special_text else f"Roll {text}"
        button = customtkinter.CTkButton(master=frame, text=button_text, command=lambda: self.roll_dice(sides))
        button.pack(pady=5)

    def roll_dice(self, sides):
        num_dice = int(self.num_dice_combobox.get())
        results, total = gl.roll_dice_logic(sides, num_dice)
        self.dice_result_text.insert("end", f"Rolled {num_dice}d{sides}: {results} (Total: {total})\n")
        self.total_text.delete("1.0", "end")
        self.total_text.insert("1.0", f"{total}\n")
        self.dice_result_text.see("end")

    def calculate_ability_modifier(self, score):
        return (score - 10) // 2

    def initialize_inventory_section(self):
        # Inventory setup...
        self.armor_label = customtkinter.CTkLabel(master=self.armor_frame, text="Select Armor:")
        self.armor_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")
        self.armor_type_combobox = ttk.Combobox(master=self.armor_frame, values=gl.get_armor_type_options(), state="readonly")
        self.armor_type_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.armor_type_combobox.set("No Armor")

        # Specific Armor Selection
        self.armor_options_label = customtkinter.CTkLabel(master=self.armor_frame, text="Be More Specific:")
        self.armor_options_label.grid(row=1, column=0, padx=10, pady=10, sticky="nsw")
        self.armor_options_combobox = ttk.Combobox(master=self.armor_frame, width=30, state="readonly")
        self.armor_options_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.armor_options_combobox.set("No Armor")

        # Shield Selection
        self.shield_label = customtkinter.CTkLabel(master=self.armor_frame, text="Shield / AC Bonus:")
        self.shield_label.grid(row=2, column=0, padx=10, pady=10, sticky="nsw")
        self.shield_combobox = ttk.Combobox(master=self.armor_frame, width=5, values=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], state="readonly")
        self.shield_combobox.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        self.shield_combobox.set(0)

        self.armor_type_combobox.bind("<<ComboboxSelected>>", self.on_armor_type_select)
        self.armor_options_combobox.bind("<<ComboboxSelected>>", self.update_ac_display)
        self.shield_combobox.bind("<<ComboboxSelected>>", self.update_ac_display)
        self.update_ac_display()  # Initial AC calculation

    def on_armor_type_select(self, event):
        self.update_ac_display()
        self.update_armor_options(event)

    def update_ac_display(self, event=None):
        armor_type = self.armor_type_combobox.get()
        armor_name = self.armor_options_combobox.get() if armor_type != "No Armor" else ""
        dex_modifier = self.calculate_ability_modifier(self.current_ability_scores[1])  # Use the stored ability scores
        shield_bonus = int(self.shield_combobox.get())
        total_ac = gl.calculate_ac(armor_type, armor_name, dex_modifier, shield_bonus)
        self.armor_class_label.configure(text=f"Armor Class: {total_ac}")

    def update_armor_options(self, event):
        selected_type = self.armor_type_combobox.get()
        options = gl.get_armor_options().get(selected_type, [""])
        self.armor_options_combobox['values'] = options
        self.armor_options_combobox.current(0)
        self.update_ac_display()

class AdminUI:
    def __init__(self, root, admin_user, go_back_function, main_window_ui):
        self.root = root
        self.admin_user = admin_user
        self.go_back_function = go_back_function
        self.main_window_ui = main_window_ui
        self.character_frame = None

    def initialize_ui(self):
        self.main_frame = customtkinter.CTkFrame(master=self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.header_frame = customtkinter.CTkFrame(master=self.main_frame)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.body_frame = customtkinter.CTkFrame(master=self.main_frame, fg_color="transparent")
        self.body_frame.grid(row=1, column=0, sticky="nsew")
        self.body_frame.grid_columnconfigure(1, weight=1)
        self.body_frame.grid_rowconfigure(1, weight=1)
        self.footer_frame = customtkinter.CTkFrame(master=self.main_frame, fg_color="transparent")
        self.footer_frame.grid(row=2, column=0, sticky="ew")

        self.users_frame = customtkinter.CTkScrollableFrame(master=self.body_frame)
        self.users_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.character_frame = customtkinter.CTkFrame(master=self.body_frame, fg_color="transparent")
        self.character_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        label = customtkinter.CTkLabel(master=self.header_frame, text="RPG Character App", font=("Impact", 24))
        label.pack(pady=(10, 0), padx=10)

        label = customtkinter.CTkLabel(master=self.header_frame, text="Admin Panel", text_color="green", font=("Roboto", 18))
        label.pack(fill="both", expand=True, pady=(0, 10), padx=10)

        self. display_users()

        back_button = customtkinter.CTkButton(
            master=self.footer_frame,
            text="Back",
            fg_color="green",
            hover_color="#186A3B",
            command=self.go_back_function)
        back_button.pack(pady=10)

    def display_users(self):
        users = db.get_all_users()
        for idx, user in enumerate(users):
            user_id, username, email, is_admin = user
            user_btn_text = f"{username} - {email}" + (" - Admin" if is_admin else "")
            user_button = customtkinter.CTkButton(
                self.users_frame,
                text=user_btn_text,
                fg_color="transparent",
                hover_color="green",
                command=lambda u=user_id: self.user_action(u))  # u=user_id captures the current value
            user_button.grid(row=idx, column=0, pady=2, padx=10, sticky="nsw")
            delete_button = customtkinter.CTkButton(
                self.users_frame,
                text="Delete",
                fg_color="#186A3B",
                hover_color="red",
                command=lambda u=username: db.remove_user(u))  # u=username captures the current value
            delete_button.grid(row=idx, column=1, pady=2, padx=10)


    def user_action(self, user_id):
        self.user_id = user_id
        user_data = db.get_user_by_id(self.user_id)
        if user_data:
            self.display_user_characters(user_data)
        else:
            print(f"No user found with UserID: {user_id}")

    def display_user_characters(self, user_data):
        characters = db.get_user_characters(user_data)

        if self.character_frame:
            self.character_frame.destroy()

        self.character_frame = customtkinter.CTkFrame(master=self.body_frame, fg_color="transparent")
        self.character_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        if characters:
            for character_id, character_name in characters:
                character_button = customtkinter.CTkButton(
                    self.character_frame,
                    text=character_name,
                    fg_color="transparent",
                    hover_color="red",
                    command=lambda cid=character_id: self.main_window_ui.delete_character(cid)  # cid=character_id captures the current value
                )
                character_button.pack(pady=2, padx=10)
        else:
            print("No characters found for the user.")

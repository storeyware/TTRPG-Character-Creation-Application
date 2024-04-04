"""
Module: user_database.py

Description:
    Handles interactions with the user database, including creating users,
    fetching user information, and deleting users.

Usage:
    This module provides functions like create_users_table(), register_user(),
    get_user(), and remove_user() to manipulate user data stored in an SQLite database.
    It manages all database interactions for the application.

Dependencies:
    Requires sqlite3 for database operations.
"""
import os, sys
import sqlite3
import tkinter.messagebox
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(MODULE_DIR, "../database/users.db")

def create_connection(db_file=DB_PATH):
    """Create a database connection to the SQLite database specified by db_file."""
    # Determine the directory of the executable or script
    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, db_file)
    try:
        return sqlite3.connect(db_path)
    except sqlite3.Error as e:
        print(e)
        return None

def create_users_table():
    """Create the Users table in the database if it doesn't exist."""
    conn = create_connection()
    if conn is not None:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                UserID INTEGER PRIMARY KEY,
                Username TEXT UNIQUE NOT NULL,
                PasswordHash TEXT NOT NULL,
                Salt TEXT NOT NULL,
                Email TEXT UNIQUE NOT NULL,
                IsAdmin INTEGER NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()
    else:
        print("Error! Cannot create database connection.")

def register_user(username, password_hash, salt, email):
    """Insert a new user into the database if the username and email are not already in use."""
    conn = create_connection()
    if conn is not None:
        c = conn.cursor()
        try:
            # Check if the email already exists
            c.execute("SELECT * FROM Users WHERE Email = ?", (email,))
            if c.fetchone() is not None:
                print("Email already exists")
                tkinter.messagebox.showwarning("Warning", "Email already exists.")
                return False

            # Check if the username already exists
            c.execute("SELECT * FROM Users WHERE Username = ?", (username,))
            if c.fetchone() is not None:
                print("Username already exists")
                tkinter.messagebox.showwarning("Warning", "Username already exists.")
                return False

            # Insert the new user as both username and email are unique
            c.execute("INSERT INTO Users (Username, PasswordHash, Salt, Email) VALUES (?, ?, ?, ?)", 
                      (username, password_hash, salt, email))
            conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print("SQLite error:", e.args[0])
            return False
        finally:
            conn.close()

def get_user(username):
    """Retrieve a user's information from the database."""
    conn = create_connection()
    if conn is not None:
        c = conn.cursor()
        c.execute("SELECT UserID, Username, PasswordHash, Salt, Email, IsAdmin FROM Users WHERE Username = ?", (username,))
        user = c.fetchone()
        conn.close()
        if user:
            print("Fetched user data:", user)
            return user
        else:
            print(f"No user found with username: {username}")
            return None
    else:
        print("Error creating database connection.")
        return None

def get_user_characters(user_data):
    """Retrieve all characters associated with a user."""
    conn = create_connection()
    if conn is not None:
        c = conn.cursor()
        user_id, *_ = user_data  # Unpack only the user ID
        c.execute("SELECT CharacterID, CharacterName FROM Characters WHERE UserID = ?", (user_id,))
        characters = c.fetchall()
        conn.close()
        return characters
    else:
        print("Error creating database connection.")
        return []

# gets User class rather than data
def get_user_by_id(user_id):
    """Retrieve a user's information from the database."""
    conn = create_connection()
    if conn is not None:
        c = conn.cursor()
        c.execute("SELECT UserID, Username, PasswordHash, Salt, Email, IsAdmin FROM Users WHERE UserID = ?", (user_id,))
        user = c.fetchone()
        conn.close()
        if user:
            print("Fetched user data:", user)
            return user
        else:
            print(f"No user found with UserID: {user_id}")
            return None
    else:
        print("Error creating database connection.")
        return None

def remove_user(username):
    """Remove a user and all associated characters from the database."""
    conn = create_connection()
    if conn is not None:
        print("attempting to delete user and associated characters", username)
        c = conn.cursor()

        # Get user ID
        c.execute("SELECT UserID FROM Users WHERE Username = ?", (username,))
        user_id_row = c.fetchone()
        if user_id_row:
            user_id = user_id_row[0]

            # Retrieve all character IDs associated with the user
            c.execute("SELECT CharacterID FROM Characters WHERE UserID = ?", (user_id,))
            character_ids = [row[0] for row in c.fetchall()]

            # Delete related data for each character
            for character_id in character_ids:
                c.execute("DELETE FROM Classes WHERE CharacterID = ?", (character_id,))
                c.execute("DELETE FROM CharacterSkills WHERE CharacterID = ?", (character_id,))
                c.execute("DELETE FROM Characters WHERE CharacterID = ?", (character_id,))

        else:
            print("User not found, no characters deleted.")

        # Delete the user
        c.execute("DELETE FROM Users WHERE Username = ?", (username,))
        print("User and associated characters deleted")

        conn.commit()
        conn.close()
    else:
        print("Error! Cannot create database connection.")

def get_character(character_id):
    conn = create_connection()
    character_data = {}
    if conn is not None:
        c = conn.cursor()
        # Get the basic character information
        c.execute("SELECT * FROM Characters WHERE CharacterID = ?", (character_id,))
        row = c.fetchone()
        if row:
            character_data = {
                'character_id': row[0],
                'user_id': row[1],
                'name': row[2],
                'race': row[3],
                'background': row[4],
                'ability_scores': list(map(int, row[5].split(','))),
                'feats': row[6].split(',') if row[6] else [],
                'is_jack_of_all_trades': bool(row[7])
            }

            # Get the character's classes
            c.execute("SELECT ClassName, Level FROM Classes WHERE CharacterID = ?", (character_id,))
            classes = c.fetchall()
            character_data['classes'] = {class_name: level for class_name, level in classes}

            # Get the character's skill proficiencies
            c.execute("SELECT SkillName FROM CharacterSkills WHERE CharacterID = ?", (character_id,))
            skills = c.fetchall()
            character_data['skill_proficiencies'] = [skill[0] for skill in skills]

        conn.close()
    return character_data

def create_characters_table():
    """Create the Characters, Classes, and CharacterSkills tables in the database if they don't exist."""
    print("Creating character tables...")
    conn = create_connection()
    if conn is not None:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS Characters (
                CharacterID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER,
                CharacterName TEXT NOT NULL,
                Race TEXT NOT NULL,
                Background TEXT,
                AbilityScores TEXT NOT NULL,
                Feats TEXT,
                IsJackOfAllTrades INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (UserID) REFERENCES Users(UserID)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS Classes (
                ClassID INTEGER PRIMARY KEY AUTOINCREMENT,
                CharacterID INTEGER,
                ClassName TEXT NOT NULL,
                Level INTEGER NOT NULL,
                FOREIGN KEY (CharacterID) REFERENCES Characters(CharacterID)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS CharacterSkills (
                SkillID INTEGER PRIMARY KEY AUTOINCREMENT,
                CharacterID INTEGER,
                SkillName TEXT NOT NULL,
                FOREIGN KEY (CharacterID) REFERENCES Characters(CharacterID)
            )
        ''')
        conn.commit()
        conn.close()
    else:
        print("Error! Cannot create database connection.")

def add_character_to_db(user_id, character_data):
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Characters (UserID, CharacterName, Race, Background, AbilityScores, Feats, IsJackOfAllTrades) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    user_id,
                    character_data['name'],
                    character_data['race'],
                    character_data['background'],
                    ','.join(map(str, character_data['ability_scores'])),
                    ','.join(map(str, character_data.get('feats', []))),
                    int(character_data.get('is_jack_of_all_trades', False))
                )
            )

            character_id = cursor.lastrowid
            for class_name, level in character_data['classes'].items():
                cursor.execute(
                    "INSERT INTO Classes (CharacterID, ClassName, Level) VALUES (?, ?, ?)",
                    (character_id, class_name, level)
                )

            for skill in character_data.get('skill_proficiencies', []):
                cursor.execute(
                    "INSERT INTO CharacterSkills (CharacterID, SkillName) VALUES (?, ?)",
                    (character_id, skill)
                )

            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()
    else:
        print("Failed to create database connection.")

def delete_character_from_db(character_id):
    conn = create_connection()
    if conn is not None:
        c = conn.cursor()
        c.execute("DELETE FROM Characters WHERE CharacterID = ?", (character_id,))
        conn.commit()
        conn.close()

# admin stuff
def get_all_users():
    """Retrieve all users' information from the database."""
    conn = create_connection()
    if conn is not None:
        c = conn.cursor()
        c.execute("SELECT UserID, Username, Email, IsAdmin FROM Users")
        users = c.fetchall()
        conn.close()
        return users
    else:
        print("Error creating database connection.")
        return []

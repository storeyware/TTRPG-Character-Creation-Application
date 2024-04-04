"""
Module: auth.py

Description:
    This module provides authentication functionalities for the application, including
    user registration and login. It handles password hashing, email validation, and
    integrates with the user_database module to interact with the user data.

Dependencies:
    - os: For generating a random salt.
    - hashlib: For hashing passwords.
    - user_database.py: For interacting with the user database.
    - game_logic.py: For creating User objects.
    - re: For email validation.
    - tkinter.messagebox: For displaying messages in the UI.

Usage:
    - Call `register` with user details to create a new user account.
    - Call `login` with username and password to authenticate a user.
"""
import os
import hashlib
import user_database as db
import game_logic as gl
from game_logic import User
import ui
import re
import tkinter.messagebox

# Login / Register
def hash_password(password, salt=None):
    """Hash a password with an optional salt."""
    if salt is None:
        salt = os.urandom(16)  # Generate a new salt
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return pwdhash.hex(), salt.hex()

def is_valid_email(email):
    """Check if the email is valid."""
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(email_regex, email) is not None

def register(username, password, repeat_password, email, open_login_callback):
    if password != repeat_password:
        return False, "Passwords do not match"

    if not is_valid_email(email):
        return False, "Invalid email address"

    if db.get_user(username):
        return False, "Username already exists"

    pwdhash, salt = hash_password(password)
    if db.register_user(username, pwdhash, salt, email):
        # After successful registration, fetch the user to get the user_id
        user_data = db.get_user(username)
        if user_data:
            user_id, username, stored_hash, stored_salt, email, is_admin = user_data
            new_user = gl.User(user_id=user_id, username=username, password=password, email=email)
            open_login_callback()
            return True, "Registration successful"
    return False, "Registration failed"

def login(username, password):
    user_data = db.get_user(username)
    if user_data:
        user_id, username, stored_hash, stored_salt, email, is_admin = user_data
        pwdhash, _ = hash_password(password, bytes.fromhex(stored_salt))
        if pwdhash == stored_hash:
            user_object = gl.User(user_id=user_id, username=username, password=password, email=email, is_admin=bool(is_admin))
            return True, user_object, "Login successful"
    return False, None, "Invalid username or password"


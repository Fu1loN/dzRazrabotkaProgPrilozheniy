import json
from pathlib import Path

class UserModel:
    def __init__(self):
        self.users_file = "users.json"
        self._ensure_file_exists()
        
    def _ensure_file_exists(self):
        if not Path(self.users_file).exists():
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)
    
    def load_users(self):
        with open(self.users_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_users(self, users):
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=4)
    
    def check_password_strength(self, password):
        if len(password) < 8:
            return False
            
        has_digit = any(char.isdigit() for char in password)
        has_upper = any(char.isupper() for char in password)
        has_lower = any(char.islower() for char in password)
        
        # Список специальных символов для проверки
        special_chars = "!@#$%^&*(),.?\":{}|<>"
        has_special = any(char in special_chars for char in password)
        
        return all([has_digit, has_upper, has_lower, has_special])
    
    def authenticate_user(self, login, password):
        users = self.load_users()
        if login in users and users[login]['password'] == password:
            return users[login]
        return None
    
    def create_user(self, login, password, first_name="", last_name="", email=""):
        users = self.load_users()
        if login in users:
            return False, "User already exists"
        
        if not self.check_password_strength(password):
            return False, "Password must contain uppercase and lowercase letters, numbers, and special characters"
        
        users[login] = {
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }
        self.save_users(users)
        return True, "User created successfully"
    
    def update_user(self, login, first_name, last_name, email):
        users = self.load_users()
        if login not in users:
            return False, "User not found"
        
        users[login]['first_name'] = first_name
        users[login]['last_name'] = last_name
        users[login]['email'] = email
        self.save_users(users)
        return True, "User updated successfully" 
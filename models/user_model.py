import json
from pathlib import Path
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from typing import Any, Dict, List

class UserModel(QAbstractTableModel):
    # Определяем колонки таблицы
    HEADERS = ['Login', 'First Name', 'Last Name', 'Email']
    
    def __init__(self):
        super().__init__()
        self.users_file = "users.json"
        self._ensure_file_exists()
        self.users: Dict[str, Dict[str, str]] = self.load_users()
        self._users_list: List[Dict[str, str]] = []
        self._update_users_list()
    
    def _update_users_list(self):
        """Обновляет внутренний список пользователей для табличного представления"""
        self._users_list = [
            {"login": login, **data}
            for login, data in self.users.items()
        ]
    
    def _ensure_file_exists(self):
        if not Path(self.users_file).exists():
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)
    
    def load_users(self) -> Dict[str, Dict[str, str]]:
        with open(self.users_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_users(self):
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, indent=4)
    
    # Реализация методов QAbstractTableModel
    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._users_list)
    
    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self.HEADERS)
    
    def data(self, index: QModelIndex, role=Qt.DisplayRole) -> Any:
        if not index.isValid():
            return None
            
        if role == Qt.DisplayRole:
            user = self._users_list[index.row()]
            column = index.column()
            
            if column == 0:
                return user['login']
            elif column == 1:
                return user['first_name']
            elif column == 2:
                return user['last_name']
            elif column == 3:
                return user['email']
        
        return None
    
    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.DisplayRole) -> Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.HEADERS[section]
        return None
    
    def check_password_strength(self, password: str) -> bool:
        if len(password) < 8:
            return False
            
        has_digit = any(char.isdigit() for char in password)
        has_upper = any(char.isupper() for char in password)
        has_lower = any(char.islower() for char in password)
        
        # Список специальных символов для проверки
        special_chars = "!@#$%^&*(),.?\":{}|<>"
        has_special = any(char in special_chars for char in password)
        
        return all([has_digit, has_upper, has_lower, has_special])
    
    def authenticate_user(self, login: str, password: str) -> Dict[str, str] | None:
        if login in self.users and self.users[login]['password'] == password:
            return self.users[login]
        return None
    
    def create_user(self, login: str, password: str, first_name: str = "", 
                   last_name: str = "", email: str = "") -> tuple[bool, str]:
        if login in self.users:
            return False, "User already exists"
        
        if not self.check_password_strength(password):
            return False, "Password must contain uppercase and lowercase letters, numbers, and special characters"
        
        # Начинаем обновление модели
        self.beginInsertRows(QModelIndex(), len(self._users_list), len(self._users_list))
        
        self.users[login] = {
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }
        
        self._update_users_list()
        self.save_users()
        
        # Завершаем обновление модели
        self.endInsertRows()
        return True, "User created successfully"
    
    def update_user(self, login: str, first_name: str, last_name: str, 
                   email: str) -> tuple[bool, str]:
        if login not in self.users:
            return False, "User not found"
        
        # Находим индекс пользователя в списке
        row = next((i for i, user in enumerate(self._users_list) 
                   if user['login'] == login), -1)
        
        if row == -1:
            return False, "User not found in list"
            
        self.users[login].update({
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        })
        
        self._update_users_list()
        self.save_users()
        
        # Оповещаем о изменении данных
        self.dataChanged.emit(
            self.index(row, 0),
            self.index(row, self.columnCount() - 1)
        )
        
        return True, "User updated successfully" 
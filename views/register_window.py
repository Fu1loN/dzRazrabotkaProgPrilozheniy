from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                                 QLabel, QLineEdit, QPushButton, QMessageBox,
                                 QFrame)
from PySide6.QtCore import Qt, Signal

class RegisterWindow(QMainWindow):
    registration_successful = Signal(str, dict)
    finished = Signal()
    
    def __init__(self, user_model, preset_login=""):
        super().__init__()
        self.user_model = user_model
        self.preset_login = preset_login
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("User Management - Create Account")
        self.setMinimumSize(400, 450)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(8)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Registration form
        title_label = QLabel("Create New Account")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        layout.addSpacing(20)
        
        # Login field
        layout.addWidget(QLabel("Login:"))
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Enter your login")
        if self.preset_login:
            self.login_input.setText(self.preset_login)
        layout.addWidget(self.login_input)
        
        # Password container
        password_container = QFrame()
        password_container.setObjectName("fieldContainer")
        password_layout = QVBoxLayout(password_container)
        password_layout.setSpacing(4)
        password_layout.setContentsMargins(0, 0, 0, 0)
        
        # Password fields
        password_layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.textChanged.connect(self.validate_password_strength)
        password_layout.addWidget(self.password_input)
        
        # Password requirements label
        self.password_error = QLabel("Password must contain uppercase and lowercase letters,\nnumbers, and special characters")
        self.password_error.setObjectName("error")
        self.password_error.setWordWrap(True)
        password_layout.addWidget(self.password_error)
        
        layout.addWidget(password_container)
        
        # Confirm password container
        confirm_container = QFrame()
        confirm_container.setObjectName("fieldContainer")
        confirm_layout = QVBoxLayout(confirm_container)
        confirm_layout.setSpacing(4)
        confirm_layout.setContentsMargins(0, 0, 0, 0)
        
        confirm_layout.addWidget(QLabel("Confirm Password:"))
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm your password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.textChanged.connect(self.validate_passwords_match)
        confirm_layout.addWidget(self.confirm_password_input)
        
        # Confirm password error label
        self.confirm_error = QLabel()
        self.confirm_error.setObjectName("error")
        self.confirm_error.hide()
        confirm_layout.addWidget(self.confirm_error)
        
        layout.addWidget(confirm_container)
        
        layout.addSpacing(20)
        
        # Create account button
        self.create_button = QPushButton("Create Account")
        self.create_button.clicked.connect(self.try_register)
        self.create_button.setEnabled(False)
        layout.addWidget(self.create_button)
        
        # Cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.setProperty("danger", True)
        cancel_button.clicked.connect(self.close)
        layout.addWidget(cancel_button)
        
        layout.addStretch()
    
    def validate_password_strength(self):
        """Проверка надежности пароля"""
        password = self.password_input.text()
        
        if password:
            is_strong = self.user_model.check_password_strength(password)
            self.password_input.setProperty("invalid", not is_strong)
            if not is_strong:
                self.password_error.show()
            else:
                self.password_error.hide()
            self.password_input.style().unpolish(self.password_input)
            self.password_input.style().polish(self.password_input)
        else:
            self.password_error.show()
            self.password_input.setProperty("invalid", False)
            self.password_input.style().unpolish(self.password_input)
            self.password_input.style().polish(self.password_input)
        
        self.update_create_button()
    
    def validate_passwords_match(self):
        """Проверка совпадения паролей"""
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        if confirm_password:
            passwords_match = password == confirm_password
            self.confirm_password_input.setProperty("invalid", not passwords_match)
            if not passwords_match:
                self.confirm_error.setText("Passwords do not match")
                self.confirm_error.show()
            else:
                self.confirm_error.hide()
            self.confirm_password_input.style().unpolish(self.confirm_password_input)
            self.confirm_password_input.style().polish(self.confirm_password_input)
        else:
            self.confirm_error.hide()
            self.confirm_password_input.setProperty("invalid", False)
            self.confirm_password_input.style().unpolish(self.confirm_password_input)
            self.confirm_password_input.style().polish(self.confirm_password_input)
        
        self.update_create_button()
    
    def update_create_button(self):
        """Обновление состояния кнопки создания аккаунта"""
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        self.create_button.setEnabled(
            bool(password) and 
            bool(confirm_password) and 
            password == confirm_password and 
            self.user_model.check_password_strength(password)
        )
    
    def closeEvent(self, event):
        self.finished.emit()
        super().closeEvent(event)
    
    def try_register(self):
        login = self.login_input.text()
        password = self.password_input.text()
        
        if not login or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return
        
        success, message = self.user_model.create_user(login, password)
        if success:
            QMessageBox.information(self, "Success", "Account created successfully!")
            self.registration_successful.emit(login, {'password': password})
            self.close()
        else:
            QMessageBox.warning(self, "Error", message) 
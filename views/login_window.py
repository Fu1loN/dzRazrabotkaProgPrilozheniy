from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                                 QLabel, QLineEdit, QPushButton, QMessageBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

class LoginWindow(QMainWindow):
    login_successful = Signal(str, dict)
    register_requested = Signal(str)
    
    def __init__(self, user_model):
        super().__init__()
        self.user_model = user_model
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("User Management - Login")
        self.setMinimumSize(400, 300)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)
        
        # Login form
        title_label = QLabel("Login to Your Account")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        layout.addSpacing(20)
        
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Enter your login")
        layout.addWidget(QLabel("Login:"))
        layout.addWidget(self.login_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        
        layout.addSpacing(20)
        
        # Buttons
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.try_login)
        layout.addWidget(self.login_button)
        
        self.register_button = QPushButton("Create New Account")
        self.register_button.setProperty("secondary", True)
        self.register_button.clicked.connect(self.open_register)
        layout.addWidget(self.register_button)
        
        layout.addStretch()
    
    def try_login(self):
        login = self.login_input.text()
        password = self.password_input.text()
        
        if not login or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return
        
        user_data = self.user_model.authenticate_user(login, password)
        if user_data:
            self.login_successful.emit(login, user_data)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setText("User not found or incorrect password")
            msg.setInformativeText("Would you like to create a new account?")
            msg.setWindowTitle("Login Failed")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            
            if msg.exec() == QMessageBox.Yes:
                self.open_register(login)
    
    def open_register(self, preset_login=None):
        # Disable all inputs and buttons
        self.login_input.setEnabled(False)
        self.password_input.setEnabled(False)
        self.login_button.setEnabled(False)
        self.register_button.setEnabled(False)
        
        # Set window title to indicate registration is in progress
        self.setWindowTitle("User Management - Login (Registration in Progress)")
        
        self.register_requested.emit(preset_login if preset_login else "")
    
    def enable_login(self):
        # Re-enable all inputs and buttons
        self.login_input.setEnabled(True)
        self.password_input.setEnabled(True)
        self.login_button.setEnabled(True)
        self.register_button.setEnabled(True)
        
        # Restore original window title
        self.setWindowTitle("User Management - Login") 
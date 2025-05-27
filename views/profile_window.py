from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                                 QLabel, QPushButton, QMenuBar, QMenu)
from PySide6.QtCore import Qt, Signal
from .edit_window import EditWindow

class ProfileWindow(QMainWindow):
    edit_requested = Signal(str)
    logout_requested = Signal()
    
    def __init__(self, user_model, current_login):
        super().__init__()
        self.user_model = user_model
        self.current_login = current_login
        self.edit_window = None
        self.setup_ui()
        self.load_user_data()
        
    def setup_ui(self):
        self.setWindowTitle("User Management - Profile")
        self.setMinimumSize(400, 300)
        
        # Create menu bar
        menubar = QMenuBar()
        self.setMenuBar(menubar)
        
        # File menu
        file_menu = QMenu("File", self)
        menubar.addMenu(file_menu)
        
        logout_action = file_menu.addAction("Logout")
        logout_action.triggered.connect(self.logout)
        
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)
        
        # Welcome title
        title_label = QLabel("Profile Information")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        layout.addSpacing(20)
        
        # User info container
        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)
        info_layout.setSpacing(10)
        
        self.login_label = QLabel()
        self.login_label.setObjectName("info")
        info_layout.addWidget(self.login_label)
        
        self.name_label = QLabel()
        self.name_label.setObjectName("info")
        info_layout.addWidget(self.name_label)
        
        self.email_label = QLabel()
        self.email_label.setObjectName("info")
        info_layout.addWidget(self.email_label)
        
        layout.addWidget(info_container)
        
        layout.addSpacing(20)
        
        # Edit button
        edit_button = QPushButton("Edit Profile")
        edit_button.setProperty("secondary", True)
        edit_button.clicked.connect(self.show_edit_window)
        layout.addWidget(edit_button)
        
        layout.addStretch()
    
    def load_user_data(self):
        users = self.user_model.load_users()
        user_data = users.get(self.current_login, {})
        
        self.login_label.setText(f"Login: {self.current_login}")
        
        first_name = user_data.get('first_name', '')
        last_name = user_data.get('last_name', '')
        if first_name or last_name:
            self.name_label.setText(f"Name: {first_name} {last_name}".strip())
        else:
            self.name_label.setText("Name: Not set")
        
        email = user_data.get('email', '')
        if email:
            self.email_label.setText(f"Email: {email}")
        else:
            self.email_label.setText("Email: Not set")
    
    def show_edit_window(self):
        self.edit_window = EditWindow(self.user_model, self.current_login)
        self.edit_window.edit_successful.connect(self.load_user_data)
        self.edit_window.finished.connect(self.enable_window)
        self.edit_window.show()
        self.disable_window()
    
    def disable_window(self):
        self.setEnabled(False)
    
    def enable_window(self):
        self.setEnabled(True)
    
    def logout(self):
        self.logout_requested.emit() 
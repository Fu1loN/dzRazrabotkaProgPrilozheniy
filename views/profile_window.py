from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                                 QLabel, QPushButton, QMenuBar, QMenu, QFormLayout)
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
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(10)
        
        # Welcome title
        title_label = QLabel("Profile Information")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        main_layout.addSpacing(20)
        
        # Create form layout for user data
        form_container = QWidget()
        form_layout = QFormLayout(form_container)
        form_layout.setSpacing(10)
        form_layout.setContentsMargins(20, 0, 20, 0)
        
        # Create labels for user data
        self.login_label = QLabel()
        self.first_name_label = QLabel()
        self.last_name_label = QLabel()
        self.email_label = QLabel()
        
        # Set object names for styling
        for label in [self.login_label, self.first_name_label, 
                     self.last_name_label, self.email_label]:
            label.setObjectName("info")
        
        # Add fields to form
        form_layout.addRow("Login:", self.login_label)
        form_layout.addRow("First Name:", self.first_name_label)
        form_layout.addRow("Last Name:", self.last_name_label)
        form_layout.addRow("Email:", self.email_label)
        
        main_layout.addWidget(form_container)
        
        main_layout.addSpacing(20)
        
        # Edit button
        edit_button = QPushButton("Edit Profile")
        edit_button.setProperty("secondary", True)
        edit_button.clicked.connect(self.show_edit_window)
        main_layout.addWidget(edit_button)
        
        main_layout.addStretch()
    
    def load_user_data(self):
        # Находим индекс текущего пользователя в модели
        current_row = -1
        for row in range(self.user_model.rowCount()):
            if self.user_model.data(self.user_model.index(row, 0)) == self.current_login:
                current_row = row
                break
        
        if current_row == -1:
            return
            
        # Получаем данные из модели
        self.login_label.setText(self.user_model.data(self.user_model.index(current_row, 0)) or 'Not set')
        self.first_name_label.setText(self.user_model.data(self.user_model.index(current_row, 1)) or 'Not set')
        self.last_name_label.setText(self.user_model.data(self.user_model.index(current_row, 2)) or 'Not set')
        self.email_label.setText(self.user_model.data(self.user_model.index(current_row, 3)) or 'Not set')
    
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
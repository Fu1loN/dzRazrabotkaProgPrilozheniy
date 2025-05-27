from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                                 QLabel, QLineEdit, QPushButton, QMessageBox,
                                 QFrame)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

class EditWindow(QMainWindow):
    edit_successful = Signal()
    finished = Signal()
    
    def __init__(self, user_model, current_login):
        super().__init__()
        self.user_model = user_model
        self.current_login = current_login
        
        # Находим индекс текущего пользователя в модели
        self.current_row = -1
        for row in range(self.user_model.rowCount()):
            if self.user_model.data(self.user_model.index(row, 0)) == current_login:
                self.current_row = row
                break
                
        self.setup_ui()
        self.load_user_data()
        
    def setup_ui(self):
        self.setWindowTitle("User Management - Edit Profile")
        self.setMinimumSize(400, 550)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(8)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Edit form
        title_label = QLabel("Edit Profile")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        layout.addSpacing(20)
        
        # First name field
        layout.addWidget(QLabel("First Name:"))
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Enter your first name")
        layout.addWidget(self.first_name_input)
        
        # Last name field
        layout.addWidget(QLabel("Last Name:"))
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Enter your last name")
        layout.addWidget(self.last_name_input)
        
        # Email field container
        email_container = QFrame()
        email_container.setObjectName("fieldContainer")
        email_layout = QVBoxLayout(email_container)
        email_layout.setSpacing(4)
        email_layout.setContentsMargins(0, 0, 0, 0)
        
        email_label = QLabel("Email:")
        email_layout.addWidget(email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email (example@domain.com)")
        self.email_input.textChanged.connect(self.validate_email)
        email_layout.addWidget(self.email_input)
        
        # Email error label
        self.email_error = QLabel()
        self.email_error.setObjectName("error")
        self.email_error.setWordWrap(True)
        self.email_error.setAlignment(Qt.AlignLeft)
        self.email_error.hide()
        email_layout.addWidget(self.email_error)
        
        # Add email container to main layout
        layout.addWidget(email_container)
        
        layout.addSpacing(20)
        
        # Save button
        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(self.save_changes)
        layout.addWidget(self.save_button)
        
        # Cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.setProperty("danger", True)
        cancel_button.clicked.connect(self.close)
        layout.addWidget(cancel_button)
        
        layout.addStretch()
    
    def validate_email(self):
        email = self.email_input.text()
        
        if not email:  # Empty email is allowed
            self.email_input.setProperty("invalid", False)
            self.email_error.hide()
            self.save_button.setEnabled(True)
            self.email_input.style().unpolish(self.email_input)
            self.email_input.style().polish(self.email_input)
            return True
            
        # Simple email validation
        parts = email.split('@')
        if len(parts) != 2 or not parts[0] or not parts[1]:
            valid = False
        else:
            domain_parts = parts[1].split('.')
            valid = len(domain_parts) >= 2 and all(domain_parts)
        
        self.email_input.setProperty("invalid", not valid)
        
        if not valid:
            self.email_error.setText("Invalid email format.\nPlease use format: example@domain.com")
            self.email_error.show()
            self.save_button.setEnabled(False)
        else:
            self.email_error.hide()
            self.save_button.setEnabled(True)
        
        self.email_input.style().unpolish(self.email_input)
        self.email_input.style().polish(self.email_input)
        return valid
    
    def load_user_data(self):
        if self.current_row == -1:
            return
            
        model_index = self.user_model.index(self.current_row, 0)
        first_name = self.user_model.data(self.user_model.index(self.current_row, 1))
        last_name = self.user_model.data(self.user_model.index(self.current_row, 2))
        email = self.user_model.data(self.user_model.index(self.current_row, 3))
        
        self.first_name_input.setText(first_name or '')
        self.last_name_input.setText(last_name or '')
        self.email_input.setText(email or '')
    
    def save_changes(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        email = self.email_input.text()
        
        if email and not self.validate_email():
            QMessageBox.warning(self, "Error", "Please enter a valid email address")
            return
        
        success, message = self.user_model.update_user(
            self.current_login,
            first_name,
            last_name,
            email
        )
        
        if success:
            QMessageBox.information(self, "Success", "Profile updated successfully!")
            self.edit_successful.emit()
            self.close()
        else:
            QMessageBox.warning(self, "Error", message)
    
    def closeEvent(self, event):
        self.finished.emit()
        super().closeEvent(event) 
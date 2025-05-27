import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Signal, QObject

from models.user_model import UserModel
from views.login_window import LoginWindow
from views.register_window import RegisterWindow
from views.profile_window import ProfileWindow
from views.edit_window import EditWindow
from styles.utils import load_stylesheet

class UserManagementApp(QObject):
    def __init__(self):
        super().__init__()
        self.user_model = UserModel()
        self.current_login = None
        
        # Create windows
        self.login_window = LoginWindow(self.user_model)
        self.register_window = None
        self.profile_window = None
        self.edit_window = None
        
        # Connect signals
        self.login_window.login_successful.connect(self.on_login_successful)
        self.login_window.register_requested.connect(self.show_register_window)
        
        # Show login window
        self.login_window.show()
    
    def show_register_window(self, preset_login=""):
        self.register_window = RegisterWindow(self.user_model, preset_login)
        self.register_window.registration_successful.connect(self.on_login_successful)
        # Re-enable login window when registration window is closed
        self.register_window.finished.connect(self.login_window.enable_login)
        self.register_window.show()
    
    def on_login_successful(self, login, user_data):
        self.current_login = login
        
        # Close login and register windows if they exist
        if self.login_window:
            self.login_window.close()
        if self.register_window:
            self.register_window.close()
        
        # Show profile window
        self.profile_window = ProfileWindow(self.user_model, login)
        self.profile_window.edit_requested.connect(self.show_edit_window)
        self.profile_window.logout_requested.connect(self.logout)
        self.profile_window.show()
    
    def show_edit_window(self, login):
        self.edit_window = EditWindow(self.user_model, login)
        self.edit_window.edit_successful.connect(self.profile_window.load_user_data)
        self.edit_window.show()
    
    def logout(self):
        self.current_login = None
        
        # Close all windows
        if self.profile_window:
            self.profile_window.close()
        if self.edit_window:
            self.edit_window.close()
        
        # Show login window
        self.login_window = LoginWindow(self.user_model)
        self.login_window.login_successful.connect(self.on_login_successful)
        self.login_window.register_requested.connect(self.show_register_window)
        self.login_window.show()

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Load and apply stylesheet
    app.setStyleSheet(load_stylesheet())
    
    # Create and run application
    user_management = UserManagementApp()
    
    return app.exec()

if __name__ == '__main__':
    sys.exit(main()) 
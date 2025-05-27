# User Management Application

A desktop application for user management built with PySide6 (Qt for Python).

## Features

- User registration with password strength validation
- User authentication (login)
- Profile management (view and edit user information)
- Email validation
- Modern UI with consistent styling
- Real-time form validation

## Requirements

- Python 3.8+
- PySide6

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Install dependencies:
```bash
pip install PySide6
```

## Usage

Run the application:
```bash
python main.py
```

## Project Structure

- `main.py` - Application entry point
- `models/` - Data models and business logic
  - `user_model.py` - User data management
- `views/` - UI components
  - `login_window.py` - Login form
  - `register_window.py` - Registration form
  - `profile_window.py` - User profile view/edit
  - `edit_window.py` - Profile editing form
- `styles/` - QSS stylesheets
  - `main.qss` - Application styling 
# Flask Login Authentication

This project implements user authentication using Flask and Flask-Login. It provides functionality for user registration, login, logout, and protected routes that require authentication.

## Features

- **User Registration**: Allows new users to create an account.
- **User Login**: Existing users can log in with their credentials.
- **Session Management**: Flask-Login handles user sessions, making sure logged-in users can access restricted routes.
- **Protected Routes**: Certain pages or actions are restricted to logged-in users only.
- **User Logout**: Users can log out and end their session.

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/PrithaAgrawal/login_auth_flask.git
cd login_auth_flask
```
### 2. Set up the virtual environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment (Linux/macOS)
source venv/bin/activate

# Activate virtual environment (Windows)
venv\Scripts\activate
```
### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup
```postgre
python
>>> from app import db
>>> db.create_all()
```

### 5. Running the Application
**Start the Flask server using:**
```bash
flask run
```
**using the Python command:**
```bash
python app.py
```

### 6. Project structure:

**login_auth_flask/**
**│**
**├── app.py                  # Main application file**
**├── templates/              # HTML templates (includes: home.html, login.html, register.html, dashboard.html)**
**├── requirements.txt        # List of dependencies**
**└── venv/                   # Virtual environment directory (included in .gitignore)**


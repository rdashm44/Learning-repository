# Hunt Club Manager

A web application for managing a private hunt club with member authentication, stand check-in/out, and harvest logging.

## Features

- **User Authentication**: Register and login functionality with secure password hashing
- **User Permissions**: Admin and member roles with different access levels
- **Stand Management**: 
  - View available hunting stands
  - Check in to stands with capacity rules
  - Check out when done hunting
- **Active Hunter Dashboard**: Real-time view of who is currently hunting and which stand they're using
- **Harvest Log**: Track game harvests with details like game type, location, and notes
- **Admin Features**:
  - Add and manage hunting stands
  - View all users and their status

## Installation

1. Install Python 3.8 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Default Credentials

The application creates a default admin account:
- Username: `admin`
- Password: `admin123`

**Important**: Change the admin password after first login in a production environment.

## Usage

1. **Register**: Create a new account or use the admin credentials
2. **Dashboard**: View active hunters and their current stands
3. **Stands**: Check in to an available hunting stand
4. **Harvest Log**: Record your harvests with details
5. **Admin**: Manage stands and view all users (admin only)

## Stand Rules

- Users can only check in to one stand at a time
- Stands have a maximum capacity (default: 1 hunter)
- Users must check out before checking in to another stand
- Stand availability is shown in real-time

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite with Flask-SQLAlchemy
- **Authentication**: Flask-Login with Werkzeug password hashing
- **Frontend**: HTML templates with embedded CSS

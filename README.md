# Hunt Club Manager

A web application for managing a private hunt club with member authentication, stand check-in/out, and harvest logging.

## Getting the Code

### Option 1: Clone from GitHub
```bash
git clone https://github.com/rdashm44/Learning-repository.git
cd Learning-repository
```

### Option 2: Download ZIP
1. Download the repository as a ZIP file from GitHub
2. Extract it to a folder on your computer
3. Open a terminal and navigate to the extracted folder

## Working Directory

**The directory you should reference is the root folder of this repository.**

This is where you'll find:
- `app.py` - The main Flask application
- `requirements.txt` - Python dependencies
- `templates/` - HTML templates folder
- `README.md` - This file

### For Terminal/Command Line:
```bash
# Navigate to the repository folder
cd Learning-repository

# Or if you extracted/cloned to a specific location:
cd /path/to/Learning-repository

# Verify you're in the right place - you should see app.py
ls
# You should see: app.py  README.md  requirements.txt  templates
```

### For Claude Code / VS Code / IDEs:
- **Open Folder:** Select the `Learning-repository` folder (the root directory)
- **Working Directory:** This is where `app.py` is located
- All commands in this README should be run from this directory

### Directory Structure:
```
Learning-repository/          ← YOU ARE HERE (root directory)
├── app.py                     ← Main Flask application
├── requirements.txt           ← Python dependencies
├── README.md                  ← This documentation
├── .gitignore                 ← Git ignore rules
└── templates/                 ← HTML templates folder
    ├── base.html
    ├── login.html
    ├── dashboard.html
    └── ... (other templates)
```

## Quick Start - Opening the Application in Your Browser

**Prerequisites:** 
- Python 3.8 or higher installed on your system
- You're in the repository's root directory (where `app.py` is located)

1. **Install dependencies** (first time only):
   ```bash
   pip install -r requirements.txt
   ```
   
   > **Note:** If you get "File not found" error, make sure you're in the correct directory. Run `ls` (Mac/Linux) or `dir` (Windows) to check if you see `app.py` and `requirements.txt`

2. **Start the application:**
   ```bash
   python app.py
   ```
   
   You should see output like:
   ```
   ============================================================
   SECURITY WARNING: Default admin account created!
   Username: admin
   Password: admin123
   CHANGE THIS PASSWORD IMMEDIATELY!
   ============================================================
   Database initialized!
    * Serving Flask app 'app'
    * Debug mode: off
   WARNING: This is a development server. Do not use it in a production deployment.
    * Running on http://0.0.0.0:5000
   Press CTRL+C to quit
   ```

3. **Open your web browser** and navigate to:
   ```
   http://localhost:5000
   ```
   
   Alternative URLs that also work:
   - `http://127.0.0.1:5000`
   - `http://0.0.0.0:5000`

4. **Login** with the default credentials:
   - Username: `admin`
   - Password: `admin123`

You're now ready to use the Hunt Club Manager! 🦌

## 🎯 How to Use the Features - Complete Walkthrough

Once you have localhost open (see Quick Start above), here's how to explore all the features:

### 1. **Login to the System**

![Login Page](https://github.com/user-attachments/assets/556d716c-f4f0-4a55-b178-7194ce7df8d0)

- Enter username: `admin`
- Enter password: `admin123`
- Click "Login"
- You'll see a success message and be redirected to the dashboard

### 2. **View the Dashboard (Home Page)**

![Dashboard](https://github.com/user-attachments/assets/1159d9ec-22a3-4714-a5c2-84950bcba7bf)

The dashboard is your home base and shows:
- **Currently Hunting** section: Real-time list of all active hunters
- **Your Active Hunt** box: If you're checked in, shows which stand you're at
- Quick action buttons to check in or view harvest log

**What you can do:**
- See who else is hunting and where they are
- Click "Check In to a Stand" to start hunting
- Click "View Harvest Log" to log or view harvests

### 3. **Check In to a Hunting Stand**

![Hunting Stands](https://github.com/user-attachments/assets/c8fbd038-85bb-4c1b-b08f-317a2deba854)

Click "Stands" in the navigation menu to see all available stands:
- **4 pre-configured stands**: North Ridge, Creek Bottom, Oak Grove, South Field
- Each stand shows:
  - Description of location
  - Capacity (current/maximum hunters)
  - Availability status (Available/Full)
- **Green "Check In" button**: Click to check in to that stand

**Rules:**
- You can only check in to one stand at a time
- Stands have maximum capacity (some allow multiple hunters)
- You must check out before checking in to another stand

### 4. **Track Your Active Hunt**

![Active Hunter Dashboard](https://github.com/user-attachments/assets/387c8f3b-c51e-4882-8036-25e28cdc51b8)

After checking in, the dashboard updates to show:
- **Your Active Hunt** (highlighted in green):
  - Which stand you're at
  - When you checked in
  - Red "Check Out" button when you're done
- **Currently Hunting table**: 
  - Shows all active hunters (including you)
  - Stand locations
  - Check-in times
  - Status badges

**What you can do:**
- Click "Check Out" when you're done hunting
- See real-time updates of who else is hunting

### 5. **Log Your Harvests**

![Harvest Log](https://github.com/user-attachments/assets/0bdc6cbe-a702-4da8-9d3a-93ae6b901c41)

Click "Harvest Log" in the navigation menu:
- **Log New Harvest** form at the top:
  - **Game Type** (required): e.g., "White-tail Buck", "Doe", "Turkey"
  - **Location**: e.g., "North Ridge", "Oak Grove"
  - **Notes**: Add details like weight, points, field conditions
  - Click "Log Harvest" to save
- **Harvest History** table below:
  - Shows all logged harvests from all members
  - Includes date, hunter, game type, location, and notes
  - Most recent harvests appear first

### 6. **Admin: Manage Stands** (Admin Only)

![Manage Stands](https://github.com/user-attachments/assets/e17db5fa-0aed-4d9b-9b6a-1ae37b0b8001)

If you're logged in as admin, click "Manage Stands":
- **Add New Stand** form:
  - Stand Name (required)
  - Description
  - Maximum Hunters (default: 1)
  - Click "Add Stand" to create
- **Existing Stands** table:
  - Lists all stands with their details
  - Shows current capacity and active hunter count
  - Status indicators (Available/Full)

### 7. **Admin: View Users** (Admin Only)

Click "Users" in the navigation menu:
- See all registered users
- View each user's role (Admin/Member)
- Check if users are currently hunting (Active/Inactive status)

### 8. **Logout**

When you're done:
- Click "Logout (admin)" in the top navigation
- You'll be redirected back to the login page

---

## 💡 Quick Tips

- **Navigation Bar**: Always visible at the top with links to all features
- **Success Messages**: Green notifications appear when actions complete
- **Stand Capacity**: Pay attention to capacity - you can't check in if a stand is full
- **Real-Time Updates**: Refresh the dashboard to see latest active hunters
- **Harvest Log**: Open to all members - everyone can see all harvests
- **Admin Features**: Only visible if logged in as admin

### Troubleshooting

**Problem:** "Address already in use" or "Port 5000 is in use"  
**Solution:** Another application is using port 5000. Either:
- Stop the other application
- Or modify `app.py` to use a different port (e.g., change `port=5000` to `port=5001`)

**Problem:** Can't connect to the server  
**Solution:** 
- Make sure the `python app.py` command is still running
- Check for any error messages in the terminal
- Try accessing `http://127.0.0.1:5000` instead

**Problem:** Page not found or blank page  
**Solution:**
- Clear your browser cache
- Try a different browser
- Check the terminal for any error messages

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

## Installation & Setup

See the **Quick Start** section above for step-by-step instructions.

For development:
1. Install Python 3.8 or higher
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python app.py`
4. Open browser to: `http://localhost:5000`

## Default Credentials

The application creates a default admin account on first run:
- Username: `admin`
- Password: `admin123`

**⚠️ SECURITY WARNING**: This default password is for development only. In production:
1. Change the admin password immediately after first login
2. Set a strong SECRET_KEY environment variable
3. Use HTTPS for all connections
4. Consider implementing mandatory password change on first login

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

## Environment Variables

For production deployment, set these environment variables:
- `SECRET_KEY`: A strong random secret key for session security
- `FLASK_DEBUG`: Set to `true` only for development (default: `false`)

<!-- ## How to setup your project

1. `python3.11 -m venv venv && source venv/bin/activate`
2. `pip install --upgrade pip`
3. (optional):
   - `pip install pip-tools`
   - `pip-compile --resolver=backtracking requirements.in`
4. `pip install -r requirements.txt`

# Initialise the migrations
flask db init

# Generate migration (if using Flask-Migrate)
flask db migrate

# Apply migration to create database tables
flask db upgrade

# Start Flask application
python3 -m backend.app
 or
cd backend
flask run

# start vue application
cd client
nvm use 14
npm run dev -->



<!-- -------- -->


# UAV Monitoring System

## Overview
This project is a UAV (Unmanned Aerial Vehicle) monitoring system built with Flask (backend) and Vue.js (frontend). It allows users to manage drones, tasks, and captured images associated with those tasks.

## Setup Instructions

### Backend Setup
1. Create a virtual environment: 
   ```
   python3.11 -m venv venv && source venv/bin/activate
   ```

2. Upgrade pip:
   ```
   pip install --upgrade pip
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Initialize the migrations:
   ```
   flask db init
   ```

5. Generate migration:
   ```
   flask db migrate
   ```

6. Apply migration to create database tables:
   ```
   flask db upgrade
   ```

7. Start the Flask application:
   ```
   python3 -m backend.app
   ```

### Frontend Setup
1. Install Node.js dependencies:
   ```
   cd client
   npm install
   ```

2. Compile and hot-reload for development:
   ```
   nvm use 14
   npm run dev
   ```

3. Compile and minify for production:
   ```
   npm run build
   ```

## Additional Notes
- Ensure you have Node.js and npm installed on your system for the frontend setup.
- The backend runs on Flask, and the frontend is developed using Vue.js.
- The project uses Flask-Migrate for database migrations and SQLAlchemy as the ORM.


This README provides clear setup instructions for both the backend and frontend, along with some additional notes about the project.
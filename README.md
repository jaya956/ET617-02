# Explanation of the website project:
Basically we built a learning platform which secretly watches what people do and tells teachers(admin) everything.

## What does it do?

### For Students:
- Sign up and log in
- Take online courses (read, watch videos, do quizzes)

### For Teachers:
- See exactly what every student does
- Know who clicked what, when, and where
- Download reports to understand student behavior

## The "Spy" System (Clickstream Tracking):
### The website tracks:
- Every page visit (when someone goes to a page)
- Every button click (what buttons they press)
- Video actions (play, pause, rewind)
- Quiz answers (what they answered, if they got it right)
- IP addresses (where they're accessing from)
 
 ## How we built this step by step:

### Step 1: Set Up the Foundation:
  We created a Flask website with:
- User registration and login
- Course management system
- Database to store everything

### Step 2: Added the "Spy" System
 We built a tracking system that:
- Records every user action
- Stores data in a database
- Works even when users aren't logged in

### Step 3: Created the Admin Dashboard
 We made special pages for teachers to:
- See real-time user activity
- View detailed reports
- Export data to Excel

### To enhance the Admin System:
- Created a new detailed user activity page
- Added filtering and search capabilities
- Made the data display match our exact requirements
- Fixed Issues: Corrected database paths

###  Testing and Launch:
- Started the application
- Verified it was working
- Tested all features

## Important Elements in the project:
- Every action is recorded instantly
- No delay in data collection
- Works for both logged-in and anonymous users
- Export Capabilities: Download data as Excel files

## How to Use It:

### For Students:
- Go to http://localhost:5000
- Register an account
- Browse courses and take lessons
- The system automatically tracks everything you do

### For Teachers/Admins:
- Go to http://localhost:5000/admin/login
- Login with: username = admin, password = admin123
- View the dashboard to see user activity
- Click "User Activity" for detailed tracking
- Export data to Excel for analysis

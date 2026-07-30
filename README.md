# Online Course Registration System

A complete Python-based course registration system with Tkinter GUI for managing student enrollments and course administration.

## Features

### Student Features
- **Account Registration**: Students can create new accounts with username, password, and email
- **Login**: Secure authentication with password encryption
- **View Available Courses**: Browse all available courses with details
- **Search Courses**: Search courses by code, name, or description
- **Enroll in Courses**: Register for courses with capacity checking
- **View Enrolled Courses**: See all courses the student is enrolled in
- **Drop Courses**: Remove enrollment from courses

### Administrator Features
- **Add Courses**: Create new courses with code, name, description, credits, and capacity
- **Remove Courses**: Delete courses and associated enrollments
- **View All Students**: Monitor registered students
- **Generate Reports**: 
  - Enrollment reports showing all student-course enrollments
  - Course statistics reports showing capacity and fill percentages
- **Export Reports**: Export reports to CSV format

### Technical Features
- **Object-Oriented Programming**: Clean OOP design with inheritance
- **SQLite Database**: Persistent data storage
- **Password Encryption**: SHA-256 hashing for secure password storage
- **Exception Handling**: Comprehensive error handling throughout
- **Input Validation**: Form validation for all user inputs
- **User-Friendly GUI**: Modern Tkinter interface with tabbed navigation
- **Search Functionality**: Real-time search for courses

## Installation

### Requirements
- Python 3.6 or higher
- Tkinter (usually included with Python)
- SQLite3 (included with Python)

### Setup
1. Clone or download the project files
2. Ensure all Python files are in the same directory:
   - `main.py`
   - `gui.py`
   - `database.py`
   - `models.py`
   - `auth.py`

No additional packages need to be installed as the system uses only Python standard library modules.

## Usage

### Running the Application
```bash
python main.py
```

### Default Administrator Account
- **Username**: `admin`
- **Password**: `admin123`

### Student Registration
1. Click "Register as Student" on the login screen
2. Fill in the registration form:
   - Full Name
   - Username
   - Email
   - Password (minimum 6 characters)
   - Confirm Password
3. Click "Register" to create the account
4. Login with your credentials

### Student Dashboard
The student dashboard has two tabs:

**Available Courses Tab**
- View all available courses
- Search courses by code, name, or description
- Select a course and click "Enroll" to register
- View course details including capacity and available seats

**My Courses Tab**
- View all enrolled courses
- See enrollment dates
- Drop courses by selecting and clicking "Drop Selected Course"

### Administrator Dashboard
The admin dashboard has three tabs:

**Manage Courses Tab**
- Add new courses with code, name, description, credits, and capacity
- View all courses in a table
- Remove courses (also removes all associated enrollments)

**View Students Tab**
- View all registered students
- See student details including registration date

**Reports Tab**
- Generate Enrollment Report: Shows all student-course enrollments
- Generate Course Statistics: Shows course capacity and fill percentages
- Export reports to CSV format

## Project Structure

```
question 7 new/
├── main.py              # Application entry point
├── gui.py               # Tkinter GUI implementation
├── database.py          # SQLite database operations
├── models.py            # OOP models (User, Student, Administrator, Course)
├── auth.py              # Authentication and session management
├── README.md            # This file
└── TECHNICAL_REPORT.md  # Detailed technical documentation
```

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `password`: Hashed password (SHA-256)
- `full_name`: Student/admin full name
- `email`: Unique email address
- `role`: 'student' or 'admin'
- `created_at`: Registration timestamp

### Courses Table
- `id`: Primary key
- `course_code`: Unique course code
- `course_name`: Course name
- `description`: Course description
- `credits`: Credit hours
- `capacity`: Maximum enrollment
- `enrolled_count`: Current enrollment count
- `created_at`: Creation timestamp

### Enrollments Table
- `id`: Primary key
- `student_id`: Foreign key to users table
- `course_id`: Foreign key to courses table
- `enrollment_date`: Enrollment timestamp
- Unique constraint on (student_id, course_id)

## Security Features

- **Password Encryption**: All passwords are hashed using SHA-256 before storage
- **SQL Injection Prevention**: Parameterized queries for all database operations
- **Input Validation**: All user inputs are validated before processing
- **Role-Based Access**: Separate interfaces for students and administrators

## Error Handling

The system includes comprehensive exception handling:
- Database connection errors
- Duplicate registration attempts
- Invalid login credentials
- Course capacity limits
- Input validation errors
- File export errors

## Bonus Features Implemented

✅ **GUI using Tkinter**: Complete graphical user interface
✅ **Password Encryption**: SHA-256 hashing for passwords
✅ **Export Reports to CSV**: Export enrollment and statistics reports
✅ **Search Functionality**: Real-time search for courses

## Screenshots

### Login Screen
- Clean login interface with username and password fields
- Registration button for new students
- Enter key support for quick login

### Student Dashboard
- Tabbed interface for Available Courses and My Courses
- Search functionality for courses
- Course details table with capacity information
- Enroll and drop functionality

### Administrator Dashboard
- Tabbed interface for course management, student view, and reports
- Course addition form with validation
- Student listing with registration details
- Report generation and CSV export

## Troubleshooting

### Database Not Created
The system automatically creates the SQLite database on first run. If you encounter database errors:
1. Delete `course_registration.db` if it exists
2. Run the application again

### Login Issues
- Ensure you're using the correct credentials
- For admin: username `admin`, password `admin123`
- For students: use the credentials you registered with

### GUI Not Displaying
- Ensure Tkinter is installed (comes with Python by default)
- On Linux: `sudo apt-get install python3-tk`
- On macOS: Tkinter is included with Python installation

## Future Enhancements

Potential improvements for future versions:
- Email verification for registration
- Password reset functionality
- Course prerequisites
- Waitlist functionality for full courses
- Grade tracking
- Schedule conflict detection
- PDF report export
- Multi-language support

## Author

Online Course Registration System
Python Mini-Project

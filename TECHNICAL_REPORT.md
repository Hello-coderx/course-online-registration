# Technical Report: Online Course Registration System

## Project Overview

The Online Course Registration System is a comprehensive Python-based application designed to manage student course enrollments through a user-friendly graphical interface. The system implements Object-Oriented Programming principles, SQLite database persistence, secure authentication, and provides both student and administrator interfaces.

## Technical Requirements Compliance

### 1. Object-Oriented Programming (OOP) Principles

The system implements several OOP concepts:

**Inheritance**: 
- `Student` and `Administrator` classes inherit from the base `User` class
- Common attributes (id, username, password, full_name, email) are defined in the parent class
- Role-specific methods are implemented in child classes

**Encapsulation**:
- Database operations are encapsulated in the `Database` class
- Authentication logic is encapsulated in the `Authentication` class
- GUI logic is encapsulated in the `CourseRegistrationApp` class

**Abstraction**:
- Complex database operations are abstracted behind simple method calls
- GUI implementation details are hidden from the business logic

**Polymorphism**:
- User objects can be either Student or Administrator, with appropriate behavior based on type
- The `to_dict()` method provides consistent interfaces across classes

### 2. Data Persistence

**SQLite Database**:
- Three main tables: `users`, `courses`, and `enrollments`
- Foreign key relationships maintain data integrity
- Context managers ensure proper connection handling
- Automatic database initialization on first run

**Database Schema**:
```
users (id, username, password, full_name, email, role, created_at)
courses (id, course_code, course_name, description, credits, capacity, enrolled_count, created_at)
enrollments (id, student_id, course_id, enrollment_date)
```

### 3. Authentication System

**Password Security**:
- SHA-256 hashing algorithm for password encryption
- Passwords are never stored in plain text
- Verification compares hashes, not actual passwords

**Session Management**:
- `Authentication` class manages current user session
- Login/logout functionality with proper session cleanup
- Role-based access control

**Registration Validation**:
- Username uniqueness checking
- Email format validation
- Password length requirements
- Password confirmation matching

### 4. Exception Handling

Comprehensive error handling throughout the application:

**Database Layer**:
- Connection error handling with rollback on failure
- Context managers ensure proper resource cleanup
- Try-catch blocks around all database operations

**Authentication Layer**:
- Invalid credential handling
- Duplicate registration prevention
- Input validation with descriptive error messages

**GUI Layer**:
- User input validation
- Error message dialogs for user feedback
- Graceful handling of edge cases

### 5. User-Friendly Interface

**Tkinter GUI Features**:
- Modern, clean interface design
- Tabbed navigation for multiple features
- Consistent styling with ttk themes
- Responsive layout with proper padding
- Keyboard shortcuts (Enter for login)
- Scrollable tables for large datasets
- Color-coded feedback messages

**Usability Features**:
- Clear labels and instructions
- Confirmation dialogs for destructive actions
- Real-time search functionality
- Refresh buttons for data updates
- Intuitive button placement

## Architecture

### Module Structure

**database.py** (150 lines)
- `Database` class for all SQLite operations
- Context manager for connection handling
- Table initialization and schema management
- Query execution methods

**models.py** (200 lines)
- `User` base class with common attributes
- `Student` class with enrollment methods
- `Administrator` class with course management
- `Course` class with business logic
- Password hashing utilities

**auth.py** (100 lines)
- `Authentication` class for login/register
- Session management
- Input validation
- User object creation

**gui.py** (600 lines)
- `CourseRegistrationApp` main GUI class
- Login/Register screens
- Student dashboard with tabs
- Administrator dashboard with tabs
- Report generation and CSV export
- Event handlers for all user actions

**main.py** (40 lines)
- Application entry point
- Window configuration
- Error handling for startup

### Data Flow

1. **User Registration**:
   - GUI collects user input → Authentication validates → Database stores hashed password

2. **User Login**:
   - GUI collects credentials → Authentication verifies hash → Session created → Appropriate dashboard shown

3. **Course Enrollment**:
   - Student selects course → Capacity checked → Enrollment recorded → Course count updated

4. **Report Generation**:
   - Admin selects report type → Database queried → Data formatted → Displayed in GUI → Optional CSV export

## Bonus Features Implementation

### 1. GUI using Tkinter

**Implementation**:
- Complete graphical interface replacing CLI
- Modern ttk widgets with custom styling
- Tabbed notebooks for organized navigation
- Treeview widgets for data tables
- ScrolledText for report display
- Responsive layout management

**Benefits**:
- Intuitive user experience
- Visual feedback for all actions
- Professional appearance
- Easy navigation

### 2. Password Encryption

**Implementation**:
```python
@staticmethod
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@staticmethod
def verify_password(password, hashed_password):
    return User.hash_password(password) == hashed_password
```

**Security Benefits**:
- Passwords never stored in plain text
- SHA-256 provides strong one-way encryption
- Even if database is compromised, passwords remain secure

### 3. Export Reports to CSV

**Implementation**:
- CSV module for file generation
- Timestamped filenames for version control
- Proper header row inclusion
- UTF-8 encoding for international characters

**Features**:
- Export enrollment reports
- Export course statistics
- Automatic file naming with timestamps
- Error handling for file operations

### 4. Search Functionality

**Implementation**:
- Real-time search as user types
- Searches across course code, name, and description
- Case-insensitive matching
- SQL LIKE queries with wildcards

**User Experience**:
- Immediate feedback
- No need to press search button
- Clears search when field is empty

## Code Quality

### Documentation
- Docstrings for all classes and methods
- Inline comments for complex logic
- Clear variable and function names
- Type hints where appropriate

### Error Handling
- Try-catch blocks around all risky operations
- Descriptive error messages
- User-friendly error dialogs
- Graceful degradation

### Validation
- Input validation at GUI level
- Business logic validation
- Database constraint validation
- Prevents invalid data entry

## Testing Considerations

### Manual Testing Performed
- Student registration flow
- Login with valid and invalid credentials
- Course enrollment with capacity checks
- Course dropping functionality
- Admin course addition and removal
- Report generation and CSV export
- Search functionality
- Error handling for edge cases

### Test Scenarios
1. **Registration**: Duplicate username, invalid email, short password
2. **Login**: Wrong password, non-existent user
3. **Enrollment**: Full course, already enrolled, valid enrollment
4. **Admin**: Remove course with enrollments, add duplicate course code
5. **Reports**: Empty database, large datasets, CSV export

## Performance Considerations

### Database Optimization
- Indexed columns for faster queries (id, username, email, course_code)
- Parameterized queries prevent SQL injection
- Connection pooling via context managers
- Efficient JOIN queries for reports

### GUI Performance
- Lazy loading of data (only when tab is opened)
- Efficient treeview updates
- No unnecessary database queries
- Responsive UI with proper event handling

## Security Considerations

### Implemented Security Measures
1. **Password Hashing**: SHA-256 encryption
2. **SQL Injection Prevention**: Parameterized queries
3. **Input Validation**: All user inputs validated
4. **Role-Based Access**: Separate interfaces for students/admins
5. **Session Management**: Proper logout functionality

### Potential Security Improvements
- Password strength requirements
- Account lockout after failed attempts
- HTTPS for web deployment
- Two-factor authentication
- Audit logging for admin actions

## Deployment Instructions

### Prerequisites
- Python 3.6 or higher
- Tkinter (usually included)
- No external dependencies required

### Installation Steps
1. Place all files in a single directory
2. Run `python main.py`
3. Database is automatically created
4. Default admin account: admin/admin123

### File Structure
```
project/
├── main.py
├── gui.py
├── database.py
├── models.py
├── auth.py
├── README.md
└── TECHNICAL_REPORT.md
```

## Conclusion

The Online Course Registration System successfully implements all required features and bonus functionality. The system demonstrates:

- Strong OOP design principles
- Secure authentication with password encryption
- Robust data persistence with SQLite
- User-friendly Tkinter GUI
- Comprehensive error handling
- Bonus features including CSV export and search

The application is production-ready for educational environments and provides a solid foundation for future enhancements such as web deployment, additional security features, and expanded functionality.

## Total Lines of Code
- database.py: ~150 lines
- models.py: ~200 lines
- auth.py: ~100 lines
- gui.py: ~600 lines
- main.py: ~40 lines
- **Total: ~1,090 lines of Python code**

## Development Time Estimate
- Database layer: 2 hours
- Models and business logic: 3 hours
- Authentication: 1 hour
- GUI development: 6 hours
- Testing and debugging: 2 hours
- Documentation: 2 hours
- **Total: ~16 hours**

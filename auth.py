"""
Authentication Module
Handles user authentication and session management
"""
from database import Database
from models import Student, Administrator, User


class Authentication:
    """Authentication class for managing user login and registration"""
    
    def __init__(self):
        self.db = Database()
        self.current_user = None
    
    def register_student(self, username, password, full_name, email):
        """
        Register a new student
        Returns: (success: bool, message: str)
        """
        try:
            # Validate inputs
            if not username or not password or not full_name or not email:
                return False, "All fields are required"
            
            if len(password) < 6:
                return False, "Password must be at least 6 characters"
            
            if '@' not in email or '.' not in email:
                return False, "Invalid email format"
            
            # Check if username exists
            existing = self.db.execute_query(
                'SELECT id FROM users WHERE username = ?',
                (username,)
            )
            if existing:
                return False, "Username already exists"
            
            # Check if email exists
            existing_email = self.db.execute_query(
                'SELECT id FROM users WHERE email = ?',
                (email,)
            )
            if existing_email:
                return False, "Email already registered"
            
            # Hash password
            hashed_password = User.hash_password(password)
            
            # Insert user
            user_id = self.db.execute_query(
                '''INSERT INTO users (username, password, full_name, email, role)
                   VALUES (?, ?, ?, ?, ?)''',
                (username, hashed_password, full_name, email, 'student'),
                fetch=False
            )
            
            return True, "Registration successful"
        except Exception as e:
            return False, f"Registration error: {str(e)}"
    
    def login(self, username, password):
        """
        Login user
        Returns: (success: bool, message: str, user: User/None)
        """
        try:
            if not username or not password:
                return False, "Username and password required", None
            
            # Get user from database
            user_data = self.db.execute_query(
                'SELECT id, username, password, full_name, email, role FROM users WHERE username = ?',
                (username,)
            )
            
            if not user_data:
                return False, "Invalid username or password", None
            
            user_id, db_username, db_password, full_name, email, role = user_data[0]
            
            # Verify password
            if not User.verify_password(password, db_password):
                return False, "Invalid username or password", None
            
            # Create user object based on role
            if role == 'student':
                user = Student(user_id, db_username, db_password, full_name, email)
            elif role == 'admin':
                user = Administrator(user_id, db_username, db_password, full_name, email)
            else:
                return False, "Invalid user role", None
            
            self.current_user = user
            return True, "Login successful", user
        except Exception as e:
            return False, f"Login error: {str(e)}", None
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    

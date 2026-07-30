"""
Database Module
Handles SQLite database operations for the Course Registration System
"""
import sqlite3
import hashlib
from contextlib import contextmanager


class Database:
    """Database class for managing SQLite operations"""
    
    def __init__(self, db_name="course_registration.db"):
        """Initialize database connection"""
        self.db_name = db_name
        self.initialize_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def initialize_database(self):
        """Create all necessary tables if they don't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table (for both students and admins)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('student', 'admin')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Courses table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_code TEXT UNIQUE NOT NULL,
                    course_name TEXT NOT NULL,
                    description TEXT,
                    credits INTEGER NOT NULL,
                    capacity INTEGER NOT NULL,
                    enrolled_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Enrollments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS enrollments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    course_id INTEGER NOT NULL,
                    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES users(id),
                    FOREIGN KEY (course_id) REFERENCES courses(id),
                    UNIQUE(student_id, course_id)
                )
            ''')
            
            # Create default admin if not exists (password is hashed)
            hashed_password = hashlib.sha256('admin123'.encode()).hexdigest()
            cursor.execute('''
                INSERT OR IGNORE INTO users (username, password, full_name, email, role)
                VALUES (?, ?, ?, ?, ?)
            ''', ('admin', hashed_password, 'System Administrator', 'admin@system.com', 'admin'))
            
            conn.commit()
    
    def execute_query(self, query, params=None, fetch=True):
        """
        Execute a SQL query
        Args:
            query: SQL query string
            params: Parameters for the query
            fetch: Whether to fetch results
        Returns:
            Query results if fetch=True, else None
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                return cursor.fetchall()
            return cursor.lastrowid
    

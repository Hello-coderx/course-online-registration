"""
Models Module
Contains OOP classes for Student, Course, and Enrollment
"""
import hashlib
from database import Database


class User:
    """Base class for all users"""
    
    def __init__(self, user_id, username, password, full_name, email, role):
        self.id = user_id
        self.username = username
        self.password = password
        self.full_name = full_name
        self.email = email
        self.role = role
    
    @staticmethod
    def hash_password(password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password, hashed_password):
        """Verify password against hash"""
        return User.hash_password(password) == hashed_password
    


class Student(User):
    """Student class inheriting from User"""
    
    def __init__(self, user_id, username, password, full_name, email):
        super().__init__(user_id, username, password, full_name, email, 'student')
        self.db = Database()
    
    def enroll_in_course(self, course_id):
        """Enroll student in a course"""
        try:
            # Check if already enrolled
            existing = self.db.execute_query(
                'SELECT id FROM enrollments WHERE student_id = ? AND course_id = ?',
                (self.id, course_id)
            )
            if existing:
                return False, "Already enrolled in this course"
            
            # Check course capacity
            course = self.db.execute_query(
                'SELECT capacity, enrolled_count FROM courses WHERE id = ?',
                (course_id,)
            )
            if not course:
                return False, "Course not found"
            
            capacity, enrolled = course[0]
            if enrolled >= capacity:
                return False, "Course is full"
            
            # Enroll student
            self.db.execute_query(
                'INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)',
                (self.id, course_id),
                fetch=False
            )
            
            # Update enrolled count
            self.db.execute_query(
                'UPDATE courses SET enrolled_count = enrolled_count + 1 WHERE id = ?',
                (course_id,),
                fetch=False
            )
            
            return True, "Successfully enrolled"
        except Exception as e:
            return False, f"Error enrolling: {str(e)}"
    
    def get_enrolled_courses(self):
        """Get all courses the student is enrolled in"""
        try:
            query = '''
                SELECT c.id, c.course_code, c.course_name, c.description, 
                       c.credits, c.capacity, c.enrolled_count
                FROM courses c
                JOIN enrollments e ON c.id = e.course_id
                WHERE e.student_id = ?
            '''
            return self.db.execute_query(query, (self.id,))
        except Exception as e:
            print(f"Error getting enrolled courses: {e}")
            return []
    
    def drop_course(self, course_id):
        """Drop a course"""
        try:
            # Check if enrolled
            existing = self.db.execute_query(
                'SELECT id FROM enrollments WHERE student_id = ? AND course_id = ?',
                (self.id, course_id)
            )
            if not existing:
                return False, "Not enrolled in this course"
            
            # Remove enrollment
            self.db.execute_query(
                'DELETE FROM enrollments WHERE student_id = ? AND course_id = ?',
                (self.id, course_id),
                fetch=False
            )
            
            # Update enrolled count
            self.db.execute_query(
                'UPDATE courses SET enrolled_count = enrolled_count - 1 WHERE id = ?',
                (course_id,),
                fetch=False
            )
            
            return True, "Successfully dropped course"
        except Exception as e:
            return False, f"Error dropping course: {str(e)}"


class Administrator(User):
    """Administrator class inheriting from User"""
    
    def __init__(self, user_id, username, password, full_name, email):
        super().__init__(user_id, username, password, full_name, email, 'admin')
        self.db = Database()
    
    def add_course(self, course_code, course_name, description, credits, capacity):
        """Add a new course"""
        try:
            # Check if course code exists
            existing = self.db.execute_query(
                'SELECT id FROM courses WHERE course_code = ?',
                (course_code,)
            )
            if existing:
                return False, "Course code already exists"
            
            self.db.execute_query(
                '''INSERT INTO courses (course_code, course_name, description, credits, capacity)
                   VALUES (?, ?, ?, ?, ?)''',
                (course_code, course_name, description, credits, capacity),
                fetch=False
            )
            return True, "Course added successfully"
        except Exception as e:
            return False, f"Error adding course: {str(e)}"
    
    def remove_course(self, course_id):
        """Remove a course"""
        try:
            # Check if course exists
            existing = self.db.execute_query(
                'SELECT id FROM courses WHERE id = ?',
                (course_id,)
            )
            if not existing:
                return False, "Course not found"
            
            # Remove all enrollments for this course
            self.db.execute_query(
                'DELETE FROM enrollments WHERE course_id = ?',
                (course_id,),
                fetch=False
            )
            
            # Remove course
            self.db.execute_query(
                'DELETE FROM courses WHERE id = ?',
                (course_id,),
                fetch=False
            )
            return True, "Course removed successfully"
        except Exception as e:
            return False, f"Error removing course: {str(e)}"
    
    def get_all_students(self):
        """Get all students"""
        try:
            return self.db.execute_query(
                'SELECT id, username, full_name, email, created_at FROM users WHERE role = ?',
                ('student',)
            )
        except Exception as e:
            print(f"Error getting students: {e}")
            return []
    
    def get_all_courses(self):
        """Get all courses"""
        try:
            return self.db.execute_query(
                'SELECT id, course_code, course_name, description, credits, capacity, enrolled_count FROM courses'
            )
        except Exception as e:
            print(f"Error getting courses: {e}")
            return []
    
    def get_enrollment_report(self):
        """Generate enrollment report"""
        try:
            query = '''
                SELECT 
                    u.id, u.username, u.full_name, u.email,
                    c.course_code, c.course_name, c.credits,
                    e.enrollment_date
                FROM enrollments e
                JOIN users u ON e.student_id = u.id
                JOIN courses c ON e.course_id = c.id
                ORDER BY u.full_name, c.course_code
            '''
            return self.db.execute_query(query)
        except Exception as e:
            print(f"Error generating report: {e}")
            return []
    
    def get_course_statistics(self):
        """Get course enrollment statistics"""
        try:
            query = '''
                SELECT 
                    c.course_code, c.course_name, c.capacity, c.enrolled_count,
                    ROUND((c.enrolled_count * 100.0 / c.capacity), 2) as fill_percentage
                FROM courses c
                ORDER BY fill_percentage DESC
            '''
            return self.db.execute_query(query)
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return []

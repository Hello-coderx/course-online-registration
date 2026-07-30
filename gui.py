"""
GUI Module
Tkinter-based graphical user interface for the Course Registration System
Beautiful, colorful, and responsive design
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from auth import Authentication
from database import Database
import csv
from datetime import datetime


class CourseRegistrationApp:
    """Main application class for the Course Registration System"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Online Course Registration System")
        self.root.geometry("1000x750")
        
        self.auth = Authentication()
        self.db = Database()
        self.current_user = None
        
        # Color scheme for beautiful UI
        self.colors = {
            'login_bg': 'darkgreen',
            'login_card': 'white',
            'student_bg': 'lightblue',
            'admin_bg': 'navajowhite',
            'primary': 'blue',
            'success': 'green',
            'danger': 'red',
            'warning': 'orange',
            'info': 'dodgerblue',
            'text_dark': 'black',
            'text_light': 'white'
        }
        
        # Show login screen
        self.show_login_screen()
    
    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_colored_button(self, parent, text, command, bg_color, fg_color='#FFFFFF', width=15):
        """Create a colored button with consistent styling and hover effects"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=fg_color,
            font=('Arial', 11, 'bold'),
            width=width,
            height=2,
            relief='raised',
            cursor='hand2',
            activebackground=self.darken_color(bg_color),
            activeforeground=fg_color,
            borderwidth=2
        )
        return btn
    
    def darken_color(self, color, factor=0.8):
        """Darken a color for button hover effects (works with color names)"""
        # For color names, just return the same color (Tkinter handles hover automatically)
        return color
    
    def show_login_screen(self):
        """Display login screen with green background and admin credentials"""
        self.clear_window()
        self.root.configure(bg=self.colors['login_bg'])
        
        # Main container centered on screen
        main_frame = tk.Frame(self.root, bg=self.colors['login_bg'])
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # White login card
        login_card = tk.Frame(main_frame, bg=self.colors['login_card'], padx=50, pady=40)
        login_card.pack()
        
        # Title
        title_label = tk.Label(
            login_card,
            text="Course Registration System",
            bg=self.colors['login_card'],
            fg=self.colors['text_dark'],
            font=('Arial', 28, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Username
        tk.Label(
            login_card,
            text="Username:",
            bg=self.colors['login_card'],
            fg=self.colors['text_dark'],
            font=('Arial', 12, 'bold')
        ).grid(row=1, column=0, sticky='w', pady=10)
        
        self.login_username = tk.Entry(
            login_card,
            font=('Arial', 12),
            width=25,
            relief='solid',
            borderwidth=2
        )
        self.login_username.grid(row=1, column=1, pady=10, padx=10)
        
        # Password
        tk.Label(
            login_card,
            text="Password:",
            bg=self.colors['login_card'],
            fg=self.colors['text_dark'],
            font=('Arial', 12, 'bold')
        ).grid(row=2, column=0, sticky='w', pady=10)
        
        self.login_password = tk.Entry(
            login_card,
            font=('Arial', 12),
            width=25,
            show='*',
            relief='solid',
            borderwidth=2
        )
        self.login_password.grid(row=2, column=1, pady=10, padx=10)
        
        # Login Button
        login_btn = self.create_colored_button(
            login_card,
            "Login",
            self.handle_login,
            self.colors['primary']
        )
        login_btn.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Register Button
        register_btn = self.create_colored_button(
            login_card,
            "Register as Student",
            self.show_register_screen,
            self.colors['success'],
            width=20
        )
        register_btn.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Admin credentials display
        credentials_label = tk.Label(
            login_card,
            text="Admin Credentials: Username: admin | Password: admin123",
            bg=self.colors['login_card'],
            fg=self.colors['danger'],
            font=('Arial', 10, 'bold')
        )
        credentials_label.grid(row=5, column=0, columnspan=2, pady=15)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda e: self.handle_login())
        
        # Focus on username
        self.login_username.focus()
    
    def show_register_screen(self):
        """Display student registration screen with green background"""
        self.clear_window()
        self.root.configure(bg=self.colors['login_bg'])
        
        # Main container centered on screen
        main_frame = tk.Frame(self.root, bg=self.colors['login_bg'])
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # White registration card
        register_card = tk.Frame(main_frame, bg=self.colors['login_card'], padx=50, pady=40)
        register_card.pack()
        
        # Title
        title_label = tk.Label(
            register_card,
            text="Student Registration",
            bg=self.colors['login_card'],
            fg=self.colors['text_dark'],
            font=('Arial', 24, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 25))
        
        # Full Name
        tk.Label(register_card, text="Full Name:", bg=self.colors['login_card'], fg=self.colors['text_dark'], font=('Arial', 11, 'bold')).grid(row=1, column=0, sticky='w', pady=8)
        self.reg_fullname = tk.Entry(register_card, font=('Arial', 11), width=25, relief='solid', borderwidth=2)
        self.reg_fullname.grid(row=1, column=1, pady=8, padx=10)
        
        # Username
        tk.Label(register_card, text="Username:", bg=self.colors['login_card'], fg=self.colors['text_dark'], font=('Arial', 11, 'bold')).grid(row=2, column=0, sticky='w', pady=8)
        self.reg_username = tk.Entry(register_card, font=('Arial', 11), width=25, relief='solid', borderwidth=2)
        self.reg_username.grid(row=2, column=1, pady=8, padx=10)
        
        # Email
        tk.Label(register_card, text="Email:", bg=self.colors['login_card'], fg=self.colors['text_dark'], font=('Arial', 11, 'bold')).grid(row=3, column=0, sticky='w', pady=8)
        self.reg_email = tk.Entry(register_card, font=('Arial', 11), width=25, relief='solid', borderwidth=2)
        self.reg_email.grid(row=3, column=1, pady=8, padx=10)
        
        # Password
        tk.Label(register_card, text="Password:", bg=self.colors['login_card'], fg=self.colors['text_dark'], font=('Arial', 11, 'bold')).grid(row=4, column=0, sticky='w', pady=8)
        self.reg_password = tk.Entry(register_card, font=('Arial', 11), width=25, show='*', relief='solid', borderwidth=2)
        self.reg_password.grid(row=4, column=1, pady=8, padx=10)
        
        # Confirm Password
        tk.Label(register_card, text="Confirm Password:", bg=self.colors['login_card'], fg=self.colors['text_dark'], font=('Arial', 11, 'bold')).grid(row=5, column=0, sticky='w', pady=8)
        self.reg_confirm_password = tk.Entry(register_card, font=('Arial', 11), width=25, show='*', relief='solid', borderwidth=2)
        self.reg_confirm_password.grid(row=5, column=1, pady=8, padx=10)
        
        # Register Button
        register_btn = self.create_colored_button(register_card, "Register", self.handle_register, self.colors['success'])
        register_btn.grid(row=6, column=0, columnspan=2, pady=20)
        
        # Back Button
        back_btn = self.create_colored_button(register_card, "Back to Login", self.show_login_screen, self.colors['warning'], width=18)
        back_btn.grid(row=7, column=0, columnspan=2, pady=5)
    
    def handle_login(self):
        """Handle login button click"""
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        success, message, user = self.auth.login(username, password)
        
        if success:
            self.current_user = user
            messagebox.showinfo("Success", message)
            
            if user.role == 'student':
                self.show_student_dashboard()
            elif user.role == 'admin':
                self.show_admin_dashboard()
        else:
            messagebox.showerror("Error", message)
    
    def handle_register(self):
        """Handle registration button click"""
        full_name = self.reg_fullname.get().strip()
        username = self.reg_username.get().strip()
        email = self.reg_email.get().strip()
        password = self.reg_password.get().strip()
        confirm_password = self.reg_confirm_password.get().strip()
        
        if not all([full_name, username, email, password, confirm_password]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        
        success, message = self.auth.register_student(username, password, full_name, email)
        
        if success:
            messagebox.showinfo("Success", message)
            self.show_login_screen()
        else:
            messagebox.showerror("Error", message)
    
    def show_student_dashboard(self):
        """Display student dashboard with light blue theme and two tabs"""
        self.clear_window()
        self.root.configure(bg=self.colors['student_bg'])
        
        # Top header bar with welcome message and logout button
        top_frame = tk.Frame(self.root, bg=self.colors['primary'], padx=20, pady=15)
        top_frame.pack(fill='x')
        
        welcome_label = tk.Label(
            top_frame,
            text=f"Welcome, {self.current_user.full_name}",
            bg=self.colors['primary'],
            fg=self.colors['text_light'],
            font=('Arial', 18, 'bold')
        )
        welcome_label.pack(side='left')
        
        logout_btn = self.create_colored_button(top_frame, "Logout", self.logout, self.colors['danger'], width=10)
        logout_btn.pack(side='right')
        
        # Tabbed notebook for student features
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Available Courses Tab
        available_frame = tk.Frame(notebook, bg=self.colors['student_bg'], padx=20, pady=20)
        notebook.add(available_frame, text="Available Courses")
        self.setup_available_courses_tab(available_frame)
        
        # My Courses Tab
        enrolled_frame = tk.Frame(notebook, bg=self.colors['student_bg'], padx=20, pady=20)
        notebook.add(enrolled_frame, text="My Courses")
        self.setup_enrolled_courses_tab(enrolled_frame)
    
    def setup_available_courses_tab(self, parent):
        """Setup available courses tab with search, refresh, and enroll functionality"""
        # Search and refresh bar
        search_frame = tk.Frame(parent, bg=self.colors['student_bg'])
        search_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(search_frame, text="Search:", bg=self.colors['student_bg'], fg=self.colors['text_dark'], font=('Arial', 11, 'bold')).pack(side='left', padx=5)
        self.search_entry = tk.Entry(search_frame, font=('Arial', 11), width=30, relief='solid', borderwidth=2)
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<KeyRelease>', self.search_courses)
        
        refresh_btn = self.create_colored_button(search_frame, "Refresh", self.load_available_courses, self.colors['info'], width=10)
        refresh_btn.pack(side='left', padx=5)
        
        # Courses table with white background
        tree_frame = tk.Frame(parent, bg='white', relief='solid', borderwidth=2)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('Code', 'Name', 'Credits', 'Capacity', 'Enrolled', 'Available')
        self.available_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.available_tree.heading(col, text=col)
            self.available_tree.column(col, width=120, anchor='center')
        
        self.available_tree.pack(fill='both', expand=True)
        
        # Scrollbar for table
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.available_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.available_tree.configure(yscrollcommand=scrollbar.set)
        
        # Enroll button
        enroll_btn = self.create_colored_button(parent, "Enroll in Selected Course", self.enroll_course, self.colors['success'], width=25)
        enroll_btn.pack(pady=5)
        
        # Load courses
        self.load_available_courses()
    
    def load_available_courses(self):
        """Load available courses into treeview"""
        for item in self.available_tree.get_children():
            self.available_tree.delete(item)
        
        courses = self.db.execute_query(
            'SELECT id, course_code, course_name, description, credits, capacity, enrolled_count FROM courses'
        )
        
        for course in courses:
            course_id, code, name, desc, credits, capacity, enrolled = course
            available = capacity - enrolled
            self.available_tree.insert('', 'end', values=(code, name, credits, capacity, enrolled, available), tags=(str(course_id),))
    
    def search_courses(self, event=None):
        """Search courses"""
        search_term = self.search_entry.get().lower()
        
        for item in self.available_tree.get_children():
            self.available_tree.delete(item)
        
        if search_term:
            courses = self.db.execute_query(
                '''SELECT id, course_code, course_name, description, credits, capacity, enrolled_count 
                   FROM courses 
                   WHERE LOWER(course_code) LIKE ? OR LOWER(course_name) LIKE ? OR LOWER(description) LIKE ?''',
                (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%')
            )
        else:
            courses = self.db.execute_query(
                'SELECT id, course_code, course_name, description, credits, capacity, enrolled_count FROM courses'
            )
        
        for course in courses:
            course_id, code, name, desc, credits, capacity, enrolled = course
            available = capacity - enrolled
            self.available_tree.insert('', 'end', values=(code, name, credits, capacity, enrolled, available), tags=(str(course_id),))
    
    def enroll_course(self):
        """Enroll in selected course"""
        selection = self.available_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a course to enroll")
            return
        
        item = self.available_tree.item(selection[0])
        course_id = int(item['tags'][0])
        course_name = item['values'][1]
        
        confirm = messagebox.askyesno("Confirm", f"Enroll in {course_name}?")
        if confirm:
            success, message = self.current_user.enroll_in_course(course_id)
            if success:
                messagebox.showinfo("Success", message)
                self.load_available_courses()
                self.load_enrolled_courses()
            else:
                messagebox.showerror("Error", message)
    
    def setup_enrolled_courses_tab(self, parent):
        """Setup enrolled courses tab with refresh and drop functionality"""
        # Enrolled courses table with white background
        tree_frame = tk.Frame(parent, bg='white', relief='solid', borderwidth=2)
        tree_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        columns = ('Code', 'Name', 'Credits', 'Enrollment Date')
        self.enrolled_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.enrolled_tree.heading(col, text=col)
            self.enrolled_tree.column(col, width=150, anchor='center')
        
        self.enrolled_tree.pack(fill='both', expand=True)
        
        # Scrollbar for table
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.enrolled_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.enrolled_tree.configure(yscrollcommand=scrollbar.set)
        
        # Action buttons frame
        btn_frame = tk.Frame(parent, bg=self.colors['student_bg'])
        btn_frame.pack(pady=10)
        
        refresh_btn = self.create_colored_button(btn_frame, "Refresh", self.load_enrolled_courses, self.colors['info'], width=12)
        refresh_btn.pack(side='left', padx=5)
        
        drop_btn = self.create_colored_button(btn_frame, "Drop Selected Course", self.drop_course, self.colors['danger'], width=18)
        drop_btn.pack(side='left', padx=5)
        
        # Load enrolled courses
        self.load_enrolled_courses()
    
    def load_enrolled_courses(self):
        """Load enrolled courses"""
        for item in self.enrolled_tree.get_children():
            self.enrolled_tree.delete(item)
        
        courses = self.current_user.get_enrolled_courses()
        
        for course in courses:
            course_id, code, name, desc, credits, capacity, enrolled = course
            enrollment_data = self.db.execute_query(
                '''SELECT enrollment_date FROM enrollments 
                   WHERE student_id = ? AND course_id = ?''',
                (self.current_user.id, course_id)
            )
            enrollment_date = enrollment_data[0][0] if enrollment_data else 'N/A'
            self.enrolled_tree.insert('', 'end', values=(code, name, credits, enrollment_date), tags=(str(course_id),))
    
    def drop_course(self):
        """Drop selected course"""
        selection = self.enrolled_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a course to drop")
            return
        
        item = self.enrolled_tree.item(selection[0])
        course_id = int(item['tags'][0])
        course_name = item['values'][1]
        
        confirm = messagebox.askyesno("Confirm", f"Drop {course_name}?")
        if confirm:
            success, message = self.current_user.drop_course(course_id)
            if success:
                messagebox.showinfo("Success", message)
                self.load_enrolled_courses()
                self.load_available_courses()
            else:
                messagebox.showerror("Error", message)
    
    def show_admin_dashboard(self):
        """Display admin dashboard with light orange theme and three tabs"""
        self.clear_window()
        self.root.configure(bg=self.colors['admin_bg'])
        
        # Top header bar with admin info and logout button
        top_frame = tk.Frame(self.root, bg=self.colors['warning'], padx=20, pady=15)
        top_frame.pack(fill='x')
        
        welcome_label = tk.Label(
            top_frame,
            text=f"Admin Dashboard - {self.current_user.full_name}",
            bg=self.colors['warning'],
            fg=self.colors['text_light'],
            font=('Arial', 18, 'bold')
        )
        welcome_label.pack(side='left')
        
        logout_btn = self.create_colored_button(top_frame, "Logout", self.logout, self.colors['danger'], width=10)
        logout_btn.pack(side='right')
        
        # Tabbed notebook for admin features
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Manage Courses Tab
        courses_frame = tk.Frame(notebook, bg=self.colors['admin_bg'], padx=20, pady=20)
        notebook.add(courses_frame, text="Manage Courses")
        self.setup_admin_courses_tab(courses_frame)
        
        # View Students Tab
        students_frame = tk.Frame(notebook, bg=self.colors['admin_bg'], padx=20, pady=20)
        notebook.add(students_frame, text="View Students")
        self.setup_admin_students_tab(students_frame)
        
        # Reports Tab
        reports_frame = tk.Frame(notebook, bg=self.colors['admin_bg'], padx=20, pady=20)
        notebook.add(reports_frame, text="Reports")
        self.setup_admin_reports_tab(reports_frame)
    
    def setup_admin_courses_tab(self, parent):
        """Setup admin courses management tab with add/remove functionality"""
        # Add course form
        add_frame = tk.LabelFrame(parent, text="Add New Course", bg='white', fg=self.colors['text_dark'], font=('Arial', 12, 'bold'), padx=15, pady=15)
        add_frame.pack(fill='x', pady=(0, 15))
        
        # Course Code
        tk.Label(add_frame, text="Course Code:", bg='white', fg=self.colors['text_dark'], font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        self.admin_course_code = tk.Entry(add_frame, font=('Arial', 10), width=20, relief='solid', borderwidth=2)
        self.admin_course_code.grid(row=0, column=1, pady=5, padx=5)
        
        # Course Name
        tk.Label(add_frame, text="Course Name:", bg='white', fg=self.colors['text_dark'], font=('Arial', 10, 'bold')).grid(row=0, column=2, sticky='w', pady=5)
        self.admin_course_name = tk.Entry(add_frame, font=('Arial', 10), width=30, relief='solid', borderwidth=2)
        self.admin_course_name.grid(row=0, column=3, pady=5, padx=5)
        
        # Credits
        tk.Label(add_frame, text="Credits:", bg='white', fg=self.colors['text_dark'], font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w', pady=5)
        self.admin_credits = tk.Entry(add_frame, font=('Arial', 10), width=20, relief='solid', borderwidth=2)
        self.admin_credits.grid(row=1, column=1, pady=5, padx=5)
        
        # Capacity
        tk.Label(add_frame, text="Capacity:", bg='white', fg=self.colors['text_dark'], font=('Arial', 10, 'bold')).grid(row=1, column=2, sticky='w', pady=5)
        self.admin_capacity = tk.Entry(add_frame, font=('Arial', 10), width=20, relief='solid', borderwidth=2)
        self.admin_capacity.grid(row=1, column=3, pady=5, padx=5)
        
        # Description
        tk.Label(add_frame, text="Description:", bg='white', fg=self.colors['text_dark'], font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='w', pady=5)
        self.admin_description = tk.Entry(add_frame, font=('Arial', 10), width=50, relief='solid', borderwidth=2)
        self.admin_description.grid(row=2, column=1, columnspan=3, pady=5, padx=5, sticky='ew')
        
        # Add button
        add_btn = self.create_colored_button(add_frame, "Add Course", self.admin_add_course, self.colors['success'], width=15)
        add_btn.grid(row=3, column=0, columnspan=4, pady=10)
        
        # Courses table with white background
        tree_frame = tk.Frame(parent, bg='white', relief='solid', borderwidth=2)
        tree_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        columns = ('ID', 'Code', 'Name', 'Credits', 'Capacity', 'Enrolled')
        self.admin_courses_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            self.admin_courses_tree.heading(col, text=col)
            self.admin_courses_tree.column(col, width=100, anchor='center')
        
        self.admin_courses_tree.pack(fill='both', expand=True)
        
        # Scrollbar for table
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.admin_courses_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.admin_courses_tree.configure(yscrollcommand=scrollbar.set)
        
        # Action buttons frame
        btn_frame = tk.Frame(parent, bg=self.colors['admin_bg'])
        btn_frame.pack(pady=10)
        
        refresh_btn = self.create_colored_button(btn_frame, "Refresh", self.load_admin_courses, self.colors['info'], width=12)
        refresh_btn.pack(side='left', padx=5)
        
        remove_btn = self.create_colored_button(btn_frame, "Remove Selected Course", self.admin_remove_course, self.colors['danger'], width=20)
        remove_btn.pack(side='left', padx=5)
        
        # Load courses
        self.load_admin_courses()
    
    def load_admin_courses(self):
        """Load all courses for admin"""
        for item in self.admin_courses_tree.get_children():
            self.admin_courses_tree.delete(item)
        
        courses = self.current_user.get_all_courses()
        
        for course in courses:
            course_id, code, name, desc, credits, capacity, enrolled = course
            self.admin_courses_tree.insert('', 'end', values=(course_id, code, name, credits, capacity, enrolled))
    
    def admin_add_course(self):
        """Add new course"""
        code = self.admin_course_code.get().strip()
        name = self.admin_course_name.get().strip()
        credits = self.admin_credits.get().strip()
        capacity = self.admin_capacity.get().strip()
        description = self.admin_description.get().strip()
        
        if not all([code, name, credits, capacity]):
            messagebox.showerror("Error", "Course code, name, credits, and capacity are required")
            return
        
        try:
            credits = int(credits)
            capacity = int(capacity)
        except ValueError:
            messagebox.showerror("Error", "Credits and capacity must be numbers")
            return
        
        success, message = self.current_user.add_course(code, name, description, credits, capacity)
        
        if success:
            messagebox.showinfo("Success", message)
            self.admin_course_code.delete(0, tk.END)
            self.admin_course_name.delete(0, tk.END)
            self.admin_credits.delete(0, tk.END)
            self.admin_capacity.delete(0, tk.END)
            self.admin_description.delete(0, tk.END)
            self.load_admin_courses()
        else:
            messagebox.showerror("Error", message)
    
    def admin_remove_course(self):
        """Remove selected course"""
        selection = self.admin_courses_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a course to remove")
            return
        
        item = self.admin_courses_tree.item(selection[0])
        course_id = item['values'][0]
        course_name = item['values'][2]
        
        confirm = messagebox.askyesno("Confirm", f"Remove {course_name}? This will also remove all enrollments.")
        if confirm:
            success, message = self.current_user.remove_course(course_id)
            if success:
                messagebox.showinfo("Success", message)
                self.load_admin_courses()
            else:
                messagebox.showerror("Error", message)
    
    def setup_admin_students_tab(self, parent):
        """Setup admin students view tab with refresh functionality"""
        # Students table with white background
        tree_frame = tk.Frame(parent, bg='white', relief='solid', borderwidth=2)
        tree_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        columns = ('ID', 'Username', 'Full Name', 'Email', 'Registered')
        self.students_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.students_tree.heading(col, text=col)
            self.students_tree.column(col, width=150, anchor='center')
        
        self.students_tree.pack(fill='both', expand=True)
        
        # Scrollbar for table
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.students_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.students_tree.configure(yscrollcommand=scrollbar.set)
        
        # Refresh button
        refresh_btn = self.create_colored_button(parent, "Refresh", self.load_students, self.colors['info'], width=15)
        refresh_btn.pack(pady=10)
        
        # Load students
        self.load_students()
    
    def load_students(self):
        """Load all students"""
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        students = self.current_user.get_all_students()
        
        for student in students:
            student_id, username, full_name, email, created_at = student
            self.students_tree.insert('', 'end', values=(student_id, username, full_name, email, created_at))
    
    def setup_admin_reports_tab(self, parent):
        """Setup admin reports tab with generate and CSV export functionality"""
        # Report selection and action bar
        report_frame = tk.Frame(parent, bg=self.colors['admin_bg'])
        report_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(report_frame, text="Select Report:", bg=self.colors['admin_bg'], fg=self.colors['text_dark'], font=('Arial', 11, 'bold')).pack(side='left', padx=5)
        
        self.report_type = ttk.Combobox(report_frame, values=['Enrollment Report', 'Course Statistics'], 
                                        font=('Arial', 11), width=25, state='readonly')
        self.report_type.pack(side='left', padx=5)
        self.report_type.set('Enrollment Report')
        
        generate_btn = self.create_colored_button(report_frame, "Generate Report", self.generate_report, self.colors['primary'], width=15)
        generate_btn.pack(side='left', padx=5)
        
        export_btn = self.create_colored_button(report_frame, "Export to CSV", self.export_report, self.colors['success'], width=12)
        export_btn.pack(side='left', padx=5)
        
        # Report display area with white background
        report_frame_white = tk.Frame(parent, bg='white', relief='solid', borderwidth=2)
        report_frame_white.pack(fill='both', expand=True)
        
        self.report_text = scrolledtext.ScrolledText(report_frame_white, font=('Courier New', 10), height=20, bg='white')
        self.report_text.pack(fill='both', expand=True)
    
    def generate_report(self):
        """Generate selected report"""
        report_type = self.report_type.get()
        
        if report_type == 'Enrollment Report':
            self.generate_enrollment_report()
        elif report_type == 'Course Statistics':
            self.generate_statistics_report()
    
    def generate_enrollment_report(self):
        """Generate enrollment report showing all student-course enrollments"""
        self.report_text.delete(1.0, tk.END)
        
        report_data = self.current_user.get_enrollment_report()
        
        if not report_data:
            self.report_text.insert(tk.END, "No enrollment data available.")
            return
        
        # Report header
        header = f"{'='*100}\n"
        header += f"ENROLLMENT REPORT\n"
        header += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        header += f"{'='*100}\n\n"
        self.report_text.insert(tk.END, header)
        
        # Column headers
        col_header = f"{'Student Name':<25} {'Username':<15} {'Email':<30} {'Course Code':<12} {'Course Name':<30} {'Credits':<8}\n"
        col_header += "-" * 120 + "\n"
        self.report_text.insert(tk.END, col_header)
        
        # Data rows
        for row in report_data:
            student_id, username, full_name, email, course_code, course_name, credits, enrollment_date = row
            line = f"{full_name:<25} {username:<15} {email:<30} {course_code:<12} {course_name:<30} {credits:<8}\n"
            self.report_text.insert(tk.END, line)
        
        # Report footer
        footer = f"\n{'='*100}\n"
        footer += f"Total Enrollments: {len(report_data)}\n"
        footer += f"{'='*100}\n"
        self.report_text.insert(tk.END, footer)
    
    def generate_statistics_report(self):
        """Generate course statistics report showing capacity and fill percentages"""
        self.report_text.delete(1.0, tk.END)
        
        stats_data = self.current_user.get_course_statistics()
        
        if not stats_data:
            self.report_text.insert(tk.END, "No course data available.")
            return
        
        # Report header
        header = f"{'='*100}\n"
        header += f"COURSE STATISTICS REPORT\n"
        header += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        header += f"{'='*100}\n\n"
        self.report_text.insert(tk.END, header)
        
        # Column headers
        col_header = f"{'Course Code':<15} {'Course Name':<35} {'Capacity':<10} {'Enrolled':<10} {'Fill %':<10}\n"
        col_header += "-" * 90 + "\n"
        self.report_text.insert(tk.END, col_header)
        
        # Data rows
        for row in stats_data:
            course_code, course_name, capacity, enrolled, fill_percent = row
            line = f"{course_code:<15} {course_name:<35} {capacity:<10} {enrolled:<10} {fill_percent:<10}%\n"
            self.report_text.insert(tk.END, line)
        
        # Report footer
        footer = f"\n{'='*100}\n"
        footer += f"Total Courses: {len(stats_data)}\n"
        footer += f"{'='*100}\n"
        self.report_text.insert(tk.END, footer)
    
    def export_report(self):
        """Export current report to CSV file with timestamp"""
        report_type = self.report_type.get()
        
        if report_type == 'Enrollment Report':
            data = self.current_user.get_enrollment_report()
            filename = f"enrollment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            headers = ['Student ID', 'Username', 'Full Name', 'Email', 'Course Code', 'Course Name', 'Credits', 'Enrollment Date']
        else:
            data = self.current_user.get_course_statistics()
            filename = f"course_statistics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            headers = ['Course Code', 'Course Name', 'Capacity', 'Enrolled', 'Fill Percentage']
        
        if not data:
            messagebox.showwarning("Warning", "No data to export")
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                writer.writerows(data)
            
            messagebox.showinfo("Success", f"Report exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {str(e)}")
    
    def logout(self):
        """Logout current user and return to login screen"""
        self.auth.logout()
        self.current_user = None
        self.show_login_screen()


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = CourseRegistrationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

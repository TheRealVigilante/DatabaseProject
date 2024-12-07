import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import os
from datetime import datetime

class LoginApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Database Management System")
        self.root.geometry("400x300")
        
        # Database path
        self.db_path = os.path.join(os.path.dirname(__file__), "university.db")
        
        # Configure grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.create_main_frame()
        
    def create_main_frame(self):
        # Main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Login label
        login_label = ctk.CTkLabel(
            self.main_frame, 
            text="Login as:", 
            font=("Helvetica", 24)
        )
        login_label.pack(pady=20)
        
        # Buttons
        admin_btn = ctk.CTkButton(
            self.main_frame,
            text="Admin",
            command=lambda: self.show_login_window("Admin"),
            width=200
        )
        admin_btn.pack(pady=10)
        
        instructor_btn = ctk.CTkButton(
            self.main_frame,
            text="Instructor",
            command=lambda: self.show_login_window("Instructor"),
            width=200
        )
        instructor_btn.pack(pady=10)
        
        student_btn = ctk.CTkButton(
            self.main_frame,
            text="Student",
            command=lambda: self.show_login_window("Student"),
            width=200
        )
        student_btn.pack(pady=10)
        
    def verify_credentials(self, user_type, username, password):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if user_type == "Admin":
                # For simplicity, we'll use a hardcoded admin credentials
                # In a real application, this should be stored securely
                return username == "admin" and password == "admin123"
            
            elif user_type == "Instructor":
                cursor.execute("""
                    SELECT InstructorID, First_Name, Last_Name 
                    FROM Instructors 
                    WHERE Username = ? AND Password = ?
                """, (username, password))
                result = cursor.fetchone()
                
                if result:
                    self.user_id = result[0]
                    self.user_name = f"{result[1]} {result[2]}"
                    return True
                    
            elif user_type == "Student":
                cursor.execute("""
                    SELECT StudentID, First_Name, Last_Name 
                    FROM Students 
                    WHERE Username = ? AND Password = ?
                """, (username, password))
                result = cursor.fetchone()
                
                if result:
                    self.user_id = result[0]
                    self.user_name = f"{result[1]} {result[2]}"
                    return True
                    
            return False
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
            return False
            
        finally:
            if 'conn' in locals():
                conn.close()
                
    def show_login_window(self, user_type):
        # Create new window
        login_window = ctk.CTkToplevel(self.root)
        login_window.title(f"{user_type} Login")
        login_window.geometry("300x250")
        
        # Center the window
        login_window.transient(self.root)
        
        # Username
        username_label = ctk.CTkLabel(login_window, text="Username:")
        username_label.pack(pady=10)
        username_entry = ctk.CTkEntry(login_window)
        username_entry.pack()
        
        # Password
        password_label = ctk.CTkLabel(login_window, text="Password:")
        password_label.pack(pady=10)
        password_entry = ctk.CTkEntry(login_window, show="*")
        password_entry.pack()
        
        # Login button
        def verify_login():
            username = username_entry.get()
            password = password_entry.get()
            
            if not username or not password:
                messagebox.showerror("Error", "Please enter both username and password!")
                return
                
            if self.verify_credentials(user_type, username, password):
                messagebox.showinfo("Success", f"Welcome {self.user_name}!")
                login_window.destroy()
                self.show_main_menu(user_type)
            else:
                messagebox.showerror("Error", "Invalid credentials!")
                
        login_btn = ctk.CTkButton(
            login_window,
            text="Login",
            command=verify_login
        )
        login_btn.pack(pady=20)
        
        # Wait for window to be visible before setting grab
        def set_grab():
            if login_window.winfo_exists():
                login_window.grab_set()
                login_window.focus_set()
        
        # Schedule grab_set after window is drawn
        login_window.after(100, set_grab)
        
    def show_main_menu(self, user_type):
        # Create new window for the main menu
        self.menu_window = ctk.CTkToplevel(self.root)
        self.menu_window.title(f"{user_type} Dashboard")
        self.menu_window.geometry("800x600")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.menu_window)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Welcome message at the top
        welcome_frame = ctk.CTkFrame(self.menu_window)
        welcome_frame.pack(fill='x', padx=10, pady=5)
        welcome_label = ctk.CTkLabel(
            welcome_frame,
            text=f"Welcome {self.user_name}!",
            font=("Helvetica", 24)
        )
        welcome_label.pack(pady=10)
        
        if user_type == "Admin":
            self.create_admin_dashboard()
        elif user_type == "Instructor":
            self.create_instructor_dashboard()
        else:  # Student
            self.create_student_dashboard()
            
    def create_admin_dashboard(self):
        # User Management Tab
        user_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(user_frame, text="User Management")
        
        # Add user section
        add_user_label = ctk.CTkLabel(user_frame, text="Add New User", font=("Helvetica", 16))
        add_user_label.pack(pady=10)
        
        user_type_var = tk.StringVar(value="Student")
        user_type_frame = ctk.CTkFrame(user_frame)
        user_type_frame.pack(pady=5)
        ctk.CTkRadioButton(user_type_frame, text="Student", variable=user_type_var, value="Student").pack(side='left', padx=10)
        ctk.CTkRadioButton(user_type_frame, text="Instructor", variable=user_type_var, value="Instructor").pack(side='left', padx=10)
        
        fields = ['Username', 'Password', 'First Name', 'Last Name', 'Email']
        entries = {}
        for field in fields:
            frame = ctk.CTkFrame(user_frame)
            frame.pack(pady=5)
            ctk.CTkLabel(frame, text=f"{field}:").pack(side='left', padx=5)
            entries[field] = ctk.CTkEntry(frame)
            entries[field].pack(side='left', padx=5)
            
        ctk.CTkButton(user_frame, text="Add User", 
                     command=lambda: self.add_user(user_type_var.get(), entries)).pack(pady=10)
        
        # Course Management Tab
        course_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(course_frame, text="Course Management")
        
        # Analytics Tab
        analytics_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(analytics_frame, text="Analytics")
        
        self.create_analytics_view(analytics_frame)
        
    def create_instructor_dashboard(self):
        # Profile Tab
        profile_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(profile_frame, text="Profile")
        self.create_profile_view(profile_frame)
        
        # Courses Tab
        courses_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(courses_frame, text="My Courses")
        
        # Create Course Button
        create_course_btn = ctk.CTkButton(courses_frame, text="Create New Course",
                                        command=self.show_create_course_dialog)
        create_course_btn.pack(pady=10)
        
        # Assessments Tab
        assessments_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(assessments_frame, text="Assessments")
        
        # Reports Tab
        reports_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(reports_frame, text="Reports")
        
    def create_student_dashboard(self):
        # Profile Tab
        profile_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(profile_frame, text="Profile")
        self.create_profile_view(profile_frame)
        
        # Courses Tab
        courses_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(courses_frame, text="My Courses")
        
        # Available Courses Button
        browse_courses_btn = ctk.CTkButton(courses_frame, text="Browse Available Courses",
                                         command=self.show_available_courses)
        browse_courses_btn.pack(pady=10)
        
        # Create a scrollable frame for enrolled courses
        enrolled_courses_label = ctk.CTkLabel(courses_frame, text="Enrolled Courses:")
        enrolled_courses_label.pack(pady=5)
        
        # Grades Tab
        grades_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(grades_frame, text="Grades")
        
        # Assessments Tab
        assessments_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(assessments_frame, text="Assessments")
        
    def create_profile_view(self, parent_frame):
        fields = ['Phone Number', 'Address', 'Email']
        entries = {}
        
        for field in fields:
            frame = ctk.CTkFrame(parent_frame)
            frame.pack(pady=5)
            ctk.CTkLabel(frame, text=f"{field}:").pack(side='left', padx=5)
            entries[field] = ctk.CTkEntry(frame)
            entries[field].pack(side='left', padx=5)
            
        # Load current profile data
        self.load_profile_data(entries)
        
        # Save button
        save_btn = ctk.CTkButton(parent_frame, text="Save Changes",
                                command=lambda: self.save_profile_changes(entries))
        save_btn.pack(pady=10)
        
    def create_analytics_view(self, parent_frame):
        # Active Users Section
        users_frame = ctk.CTkFrame(parent_frame)
        users_frame.pack(pady=10, padx=10, fill='x')
        
        ctk.CTkLabel(users_frame, text="Active Users", font=("Helvetica", 16)).pack()
        
        # Course Statistics Section
        courses_frame = ctk.CTkFrame(parent_frame)
        courses_frame.pack(pady=10, padx=10, fill='x')
        
        ctk.CTkLabel(courses_frame, text="Course Statistics", font=("Helvetica", 16)).pack()
        
        # Performance Metrics Section
        performance_frame = ctk.CTkFrame(parent_frame)
        performance_frame.pack(pady=10, padx=10, fill='x')
        
        ctk.CTkLabel(performance_frame, text="Performance Metrics", font=("Helvetica", 16)).pack()
        
    def show_create_course_dialog(self):
        dialog = ctk.CTkToplevel(self.menu_window)
        dialog.title("Create New Course")
        dialog.geometry("500x400")
        
        fields = ['Title', 'Description', 'Duration (weeks)', 'Max Enrollment']
        entries = {}
        
        for field in fields:
            frame = ctk.CTkFrame(dialog)
            frame.pack(pady=5)
            ctk.CTkLabel(frame, text=f"{field}:").pack(side='left', padx=5)
            entries[field] = ctk.CTkEntry(frame)
            entries[field].pack(side='left', padx=5)
            
        # Prerequisites section
        prereq_frame = ctk.CTkFrame(dialog)
        prereq_frame.pack(pady=10)
        ctk.CTkLabel(prereq_frame, text="Prerequisites:").pack()
        
        # Add course button
        ctk.CTkButton(dialog, text="Create Course",
                     command=lambda: self.create_course(entries, dialog)).pack(pady=10)
        
    def show_available_courses(self):
        dialog = ctk.CTkToplevel(self.menu_window)
        dialog.title("Available Courses")
        dialog.geometry("600x400")
        
        # Create a scrollable frame for courses
        courses_frame = ctk.CTkScrollableFrame(dialog)
        courses_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Load and display available courses
        self.load_available_courses(courses_frame)
        
    def load_profile_data(self, entries):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            table = "Students" if hasattr(self, 'student_id') else "Instructors"
            id_field = "StudentID" if hasattr(self, 'student_id') else "InstructorID"
            id_value = self.user_id
            
            cursor.execute(f"SELECT PhoneNumber, Address, Email FROM {table} WHERE {id_field} = ?", 
                         (id_value,))
            result = cursor.fetchone()
            
            if result:
                entries['Phone Number'].insert(0, result[0] or '')
                entries['Address'].insert(0, result[1] or '')
                entries['Email'].insert(0, result[2] or '')
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading profile: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()
                
    def save_profile_changes(self, entries):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            table = "Students" if hasattr(self, 'student_id') else "Instructors"
            id_field = "StudentID" if hasattr(self, 'student_id') else "InstructorID"
            
            cursor.execute(f"""
                UPDATE {table}
                SET PhoneNumber = ?, Address = ?, Email = ?
                WHERE {id_field} = ?
            """, (entries['Phone Number'].get(), entries['Address'].get(), 
                 entries['Email'].get(), self.user_id))
            
            conn.commit()
            messagebox.showinfo("Success", "Profile updated successfully!")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error saving profile: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()
                
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LoginApp()
    app.run()

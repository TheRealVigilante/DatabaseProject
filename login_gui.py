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
                    SELECT InstructorID, First_Name, Last_Name, Email, 
                           PhoneNumber, HireDate, Specialization
                    FROM Instructors 
                    WHERE Username = ? AND Password = ?
                """, (username, password))
                result = cursor.fetchone()
                
                if result:
                    self.user_id = result[0]
                    self.user_name = f"{result[1]} {result[2]}"
                    self.user_details = {
                        'First Name': result[1],
                        'Last Name': result[2],
                        'Email': result[3],
                        'Phone Number': result[4],
                        'Hire Date': result[5],
                        'Specialization': result[6]
                    }
                    return True
                    
            elif user_type == "Student":
                cursor.execute("""
                    SELECT StudentID, First_Name, Last_Name, Email, 
                           PhoneNumber, EnrollmentDate, DateOfBirth, 
                           Address
                    FROM Students 
                    WHERE Username = ? AND Password = ?
                """, (username, password))
                result = cursor.fetchone()
                
                if result:
                    self.user_id = result[0]
                    self.user_name = f"{result[1]} {result[2]}"
                    self.user_details = {
                        'First Name': result[1],
                        'Last Name': result[2],
                        'Email': result[3],
                        'Phone Number': result[4],
                        'Enrollment Date': result[5],
                        'Date of Birth': result[6],
                        'Address': result[7]
                    }
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
        
        enrolled_frame = ctk.CTkScrollableFrame(courses_frame)
        enrolled_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Load enrolled courses
        self.load_enrolled_courses(enrolled_frame)
        
        # Grades Tab
        grades_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(grades_frame, text="Grades")
        
        # Create scrollable frame for grades
        grades_scroll = ctk.CTkScrollableFrame(grades_frame)
        grades_scroll.pack(expand=True, fill='both', padx=10, pady=10)
        self.load_assessment_grades(grades_scroll)
        
        # Assessments Tab
        assessments_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(assessments_frame, text="Assessments")
        
        # Create scrollable frame for assessments
        assessments_scroll = ctk.CTkScrollableFrame(assessments_frame)
        assessments_scroll.pack(expand=True, fill='both', padx=10, pady=10)
        self.load_student_assessments(assessments_scroll)
        
    def create_profile_view(self, parent_frame):
        # Create a main profile frame
        main_profile_frame = ctk.CTkFrame(parent_frame)
        main_profile_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Personal Information Section
        personal_info_frame = ctk.CTkFrame(main_profile_frame)
        personal_info_frame.pack(fill='x', pady=(0, 20))
        
        ctk.CTkLabel(
            personal_info_frame,
            text="Personal Information",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)
        
        # Create two columns for better layout
        left_frame = ctk.CTkFrame(personal_info_frame)
        left_frame.pack(side='left', expand=True, fill='both', padx=10)
        
        right_frame = ctk.CTkFrame(personal_info_frame)
        right_frame.pack(side='right', expand=True, fill='both', padx=10)
        
        # Display all user details
        entries = {}
        column_frames = [left_frame, right_frame]
        current_frame = 0
        
        for field, value in self.user_details.items():
            frame = ctk.CTkFrame(column_frames[current_frame])
            frame.pack(pady=5, fill='x')
            
            ctk.CTkLabel(frame, text=f"{field}:", anchor='w').pack(side='left', padx=5)
            
            if field in ['Phone Number', 'Email', 'Address']:
                # These fields are editable
                entry = ctk.CTkEntry(frame)
                entry.insert(0, value if value else '')
                entry.pack(side='left', padx=5, fill='x', expand=True)
                entries[field] = entry
            else:
                # Read-only fields
                ctk.CTkLabel(frame, text=str(value) if value else 'N/A').pack(side='left', padx=5)
            
            # Switch between columns
            current_frame = (current_frame + 1) % 2
        
        # Statistics Section (if student)
        if hasattr(self, 'student_id'):
            self.create_student_statistics(main_profile_frame)
        
        # Course Statistics Section (if instructor)
        if hasattr(self, 'instructor_id'):
            self.create_instructor_statistics(main_profile_frame)
        
        # Save button for editable fields
        if entries:
            save_btn = ctk.CTkButton(
                main_profile_frame,
                text="Save Changes",
                command=lambda: self.save_profile_changes(entries)
            )
            save_btn.pack(pady=20)
            
    def create_student_statistics(self, parent_frame):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            stats_frame = ctk.CTkFrame(parent_frame)
            stats_frame.pack(fill='x', pady=20)
            
            ctk.CTkLabel(
                stats_frame,
                text="Academic Statistics",
                font=("Helvetica", 16, "bold")
            ).pack(pady=10)
            
            # Get total courses enrolled
            cursor.execute("""
                SELECT COUNT(*), AVG(p.FinalGrade)
                FROM Enrollment e
                LEFT JOIN Performance p ON e.EnrollmentID = p.EnrollmentID
                WHERE e.StudentID = ?
            """, (self.user_id,))
            
            total_courses, avg_grade = cursor.fetchone()
            
            stats_text = f"Total Courses Enrolled: {total_courses}\n"
            if avg_grade:
                stats_text += f"Average Grade: {avg_grade:.2f}%\n"
            
            # Get completed courses
            cursor.execute("""
                SELECT COUNT(*)
                FROM Enrollment e
                JOIN Performance p ON e.EnrollmentID = p.EnrollmentID
                WHERE e.StudentID = ? AND p.FinalGrade >= 60
            """, (self.user_id,))
            
            completed_courses = cursor.fetchone()[0]
            stats_text += f"Completed Courses: {completed_courses}"
            
            ctk.CTkLabel(stats_frame, text=stats_text).pack(pady=5)
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading statistics: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()
                
    def create_instructor_statistics(self, parent_frame):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            stats_frame = ctk.CTkFrame(parent_frame)
            stats_frame.pack(fill='x', pady=20)
            
            ctk.CTkLabel(
                stats_frame,
                text="Teaching Statistics",
                font=("Helvetica", 16, "bold")
            ).pack(pady=10)
            
            # Get total courses teaching
            cursor.execute("""
                SELECT COUNT(*) as TotalCourses,
                       COUNT(DISTINCT e.StudentID) as TotalStudents,
                       AVG(p.FinalGrade) as AvgGrade
                FROM Courses c
                LEFT JOIN Enrollment e ON c.CourseID = e.CourseID
                LEFT JOIN Performance p ON e.EnrollmentID = p.EnrollmentID
                WHERE c.InstructorID = ?
            """, (self.user_id,))
            
            total_courses, total_students, avg_grade = cursor.fetchone()
            
            stats_text = f"Total Courses Teaching: {total_courses}\n"
            stats_text += f"Total Students: {total_students or 0}\n"
            if avg_grade:
                stats_text += f"Average Student Grade: {avg_grade:.2f}%"
            
            ctk.CTkLabel(stats_frame, text=stats_text).pack(pady=5)
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading statistics: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()
                
    def create_analytics_view(self, parent_frame):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Active Users Section
            users_frame = ctk.CTkFrame(parent_frame)
            users_frame.pack(pady=10, padx=10, fill='x')
            
            ctk.CTkLabel(users_frame, text="Active Users", font=("Helvetica", 16, "bold")).pack()
            
            # Count active students and instructors
            cursor.execute("SELECT COUNT(*) FROM Students")
            student_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM Instructors")
            instructor_count = cursor.fetchone()[0]
            
            ctk.CTkLabel(users_frame, text=f"Total Students: {student_count}").pack()
            ctk.CTkLabel(users_frame, text=f"Total Instructors: {instructor_count}").pack()
            
            # Course Statistics Section
            courses_frame = ctk.CTkFrame(parent_frame)
            courses_frame.pack(pady=10, padx=10, fill='x')
            
            ctk.CTkLabel(courses_frame, text="Course Statistics", font=("Helvetica", 16, "bold")).pack()
            
            # Get popular courses
            cursor.execute("""
                SELECT c.CourseName, COUNT(e.StudentID) as Enrollment
                FROM Courses c
                LEFT JOIN Enrollment e ON c.CourseID = e.CourseID
                GROUP BY c.CourseID
                ORDER BY Enrollment DESC
                LIMIT 5
            """)
            
            popular_courses = cursor.fetchall()
            
            ctk.CTkLabel(courses_frame, text="Most Popular Courses:").pack()
            for course in popular_courses:
                ctk.CTkLabel(courses_frame, text=f"{course[0]}: {course[1]} students").pack()
            
            # Performance Metrics Section
            performance_frame = ctk.CTkFrame(parent_frame)
            performance_frame.pack(pady=10, padx=10, fill='x')
            
            ctk.CTkLabel(performance_frame, text="Performance Metrics", 
                        font=("Helvetica", 16, "bold")).pack()
            
            # Calculate average grades
            cursor.execute("""
                SELECT AVG(p.FinalGrade) as AvgGrade
                FROM Performance p
            """)
            
            avg_grade = cursor.fetchone()[0]
            if avg_grade:
                ctk.CTkLabel(performance_frame, 
                            text=f"Average Grade: {avg_grade:.2f}%").pack()
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading analytics: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

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
                
    def add_user(self, user_type, entries):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Validate inputs
            for field, entry in entries.items():
                if not entry.get():
                    messagebox.showerror("Error", f"{field} cannot be empty!")
                    return
            
            table = "Students" if user_type == "Student" else "Instructors"
            
            cursor.execute(f"""
                INSERT INTO {table} (Username, Password, First_Name, Last_Name, Email)
                VALUES (?, ?, ?, ?, ?)
            """, (entries['Username'].get(), entries['Password'].get(),
                 entries['First Name'].get(), entries['Last Name'].get(),
                 entries['Email'].get()))
            
            conn.commit()
            messagebox.showinfo("Success", f"{user_type} added successfully!")
            
            # Clear entries
            for entry in entries.values():
                entry.delete(0, 'end')
                
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error adding user: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def create_course(self, entries, dialog):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Validate inputs
            for field, entry in entries.items():
                if not entry.get():
                    messagebox.showerror("Error", f"{field} cannot be empty!")
                    return
            
            cursor.execute("""
                INSERT INTO Courses (CourseName, Description, Duration, MaxEnrollment, InstructorID)
                VALUES (?, ?, ?, ?, ?)
            """, (entries['Title'].get(), entries['Description'].get(),
                 int(entries['Duration (weeks)'].get()),
                 int(entries['Max Enrollment'].get()),
                 self.user_id))
            
            conn.commit()
            messagebox.showinfo("Success", "Course created successfully!")
            dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Duration and Max Enrollment must be numbers!")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error creating course: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def load_available_courses(self, parent_frame):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get courses not enrolled in by the student
            cursor.execute("""
                SELECT c.CourseID, c.CourseName, c.Description, i.First_Name, i.Last_Name,
                       c.MaxEnrollment, COUNT(e.StudentID) as CurrentEnrollment
                FROM Courses c
                LEFT JOIN Enrollment e ON c.CourseID = e.CourseID
                JOIN Instructors i ON c.InstructorID = i.InstructorID
                WHERE c.CourseID NOT IN (
                    SELECT CourseID FROM Enrollment WHERE StudentID = ?
                )
                GROUP BY c.CourseID
                HAVING CurrentEnrollment < c.MaxEnrollment
            """, (self.user_id,))
            
            courses = cursor.fetchall()
            
            for course in courses:
                course_frame = ctk.CTkFrame(parent_frame)
                course_frame.pack(pady=5, padx=5, fill='x')
                
                # Course title and instructor
                title_label = ctk.CTkLabel(
                    course_frame,
                    text=f"{course[1]} (Instructor: {course[3]} {course[4]})",
                    font=("Helvetica", 12, "bold")
                )
                title_label.pack(anchor='w')
                
                # Description
                desc_label = ctk.CTkLabel(
                    course_frame,
                    text=f"Description: {course[2]}"
                )
                desc_label.pack(anchor='w')
                
                # Enrollment info
                enrollment_label = ctk.CTkLabel(
                    course_frame,
                    text=f"Enrollment: {course[6]}/{course[5]}"
                )
                enrollment_label.pack(anchor='w')
                
                # Enroll button
                enroll_btn = ctk.CTkButton(
                    course_frame,
                    text="Enroll",
                    command=lambda cid=course[0]: self.enroll_in_course(cid)
                )
                enroll_btn.pack(pady=5)
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading courses: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def enroll_in_course(self, course_id):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check prerequisites
            if not self.check_prerequisites(course_id):
                messagebox.showerror("Error", "Prerequisites not met!")
                return
            
            # Check if course is full
            cursor.execute("""
                SELECT c.MaxEnrollment, COUNT(e.StudentID) as CurrentEnrollment
                FROM Courses c
                LEFT JOIN Enrollment e ON c.CourseID = e.CourseID
                WHERE c.CourseID = ?
                GROUP BY c.CourseID
            """, (course_id,))
            
            result = cursor.fetchone()
            if result[1] >= result[0]:
                messagebox.showerror("Error", "Course is full!")
                return
            
            # Enroll student
            cursor.execute("""
                INSERT INTO Enrollment (StudentID, CourseID, EnrollmentDate)
                VALUES (?, ?, ?)
            """, (self.user_id, course_id, datetime.now().date()))
            
            conn.commit()
            messagebox.showinfo("Success", "Enrolled successfully!")
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Already enrolled in this course!")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error enrolling: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def check_prerequisites(self, course_id):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get prerequisites for the course
            cursor.execute("""
                SELECT p.PrerequisiteCourseID
                FROM Prerequisite p
                WHERE p.CourseID = ?
            """, (course_id,))
            
            prerequisites = cursor.fetchall()
            
            # Check if student has completed all prerequisites
            for prereq in prerequisites:
                cursor.execute("""
                    SELECT 1
                    FROM Enrollment e
                    JOIN Performance p ON e.EnrollmentID = p.EnrollmentID
                    WHERE e.StudentID = ? AND e.CourseID = ? AND p.FinalGrade >= 60
                """, (self.user_id, prereq[0]))
                
                if not cursor.fetchone():
                    return False
                    
            return True
            
        except sqlite3.Error:
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    def create_analytics_view(self, parent_frame):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Active Users Section
            users_frame = ctk.CTkFrame(parent_frame)
            users_frame.pack(pady=10, padx=10, fill='x')
            
            ctk.CTkLabel(users_frame, text="Active Users", font=("Helvetica", 16, "bold")).pack()
            
            # Count active students and instructors
            cursor.execute("SELECT COUNT(*) FROM Students")
            student_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM Instructors")
            instructor_count = cursor.fetchone()[0]
            
            ctk.CTkLabel(users_frame, text=f"Total Students: {student_count}").pack()
            ctk.CTkLabel(users_frame, text=f"Total Instructors: {instructor_count}").pack()
            
            # Course Statistics Section
            courses_frame = ctk.CTkFrame(parent_frame)
            courses_frame.pack(pady=10, padx=10, fill='x')
            
            ctk.CTkLabel(courses_frame, text="Course Statistics", font=("Helvetica", 16, "bold")).pack()
            
            # Get popular courses
            cursor.execute("""
                SELECT c.CourseName, COUNT(e.StudentID) as Enrollment
                FROM Courses c
                LEFT JOIN Enrollment e ON c.CourseID = e.CourseID
                GROUP BY c.CourseID
                ORDER BY Enrollment DESC
                LIMIT 5
            """)
            
            popular_courses = cursor.fetchall()
            
            ctk.CTkLabel(courses_frame, text="Most Popular Courses:").pack()
            for course in popular_courses:
                ctk.CTkLabel(courses_frame, text=f"{course[0]}: {course[1]} students").pack()
            
            # Performance Metrics Section
            performance_frame = ctk.CTkFrame(parent_frame)
            performance_frame.pack(pady=10, padx=10, fill='x')
            
            ctk.CTkLabel(performance_frame, text="Performance Metrics", 
                        font=("Helvetica", 16, "bold")).pack()
            
            # Calculate average grades
            cursor.execute("""
                SELECT AVG(p.FinalGrade) as AvgGrade
                FROM Performance p
            """)
            
            avg_grade = cursor.fetchone()[0]
            if avg_grade:
                ctk.CTkLabel(performance_frame, 
                            text=f"Average Grade: {avg_grade:.2f}%").pack()
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading analytics: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def load_assessment_grades(self, parent_frame):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT c.CourseName, a.Title, s.Score, a.MaxScore
                FROM Courses c
                JOIN Enrollment e ON c.CourseID = e.CourseID
                JOIN Assessments a ON c.CourseID = a.CourseID
                LEFT JOIN Submissions s ON s.StudentID = e.StudentID 
                    AND s.AssessmentID = a.AssessmentID
                WHERE e.StudentID = ?
                ORDER BY c.CourseName, a.Title
            """, (self.user_id,))
            
            grades = cursor.fetchall()
            
            if not grades:
                no_grades_label = ctk.CTkLabel(
                    parent_frame,
                    text="No assessment grades available yet"
                )
                no_grades_label.pack(pady=20)
                return
            
            # Create header
            header_frame = ctk.CTkFrame(parent_frame)
            header_frame.pack(fill='x', padx=5, pady=(0, 10))
            
            headers = ["Course", "Assessment", "Score", "Max Score"]
            for header in headers:
                ctk.CTkLabel(
                    header_frame,
                    text=header,
                    font=("Helvetica", 12, "bold")
                ).pack(side='left', expand=True, fill='x', padx=5)
            
            # Add grades
            for grade in grades:
                grade_frame = ctk.CTkFrame(parent_frame)
                grade_frame.pack(fill='x', padx=5, pady=2)
                
                # Course name
                ctk.CTkLabel(
                    grade_frame,
                    text=grade[0]
                ).pack(side='left', expand=True, fill='x', padx=5)
                
                # Assessment title
                ctk.CTkLabel(
                    grade_frame,
                    text=grade[1]
                ).pack(side='left', expand=True, fill='x', padx=5)
                
                # Score
                score_text = f"{grade[2]}" if grade[2] is not None else "Not submitted"
                score_label = ctk.CTkLabel(
                    grade_frame,
                    text=score_text
                )
                score_label.pack(side='left', expand=True, fill='x', padx=5)
                
                # Color code the score
                if grade[2] is not None:
                    percentage = (grade[2] / grade[3]) * 100
                    if percentage >= 90:
                        score_label.configure(text_color='green')
                    elif percentage >= 70:
                        score_label.configure(text_color='orange')
                    else:
                        score_label.configure(text_color='red')
                
                # Max score
                ctk.CTkLabel(
                    grade_frame,
                    text=str(grade[3])
                ).pack(side='left', expand=True, fill='x', padx=5)
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading assessment grades: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def load_enrolled_courses(self, parent_frame):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT c.CourseID, c.CourseName, i.First_Name, i.Last_Name,
                       c.Description, p.TotalScore, p.Grade
                FROM Courses c
                JOIN Enrollment e ON c.CourseID = e.CourseID
                JOIN Instructors i ON c.InstructorID = i.InstructorID
                LEFT JOIN Performance p ON p.StudentID = e.StudentID 
                    AND p.StudentID = ?
                WHERE e.StudentID = ?
            """, (self.user_id, self.user_id))
            
            courses = cursor.fetchall()
            
            for course in courses:
                course_frame = ctk.CTkFrame(parent_frame)
                course_frame.pack(pady=5, padx=5, fill='x')
                
                # Course title and instructor
                title_label = ctk.CTkLabel(
                    course_frame,
                    text=f"{course[1]} (Instructor: {course[2]} {course[3]})",
                    font=("Helvetica", 12, "bold")
                )
                title_label.pack(anchor='w')
                
                # Description
                desc_label = ctk.CTkLabel(
                    course_frame,
                    text=f"Description: {course[4]}"
                )
                desc_label.pack(anchor='w')
                
                # Grade if available
                if course[5] is not None:
                    grade_text = f"Score: {course[5]}"
                    if course[6]:
                        grade_text += f" (Grade: {course[6]})"
                    
                    grade_label = ctk.CTkLabel(
                        course_frame,
                        text=grade_text
                    )
                    grade_label.pack(anchor='w')
                    
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading enrolled courses: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()
                
    def load_student_grades(self, parent_frame):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT c.CourseName, a.Title, s.Score, a.MaxScore,
                       p.FinalGrade
                FROM Courses c
                JOIN Enrollment e ON c.CourseID = e.CourseID
                JOIN Performance p ON e.EnrollmentID = p.EnrollmentID
                LEFT JOIN Submissions s ON e.EnrollmentID = s.EnrollmentID
                LEFT JOIN Assessments a ON s.AssessmentID = a.AssessmentID
                WHERE e.StudentID = ?
                ORDER BY c.CourseName, a.Title
            """, (self.user_id,))
            
            grades = cursor.fetchall()
            
            current_course = None
            course_frame = None
            
            for grade in grades:
                if current_course != grade[0]:
                    current_course = grade[0]
                    course_frame = ctk.CTkFrame(parent_frame)
                    course_frame.pack(pady=5, padx=5, fill='x')
                    
                    # Course title
                    ctk.CTkLabel(
                        course_frame,
                        text=f"Course: {grade[0]}",
                        font=("Helvetica", 12, "bold")
                    ).pack(anchor='w')
                    
                    # Final grade
                    if grade[4] is not None:
                        ctk.CTkLabel(
                            course_frame,
                            text=f"Final Grade: {grade[4]}%"
                        ).pack(anchor='w')
                
                # Assessment grades
                if grade[1] is not None:
                    assessment_frame = ctk.CTkFrame(course_frame)
                    assessment_frame.pack(pady=2, padx=20, fill='x')
                    
                    score_text = f"{grade[1]}: {grade[2]}/{grade[3]}"
                    if grade[3] > 0:
                        percentage = (grade[2] / grade[3]) * 100
                        score_text += f" ({percentage:.1f}%)"
                        
                    ctk.CTkLabel(
                        assessment_frame,
                        text=score_text
                    ).pack(anchor='w')
                    
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading grades: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()
                
    def load_student_assessments(self, parent_frame):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT c.CourseName, a.Title, a.Type,
                       a.DueDate, a.MaxScore, s.Score, s.SubmissionDate,
                       a.AssessmentID
                FROM Courses c
                JOIN Enrollment e ON c.CourseID = e.CourseID
                JOIN Assessments a ON c.CourseID = a.CourseID
                LEFT JOIN Submissions s ON s.StudentID = e.StudentID 
                    AND s.AssessmentID = a.AssessmentID
                WHERE e.StudentID = ?
                ORDER BY a.DueDate ASC
            """, (self.user_id,))
            
            assessments = cursor.fetchall()
            
            for assessment in assessments:
                assessment_frame = ctk.CTkFrame(parent_frame)
                assessment_frame.pack(pady=5, padx=5, fill='x')
                
                # Course and assessment title
                header_frame = ctk.CTkFrame(assessment_frame)
                header_frame.pack(fill='x', padx=5, pady=5)
                
                ctk.CTkLabel(
                    header_frame,
                    text=f"{assessment[0]} - {assessment[1]}",
                    font=("Helvetica", 12, "bold")
                ).pack(side='left')
                
                # Due date with color coding
                due_date = datetime.strptime(assessment[3], '%Y-%m-%d %H:%M:%S')
                formatted_date = due_date.strftime('%Y-%m-%d %H:%M')
                today = datetime.now()
                
                date_color = "green" if assessment[6] else (
                    "red" if due_date < today else "orange"
                )
                
                ctk.CTkLabel(
                    header_frame,
                    text=f"Due: {formatted_date}",
                    text_color=date_color
                ).pack(side='right')
                
                # Assessment type
                if assessment[2]:
                    ctk.CTkLabel(
                        assessment_frame,
                        text=f"Type: {assessment[2]}"
                    ).pack(anchor='w', padx=5)
                
                # Score if submitted
                if assessment[5] is not None:
                    score_frame = ctk.CTkFrame(assessment_frame)
                    score_frame.pack(fill='x', padx=5, pady=5)
                    
                    score = assessment[5]
                    max_score = assessment[4]
                    percentage = (score / max_score) * 100 if max_score > 0 else 0
                    
                    score_text = f"Score: {score}/{max_score} ({percentage:.1f}%)"
                    score_label = ctk.CTkLabel(
                        score_frame,
                        text=score_text
                    )
                    score_label.pack(side='left')
                    
                    # Color code the score
                    if percentage >= 90:
                        score_label.configure(text_color='green')
                    elif percentage >= 70:
                        score_label.configure(text_color='orange')
                    else:
                        score_label.configure(text_color='red')
                    
                    submission_date = datetime.strptime(assessment[6], '%Y-%m-%d %H:%M:%S')
                    formatted_submission = submission_date.strftime('%Y-%m-%d %H:%M')
                    ctk.CTkLabel(
                        score_frame,
                        text=f"Submitted: {formatted_submission}"
                    ).pack(side='right')
                    
                # Submit button if not submitted and not past due date
                elif due_date >= today:
                    submit_btn = ctk.CTkButton(
                        assessment_frame,
                        text="Submit Assessment",
                        command=lambda aid=assessment[7]: self.show_submission_dialog(aid)
                    )
                    submit_btn.pack(pady=5)
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading assessments: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()
                
    def load_assessments(self, parent_frame):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT c.CourseName, a.Title, a.Type,
                       a.DueDate, a.MaxScore, s.Score, s.SubmissionDate,
                       a.AssessmentID
                FROM Courses c
                JOIN Enrollment e ON c.CourseID = e.CourseID
                JOIN Assessments a ON c.CourseID = a.CourseID
                LEFT JOIN Submissions s ON s.StudentID = e.StudentID 
                    AND s.AssessmentID = a.AssessmentID
                WHERE e.StudentID = ?
                ORDER BY a.DueDate ASC
            """, (self.user_id,))
            
            assessments = cursor.fetchall()
            
            if not assessments:
                no_assessments_label = ctk.CTkLabel(
                    parent_frame,
                    text="No assessments available"
                )
                no_assessments_label.pack(pady=20)
                return
            
            # Create headers
            header_frame = ctk.CTkFrame(parent_frame)
            header_frame.pack(fill='x', padx=5, pady=(0, 10))
            
            headers = ["Course", "Assessment", "Due Date", "Status", "Score/Max"]
            for header in headers:
                ctk.CTkLabel(
                    header_frame,
                    text=header,
                    font=("Helvetica", 12, "bold")
                ).pack(side='left', expand=True, fill='x', padx=5)
            
            # Add assessments
            for assessment in assessments:
                assessment_frame = ctk.CTkFrame(parent_frame)
                assessment_frame.pack(fill='x', padx=5, pady=2)
                
                # Course name
                ctk.CTkLabel(
                    assessment_frame,
                    text=assessment[0]
                ).pack(side='left', expand=True, fill='x', padx=5)
                
                # Assessment title with tooltip for description
                title_label = ctk.CTkLabel(
                    assessment_frame,
                    text=assessment[1]
                )
                title_label.pack(side='left', expand=True, fill='x', padx=5)
                ToolTip(title_label, assessment[2] if assessment[2] else "No description available")
                
                # Due date
                due_date = datetime.strptime(assessment[3], '%Y-%m-%d %H:%M:%S')
                formatted_date = due_date.strftime('%Y-%m-%d %H:%M')
                ctk.CTkLabel(
                    assessment_frame,
                    text=formatted_date
                ).pack(side='left', expand=True, fill='x', padx=5)
                
                # Status with color coding
                status_label = ctk.CTkLabel(
                    assessment_frame,
                    text="Submitted" if assessment[6] else "Not submitted"
                )
                status_label.pack(side='left', expand=True, fill='x', padx=5)
                
                # Color code the status
                if assessment[6]:
                    status_label.configure(text_color='green')
                else:
                    status_label.configure(text_color='orange')
                
                # Score/Max with color coding
                score = assessment[5]
                max_score = assessment[4]
                score_text = f"{score if score is not None else '-'}/{max_score}"
                score_label = ctk.CTkLabel(
                    assessment_frame,
                    text=score_text
                )
                score_label.pack(side='left', expand=True, fill='x', padx=5)
                
                # Color code the score if it exists
                if score is not None:
                    percentage = (score / max_score) * 100
                    if percentage >= 90:
                        score_label.configure(text_color='green')
                    elif percentage >= 70:
                        score_label.configure(text_color='orange')
                    else:
                        score_label.configure(text_color='red')
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading assessments: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()
                
    def show_submission_dialog(self, assessment_id):
        dialog = ctk.CTkToplevel(self.menu_window)
        dialog.title("Submit Assessment")
        dialog.geometry("500x300")
        
        # Answer text area
        answer_label = ctk.CTkLabel(dialog, text="Your Answer:")
        answer_label.pack(pady=5)
        
        answer_text = ctk.CTkTextbox(dialog, height=150)
        answer_text.pack(pady=5, padx=10, fill='both', expand=True)
        
        def submit_assessment():
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Get enrollment ID
                cursor.execute("""
                    SELECT e.EnrollmentID
                    FROM Enrollment e
                    JOIN Assessments a ON e.CourseID = a.CourseID
                    WHERE e.StudentID = ? AND a.AssessmentID = ?
                """, (self.user_id, assessment_id))
                
                enrollment_id = cursor.fetchone()[0]
                
                # Insert submission
                cursor.execute("""
                    INSERT INTO Submissions (AssessmentID, EnrollmentID, 
                                          SubmissionDate, Answer)
                    VALUES (?, ?, ?, ?)
                """, (assessment_id, enrollment_id, 
                     datetime.now().date(), answer_text.get("1.0", "end-1c")))
                
                conn.commit()
                messagebox.showinfo("Success", "Assessment submitted successfully!")
                dialog.destroy()
                
                # Refresh assessments view
                self.notebook.select(3)  # Select assessments tab
                
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error submitting assessment: {str(e)}")
            finally:
                if 'conn' in locals():
                    conn.close()
                    
        submit_btn = ctk.CTkButton(dialog, text="Submit", command=submit_assessment)
        submit_btn.pack(pady=10)
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LoginApp()
    app.run()

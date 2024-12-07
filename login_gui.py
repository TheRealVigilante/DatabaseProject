import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

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
        login_window.grab_set()
        
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
        
    def show_main_menu(self, user_type):
        # Create new window for the main menu
        menu_window = ctk.CTkToplevel(self.root)
        menu_window.title(f"{user_type} Dashboard")
        menu_window.geometry("500x400")
        
        # Welcome message
        welcome_label = ctk.CTkLabel(
            menu_window,
            text=f"Welcome {self.user_name}!",
            font=("Helvetica", 24)
        )
        welcome_label.pack(pady=20)
        
        # Add different options based on user type
        if user_type == "Admin":
            self.create_admin_menu(menu_window)
        elif user_type == "Instructor":
            self.create_instructor_menu(menu_window)
        else:  # Student
            self.create_student_menu(menu_window)
            
    def create_admin_menu(self, window):
        # Add admin-specific buttons
        ctk.CTkButton(window, text="Manage Users", 
                     command=lambda: messagebox.showinfo("Info", "Manage Users clicked")).pack(pady=10)
        ctk.CTkButton(window, text="View System Logs", 
                     command=lambda: messagebox.showinfo("Info", "View Logs clicked")).pack(pady=10)
                     
    def create_instructor_menu(self, window):
        # Add instructor-specific buttons
        ctk.CTkButton(window, text="View Courses", 
                     command=lambda: messagebox.showinfo("Info", "View Courses clicked")).pack(pady=10)
        ctk.CTkButton(window, text="Manage Assessments", 
                     command=lambda: messagebox.showinfo("Info", "Manage Assessments clicked")).pack(pady=10)
                     
    def create_student_menu(self, window):
        # Add student-specific buttons
        ctk.CTkButton(window, text="View Enrolled Courses", 
                     command=lambda: messagebox.showinfo("Info", "View Courses clicked")).pack(pady=10)
        ctk.CTkButton(window, text="View Grades", 
                     command=lambda: messagebox.showinfo("Info", "View Grades clicked")).pack(pady=10)
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LoginApp()
    app.run()

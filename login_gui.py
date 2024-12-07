import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

class LoginApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Database Management System")
        self.root.geometry("400x300")
        
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
            # TODO: Implement actual verification logic
            if self.verify_credentials(user_type, username, password):
                messagebox.showinfo("Success", f"Welcome {username}!")
                login_window.destroy()
            else:
                messagebox.showerror("Error", "Invalid credentials!")
        
        login_btn = ctk.CTkButton(
            login_window,
            text="Login",
            command=verify_login
        )
        login_btn.pack(pady=20)
        
    def verify_credentials(self, user_type, username, password):
        # TODO: Implement actual verification logic using data from main.ipynb
        # This is a placeholder that always returns False
        return False
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LoginApp()
    app.run()

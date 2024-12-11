# University Management System

## Overview
The University Management System is a comprehensive database-driven application designed to streamline the management of educational institutions. This system efficiently handles courses, students, instructors, and assessments through an intuitive graphical user interface built with CustomTkinter and SQLite.

## Problem Statement
Educational institutions often face challenges in:
- Managing complex relationships between courses, students, and instructors
- Tracking student progress and assessment submissions
- Maintaining consistent data across different aspects of the institution
- Providing real-time updates and performance metrics
- Organizing course schedules and instructor assignments

## Solution
Our system provides a robust solution through:
- A relational database design that ensures data consistency and reduces redundancy
- Role-based access control for students, instructors, and administrators
- Real-time tracking of student performance and assessment submissions
- Efficient course management and enrollment system
- User-friendly interface for all stakeholders

## Features

### For Students
- View and enroll in available courses
- Track assessment deadlines and submissions
- Monitor grades and performance
- View course prerequisites
- Submit assignments and track progress

### For Instructors
- Manage course content and assessments
- Track student submissions
- Grade assignments
- View course statistics and performance metrics
- Manage course schedules

### For Administrators
- Manage user accounts (students and instructors)
- Create and modify courses
- Monitor system-wide analytics
- Handle course prerequisites and enrollment rules

## Technical Details

### Built With
- Python 3.12
- CustomTkinter (Modern GUI Framework)
- SQLite3 (Database)
- Tkinter (GUI Base Library)

### Database Design
The system uses a normalized relational database with tables for:
- Users (Students, Instructors)
- Courses
- Enrollments
- Assessments
- Submissions
- Performance Records

## Installation

1. Clone the repository:
```bash
git clone https://github.com/TheRealVigilante/DatabaseProject
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python login_gui.py
```

## Usage

### Student Access
1. Log in with student credentials
2. Navigate through the dashboard to:
   - View enrolled courses
   - Check available courses
   - Submit assessments
   - Track grades

### Instructor Access
1. Log in with instructor credentials
2. Use the dashboard to:
   - Manage course content
   - Create assessments
   - Grade submissions
   - View course statistics

### Administrator Access
1. Log in with admin credentials
2. Access administrative functions to:
   - Manage users
   - Create/modify courses
   - View system analytics

## Features in Detail

### Course Management
- Create and modify courses
- Set prerequisites
- Manage enrollment limits
- Track course statistics

### Assessment System
- Multiple assessment types support
- Automated deadline tracking
- Grade calculation and statistics
- Submission history

### User Management
- Role-based access control
- Profile management
- Activity tracking
- Performance analytics

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Special thanks to domain experts and database development professionals who provided valuable insights
- CustomTkinter community for the modern GUI framework
- SQLite team for the reliable database engine

## Project Status
This project is actively maintained and updated regularly with new features and improvements.

# Academic-Progress-Monitor
Welcome to the repository for the Academic Progress Monitor, a console-based Python application designed for educators, students, and academic institutions to track and analyze academic progress using powerful data management and visualization tools.

## Overview
The Academic Progress Monitor is a Python application that leverages the robustness of PostgreSQL for data management and the flexibility of Matplotlib for data visualization. This combination allows for efficient data handling and detailed graphical representation of academic metrics, making it an excellent tool for academic tracking.

## Features
1. Console-Based Interface: Provides a command-line interface for easy data management and operations.
2. PostgreSQL Database: Utilizes PostgreSQL to ensure robust, secure, and scalable data management.
3. Data Visualization with Matplotlib: Generates comprehensive charts and graphs to visually summarize academic progress.
4. Report Generation: Creates detailed reports with graphical data presentations to facilitate academic assessment and planning.

## Installation
 ### Prerequisites:
 1. Python (3.8 or above recommended)
 2. pip (Python package installer)
 3. PostgreSQL (Ensure PostgreSQL is installed and running on your system)

 ### Steps:
 1. Clone the repository:
    ```
    git clone https://github.com/CodeBurnerrr/Academic-Progress-Monitor.git
    ```
 3. Navigate to the project directory:
    ```
    cd Academic-Progress-Monitor
    ```
 5. Install required Python packages:
    ```
    pip install psycopg2 matplotlib prettytable numpy
    ```
 7. Set up the PostgreSQL database:
    * Ensure PostgreSQL is installed and running.
    * Create a database named Student.
    * Restore the sql file provided in the Student database.
    * After you restore sql file, add valid email address in admin_credentials table and student_details table.
 8. Set up sender mail address:
    * In mail.py update sender_email and sender_password.
    * To update refer this video : https://youtube.com/shorts/n9Ooxum-iUo?si=uwrhEo26S_Qj9zsC

## Usage
Configure the database connection settings in main.py specifying your PostgreSQL username, password, and database name.
+ Start the application by running:
  ```
  python main.py
  ```
+ Follow the command-line prompts to enter and manage academic data.
+ Utilize the visualization features to generate graphical representations of the data stored in PostgreSQL.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Authors
- [Dhruv Mehta](https://github.com/CodeBurnerrr) - CodeBurnerrr
- [Janvi Kapadia](https://github.com/janvikapadia) - janvikapadia

## Acknowledgments
- Send Email using Python in 60s (https://youtube.com/shorts/n9Ooxum-iUo?si=uwrhEo26S_Qj9zsC) by [@CodewithSJ](https://github.com/jha-shubham01) - For providing code snippets used in this project.

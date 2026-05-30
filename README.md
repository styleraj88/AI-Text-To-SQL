# AI Text To SQL Premium System

## Project Overview

AI Text To SQL Premium System is a Flask-based intelligent web application that converts natural language questions into SQL queries using Artificial Intelligence.

This project allows users to interact with databases without manually writing SQL code.

Users can ask questions in English, Telugu, Hindi, or other languages, and the system automatically translates the question, generates SQL queries using the Llama3 AI model, executes them on MySQL databases, explains the generated SQL, and displays query results in an interactive dashboard.

The system also includes authentication, database monitoring, query logs, voice input, security validation, PDF report generation, and multilingual support.

---

## Main Objective

The main goal of this project is to simplify database interaction using Artificial Intelligence.

Instead of writing SQL syntax manually, users can simply type:

> "Show all students with marks greater than 80"

The system automatically:

* Understands the question
* Detects language
* Translates to English if required
* Generates SQL using AI
* Executes query in MySQL
* Shows results
* Explains generated SQL

---

## Technologies Used

### Backend Technologies

* Python
* Flask
* Flask Login
* MySQL Connector
* Requests Library
* Deep Translator
* LangDetect
* ReportLab

### Database

* MySQL Database

### Artificial Intelligence

* Ollama
* Llama3 Model

### Frontend Technologies

* HTML5
* CSS3
* JavaScript
* Font Awesome Icons
* Google Fonts

---

## Features

### 1. User Authentication System

This project includes a complete login system.

Users can:

* Register new account
* Login securely
* Logout
* Reset forgotten passwords

Authentication is implemented using:

* Flask Login Manager
* User Session Handling
* Login Required Route Protection

---

### 2. AI Text To SQL Generator

The core functionality of the system.

Users enter questions in plain language.

Example:

> Show all employees whose salary is greater than 50000

The AI model:

* Reads database schema
* Detects available tables
* Detects available columns
* Generates valid MySQL query
* Uses only existing database structure

---

### 3. Dynamic Database Detection

The application automatically loads:

* All available MySQL databases
* Tables inside each database

Users can select databases dynamically from the dashboard.

No hardcoded database list is required.

---

### 4. SQL Query Explanation

The system does not only generate SQL.

It also explains generated SQL queries in simple English.

Example:

Generated SQL:

```sql
SELECT * FROM students WHERE marks > 80;
```

AI Explanation:

> Retrieves student records where marks are greater than 80.

---

### 5. Multilingual Language Support

The system supports multiple languages.

Supported examples:

* English
* Telugu
* Hindi
* Tamil
* Other languages

Libraries used:

* Deep Translator
* LangDetect

The application automatically:

* Detects language
* Converts question into English
* Sends translated question to AI model

---

### 6. Dangerous SQL Query Detection

The system includes a security layer.

Dangerous SQL commands are detected.

Blocked examples:

* DROP
* DELETE
* ALTER
* TRUNCATE

Admin verification is required before execution.

This protects databases from accidental data loss.

---

### 7. Admin Verification Popup

When dangerous SQL is detected:

The application displays an Admin Verification Popup.

The administrator must enter the correct admin password before continuing.

This feature improves database security.

---

### 8. Voice Query Input

Users can interact using voice commands.

Features:

* Microphone button
* Speech recognition
* Automatic text conversion
* Auto query submission

Implemented using:

* JavaScript Web Speech API

---

### 9. Interactive Dashboard

The project includes a modern dashboard interface.

Dashboard cards display:

* Query execution time
* Selected database
* Total rows
* AI model
* Language mode
* Total queries
* Successful queries
* Failed queries
* Most used database

---

### 10. Query Audit Logs

All query activities are tracked.

Logs store:

* Username
* User question
* Generated SQL status
* Timestamp

Useful for:

* Monitoring
* Debugging
* Auditing

---

### 11. Query History System

Recent queries are saved using browser local storage.

Users can:

* View history
* Reuse previous questions
* Clear history

---

### 12. Dark Mode / Light Mode

Theme switching is supported.

Users can toggle:

* Dark Theme
* Light Theme

User preference is stored locally.

---

### 13. PDF Report Generation

The system can generate downloadable reports.

Generated reports include:

* Database name
* User question
* Generated SQL
* AI explanation
* Result table

Implemented using:

* ReportLab PDF Library

---

### 14. CSV Export Feature

Users can export query results as CSV files.

Useful for:

* Reporting
* Data analysis
* External usage

---

### 15. Database Viewer

The application displays:

* Available databases
* Available tables

Users can explore database structures directly inside the dashboard.

---

## Project Structure

```plaintext
TextToSQL_Project
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── forgot_password.html
```

---

## Required Installation

Install the following software before running the project.

### 1. Python

Install Python 3.x

Verify:

```bash
python --version
```

---

### 2. MySQL Server

Install MySQL Database Server.

Verify:

```bash
mysql --version
```

---

### 3. Ollama

Install Ollama.

---

### 4. Pull Llama3 Model

Run:

```bash
ollama pull llama3
```

---

## Python Package Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

Important libraries:

```bash
Flask
flask-login
mysql-connector-python
requests
deep-translator
langdetect
reportlab
```

---

## Running The Project

Start Flask server:

```bash
python app.py
```

Open browser:

```plaintext
http://127.0.0.1:5000
```

---

## Future Improvements

Possible future enhancements:

* User Roles
* Better Password Encryption
* Charts & Analytics
* Cloud Deployment
* AI Model Selection
* Query Optimization Suggestions
* API Integration

---

## Author

**Naveen**

AI Text To SQL Premium System using Flask + MySQL + Ollama + Llama3

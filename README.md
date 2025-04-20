# Python Projects Collection

This repository contains a collection of Python applications from my CODSOFT internship.

## Projects Overview

### 1. Simple Calculator
A command-line calculator application that performs basic arithmetic operations:
- Addition, subtraction, multiplication, and division
- Input validation and error handling for division by zero
- Option to perform multiple calculations in sequence

### 2. Contact Management System
A comprehensive GUI-based contact management application built with PyQt5 and MySQL:
- Store, update, and delete contact information
- Search functionality to find contacts by name, phone, or email
- User-friendly interface with form validation
- Database connectivity with error handling

### 3. Password Generator
A customizable password generator with the following features:
- Configurable password length
- Options to include lowercase letters, uppercase letters, digits, and special characters
- Error handling to ensure at least one character type is selected

### 4. Rock Paper Scissors Game
A simple command-line implementation of the classic game:
- Player vs. computer gameplay
- Score tracking throughout multiple rounds
- End-game summary with winner announcement

## Setup Instructions

### Database Setup for Contact App
1. Run the SQL script `databasequery.sql` to create the necessary database and tables:
```
mysql -u root -p < databasequery.sql
```
2. Make sure MySQL server is running before starting the Contact App

### Required Dependencies
- Python 3.x
- PyQt5 (for Contact Management System)
- mysql-connector-python (for Contact Management System)

Install dependencies:
```
pip install PyQt5 mysql-connector-python
```

## Running the Applications

1. **Calculator**:
```
python CALCULATOR.py
```

2. **Contact Management System**:
```
python contactApp.py
```

3. **Password Generator**:
```
python password_generator.py
```

4. **Rock Paper Scissors Game**:
```
python rock_paper_scissors.py
```

## Notes
- The Contact Management System requires a MySQL database connection. Check the connection parameters in the `DatabaseConnection` class if you encounter connection issues.
- You may need to modify the database credentials in the Contact App to match your MySQL setup.

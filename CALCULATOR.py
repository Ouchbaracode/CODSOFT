# Task 2 CALCULATOR
# This program is a simple calculator that performs addition, subtraction, multiplication, and division.


A = float(input("Enter first number: "))
B = float(input("Enter second number: "))

operation = input("Enter operation (+, -, *, /): ")

if operation == '+':
    result = A + B
    print(f"{A} + {B} = {result}")
    
elif operation == '-':
    result = A - B
    print(f"{A} - {B} = {result}")
elif operation == '*':
    result = A * B
    print(f"{A} * {B} = {result}")
elif operation == '/':
    if B != 0:
        result = A / B
        print(f"{A} / {B} = {result}")
    else:
        print("Error: Division by zero is not allowed.")
else:
    print("Error: Invalid operation. Please enter +, -, *, or /.") 
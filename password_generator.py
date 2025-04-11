# Task N 3 password Generator
# This program generates a random password based on user-defined criteria.

import random

print("Welcome to the Password Generator!")
print("You can customize your password by choosing the following options:") 

password_length = int(input("Enter the desired password length: "))

include_lowercase = input("Include lowercase letters? (y/n): ").lower() == 'y'

include_uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'

include_digits = input("Include digits? (y/n): ").lower() == 'y'

include_special_characters = input("Include special characters? (y/n): ").lower() == 'y'


password_characters = {
    'lowercase': 'abcdefghijklmnopqrstuvwxyz',
    'uppercase': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'digits': '0123456789',
    'special_characters': '!@#$%^&*()-_=+[]{ };:,.<>?'
}

def generate_password(length, include_lowercase, include_uppercase, include_digits, include_special_characters):
    characters = ''
    if include_lowercase:
        characters += password_characters['lowercase']
    if include_uppercase:
        characters += password_characters['uppercase']
    if include_digits: 
        characters += password_characters['digits']
    if include_special_characters:
        characters += password_characters['special_characters']
        
    # Ensure at least one character type is selected 
    if not characters:
        raise ValueError("At least one character type must be selected.")

    password = ""
    for i in range(length):
        password += random.choice(characters)
    return password

print("Your password is:", generate_password(password_length, include_lowercase, include_uppercase, include_digits, include_special_characters))
print("Thank you for using the Password Generator!")

    

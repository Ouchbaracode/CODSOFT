import sys
import mysql.connector
from mysql.connector import Error
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QHBoxLayout, QListWidget, QMessageBox,
    QGroupBox, QGridLayout, QFrame, QSplitter, QListWidgetItem
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont

class DatabaseConnection:
    def __init__(self):
        self.connection_params = {
            "host": "localhost",
            "user": "root",
            "password": "Mohamed@mysql",
            "database": "contactapp"
        }
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.connection_params)
            self.cursor = self.connection.cursor()
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
        return True

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            if query.strip().lower().startswith("select"):
                result = self.cursor.fetchall()
                return result
            else:
                self.connection.commit()   
                return True
        except Error as e:
            print(f"Error executing query: {e}")
            return None if query.strip().lower().startswith("select") else False

def insert_contact(db, name, phone, email, address):
    sql = "INSERT INTO contacts (name, phone, email, address) VALUES (%s, %s, %s, %s)"
    val = (name, phone, email, address)
    if db.execute_query(sql, val):
        return db.cursor.lastrowid
    return None


def load_contacts(db):
    sql = "SELECT * FROM contacts"
    return db.execute_query(sql)

def search_contact(db, search_term):
    sql = "SELECT * FROM contacts WHERE name LIKE %s OR email LIKE %s OR phone LIKE %s OR address LIKE %s"
    val = (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
    return db.execute_query(sql, val)

def delete_contact(db, contact_id):
    sql = "DELETE FROM contacts WHERE id = %s"
    val = (contact_id,)
    if db.execute_query(sql, val):
        return True
    return False 

def update_contact(db, contact_id, name=None, phone=None, email=None, address=None):
    result = db.execute_query("SELECT name, phone, email, address FROM contacts WHERE id = %s", (contact_id,))
    current_data = result[0] if result else None

    if not current_data:
        return False

    if name is None:
        name = current_data[0]
    if phone is None:
        phone = current_data[1]
    if email is None:
        email = current_data[2]
    if address is None:
        address = current_data[3]

    sql = "UPDATE contacts SET name = %s, phone = %s, email = %s, address = %s WHERE id = %s"
    val = (name, phone, email, address, contact_id)

    return db.execute_query(sql, val)

class ContactApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contact Management App")
        self.setGeometry(200, 200, 800, 600)
        self.selected_contact_id = None
        self.db = None

        app_font = QFont("Arial", 10)
        self.setFont(app_font)

        try:
            self.db = DatabaseConnection()
            self.db.connect()
            print("Database connected successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Database Connection Error",
                                f"Failed to connect to the database.\nError: {e}")
            print(f"Database connection failed: {e}")
       
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        self.create_header()
        
        self.splitter = QSplitter(Qt.Vertical)
        self.main_layout.addWidget(self.splitter)
        
        self.create_contact_form()
        
        self.create_contact_list()
        
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: gray; font-style: italic;")
        self.main_layout.addWidget(self.status_label)
        
        if self.db:
            try:
                self.load_all_contacts()
                self.status_label.setText("Contacts loaded successfully")
                print("Initial contacts loaded.")
            except Exception as e:
                QMessageBox.critical(self, "Load Error",
                                    f"Failed to load contacts on startup.\nError: {e}")
                print(f"Error loading contacts on startup: {e}")
                self.status_label.setText("Error loading contacts")
    
    def create_header(self):
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #4a86e8; color: white;")
        header_layout = QHBoxLayout()
        header_frame.setLayout(header_layout)
        
        title_label = QLabel("Contact Management System")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        header_layout.addWidget(title_label)
        
        self.main_layout.addWidget(header_frame)
    
    def create_contact_form(self):
        form_frame = QFrame()
        form_frame.setFrameShape(QFrame.StyledPanel)
        form_layout = QVBoxLayout()
        form_frame.setLayout(form_layout)
        
        contact_group = QGroupBox("Contact Details")
        contact_layout = QGridLayout()
        contact_group.setLayout(contact_layout)
        
        contact_layout.addWidget(QLabel("Name:"), 0, 0)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter contact name")
        contact_layout.addWidget(self.name_input, 0, 1, 1, 2)
        
        contact_layout.addWidget(QLabel("Phone:"), 1, 0)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter phone number")
        contact_layout.addWidget(self.phone_input, 1, 1, 1, 2)
        
        contact_layout.addWidget(QLabel("Email:"), 2, 0)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email address")
        contact_layout.addWidget(self.email_input, 2, 1, 1, 2)
        
        contact_layout.addWidget(QLabel("Address:"), 3, 0)
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Enter physical address")
        contact_layout.addWidget(self.address_input, 3, 1, 1, 2)
        
        form_layout.addWidget(contact_group)
        
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Add Contact")
        self.add_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.add_button.clicked.connect(self.add_contact)
        button_layout.addWidget(self.add_button)
        
        self.update_button = QPushButton("Update Contact")
        self.update_button.setStyleSheet("background-color: #2196F3; color: white;")
        self.update_button.clicked.connect(self.update_contact)
        button_layout.addWidget(self.update_button)
        
        self.delete_button = QPushButton("Delete Contact")
        self.delete_button.setStyleSheet("background-color: #f44336; color: white;")
        self.delete_button.clicked.connect(self.delete_contact)
        button_layout.addWidget(self.delete_button)
        
        self.clear_button = QPushButton("Clear Form")
        self.clear_button.clicked.connect(self.clear_inputs)
        button_layout.addWidget(self.clear_button)
        
        form_layout.addLayout(button_layout)
        
        self.splitter.addWidget(form_frame)
        
    def create_contact_list(self):
        list_frame = QFrame()
        list_frame.setFrameShape(QFrame.StyledPanel)
        list_layout = QVBoxLayout()
        list_frame.setLayout(list_layout)
        
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, phone, email or address...")
        self.search_input.textChanged.connect(self.search_contacts)
        search_layout.addWidget(self.search_input)
        
        list_layout.addLayout(search_layout)
        
        contacts_group = QGroupBox("Contacts")
        contacts_layout = QVBoxLayout()
        contacts_group.setLayout(contacts_layout)
        
        self.contact_list = QListWidget()
        self.contact_list.setAlternatingRowColors(True)
        self.contact_list.setStyleSheet("""
            QListWidget::item { padding: 5px; border-bottom: 1px solid #e0e0e0; }
            QListWidget::item:selected { background-color: #e3f2fd; color: black; }
            QListWidget::item:alternate { background-color: #f5f5f5; }
        """)
        self.contact_list.itemClicked.connect(self.load_contact_details)
        contacts_layout.addWidget(self.contact_list)
        
        list_layout.addWidget(contacts_group)
        
        self.splitter.addWidget(list_frame)

    def add_contact(self):
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        address = self.address_input.text().strip()

        if not name or not phone or not email:
            QMessageBox.warning(self, "Input Error", "Please fill in Name, Phone, and Email fields.")
            return

        if self.db:
            try:
                insert_contact(self.db, name, phone, email, address)
                QMessageBox.information(self, "Success", "Contact added successfully!")
                self.status_label.setText(f"Added contact: {name}")
                self.clear_inputs()
                self.load_all_contacts()
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Error adding contact:\n{e}")
                print(f"Error adding contact: {e}")
                self.status_label.setText("Error adding contact")
        else:
            QMessageBox.warning(self, "Connection Error", "Database not connected.")
            self.status_label.setText("Database not connected")

    def load_all_contacts(self):
        self.contact_list.clear()
        if self.db:
            try:
                contacts = load_contacts(self.db)
                if contacts:
                    for contact in contacts:
                        item_text = f"{contact[0]} | {contact[1]} | {contact[2]} | {contact[3]} | {contact[4]}"
                        item = QListWidgetItem(item_text)
                        item.setToolTip(f"ID: {contact[0]}\nName: {contact[1]}\nPhone: {contact[2]}\nEmail: {contact[3]}\nAddress: {contact[4]}")
                        self.contact_list.addItem(item)
                    self.status_label.setText(f"Loaded {len(contacts)} contacts")
                else:
                    self.status_label.setText("No contacts found")
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Error loading contacts:\n{e}")
                print(f"Error loading contacts: {e}")
                self.status_label.setText("Error loading contacts")

    def load_contact_details(self, item):
        item_text = item.text()
        parts = item_text.split(" | ")

        if len(parts) == 5:
            try:
                self.selected_contact_id = int(parts[0])
                self.name_input.setText(parts[1])
                self.phone_input.setText(parts[2])
                self.email_input.setText(parts[3])
                self.address_input.setText(parts[4])
                self.status_label.setText(f"Selected contact: {parts[1]}")
            except (ValueError, IndexError) as e:
                QMessageBox.warning(self, "Data Error", f"Could not parse contact details from list item:\n{item_text}\nError: {e}")
                print(f"Error parsing list item: {item_text} - {e}")
                self.clear_inputs() 
                self.status_label.setText("Error loading contact details")
        else:
            QMessageBox.warning(self, "Data Error", f"Unexpected format for list item: {item_text}")
            print(f"Unexpected list item format: {item_text}")
            self.clear_inputs()
            self.status_label.setText("Error loading contact details")

    def search_contacts(self):
        search_term = self.search_input.text().strip()
        self.contact_list.clear()

        if not self.db:
            print("Search attempted, but database not connected.")
            self.status_label.setText("Database not connected")
            return

        try:
            if search_term:
                results = search_contact(self.db, search_term)
                if results:
                    for contact in results:
                        item_text = f"{contact[0]} | {contact[1]} | {contact[2]} | {contact[3]} | {contact[4]}"
                        item = QListWidgetItem(item_text)
                        item.setToolTip(f"ID: {contact[0]}\nName: {contact[1]}\nPhone: {contact[2]}\nEmail: {contact[3]}\nAddress: {contact[4]}")
                        self.contact_list.addItem(item)
                    self.status_label.setText(f"Found {len(results)} contacts matching '{search_term}'")
                else:
                    self.status_label.setText(f"No contacts found matching '{search_term}'")
            else:
                self.load_all_contacts()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Error searching contacts:\n{e}")
            print(f"Error searching contacts: {e}")
            self.status_label.setText("Error searching contacts")

    def update_contact(self):
        if self.selected_contact_id is None:
            QMessageBox.warning(self, "Select Contact", "Please select a contact from the list to update.")
            return

        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        address = self.address_input.text().strip()

        if not name and not phone and not email and not address:
            QMessageBox.warning(self, "Input Error", "Please enter new details for the contact.")
            return

        if self.db:
            try:
                update_contact(
                    self.db,
                    self.selected_contact_id,
                    name,
                    phone,
                    email,
                    address
                )
                QMessageBox.information(self, "Success", "Contact updated successfully!")
                self.status_label.setText(f"Updated contact: {name}")
                self.clear_inputs()
                self.load_all_contacts()
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Error updating contact:\n{e}")
                print(f"Error updating contact: {e}")
                self.status_label.setText("Error updating contact")
        else:
            QMessageBox.warning(self, "Connection Error", "Database not connected.")
            self.status_label.setText("Database not connected")

    def delete_contact(self):
        if self.selected_contact_id is None:
            QMessageBox.warning(self, "Select Contact", "Please select a contact from the list to delete.")
            return

        reply = QMessageBox.question(self, 'Confirm Delete',
                                    "Are you sure you want to delete this contact?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self.db:
                try:
                    contact_name = self.name_input.text()
                    
                    delete_contact(self.db, self.selected_contact_id)
                    QMessageBox.information(self, "Success", "Contact deleted successfully!")
                    self.status_label.setText(f"Deleted contact: {contact_name}")
                    self.clear_inputs()
                    self.load_all_contacts()
                except Exception as e:
                    QMessageBox.critical(self, "Database Error", f"Error deleting contact:\n{e}")
                    print(f"Error deleting contact: {e}")
                    self.status_label.setText("Error deleting contact")
            else:
                QMessageBox.warning(self, "Connection Error", "Database not connected.")
                self.status_label.setText("Database not connected")

    def clear_inputs(self):
        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.address_input.clear()
        self.selected_contact_id = None
        self.status_label.setText("Form cleared")

    def closeEvent(self, event):
        if self.db:
            self.db.disconnect()
            print("Database disconnected.")
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = ContactApp()
    window.show()
    sys.exit(app.exec_())
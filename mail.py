import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, 
                             QMessageBox, QFileDialog, QRadioButton, QFormLayout, QVBoxLayout, QWidget, QTabWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv
import sqlite3

class ModernMailSenderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Modern Email Sender")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1F1F1F;  
            }
            QLabel, QLineEdit, QPushButton, QTextEdit, QRadioButton, QComboBox {
                color: #F5F5F5; 
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QPushButton {
                background-color: #3498DB;  
                color: white;
                border-radius: 5px;
                padding: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980B9;  
            }
            QLineEdit, QTextEdit {
                background-color: #2E2E2E;  
                border: 1px solid #555;
                border-radius: 3px;
                padding: 5px;
            }
            QRadioButton {
                color: #F5F5F5;
            }
            QComboBox {
                background-color: #2E2E2E;
                border: 1px solid #555;
            }
            QTabWidget::pane {
                border: 1px solid #3498DB;
            }
        """)

        self.initUI()

    def initUI(self):
        # Central Widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout Setup
        self.layout = QVBoxLayout(self.central_widget)

        # Tab Widget
        self.tabs = QTabWidget(self)
        self.layout.addWidget(self.tabs)

        self.new_tab()

    def new_tab(self):
        form_layout = QFormLayout()

        # Email settings
        self.label_email = QLabel("Your Email:", self)
        self.input_email = QLineEdit(self)
        form_layout.addRow(self.label_email, self.input_email)

        self.label_password = QLabel("Password:", self)
        self.input_password = QLineEdit(self)
        self.input_password.setEchoMode(QLineEdit.Password)
        form_layout.addRow(self.label_password, self.input_password)

        self.label_host = QLabel("Select Email Host:", self)
        self.combo_host = QComboBox(self)
        self.combo_host.addItem("Outlook")
        self.combo_host.addItem("Gmail")
        form_layout.addRow(self.label_host, self.combo_host)

        self.label_subject = QLabel("Subject:", self)
        self.input_subject = QLineEdit(self)
        form_layout.addRow(self.label_subject, self.input_subject)

        self.label_message = QLabel("Message:", self)
        self.input_message = QTextEdit(self)
        form_layout.addRow(self.label_message, self.input_message)

        # Email recipient for one-to-one
        self.label_to_email = QLabel("Recipient Email:", self)
        self.input_to_email = QLineEdit(self)
        self.input_to_email.setVisible(False)  # Initially hidden
        form_layout.addRow(self.label_to_email, self.input_to_email)

        # Radio Buttons for Send Type
        self.radio_one_to_one = QRadioButton("Send to One Email")
        self.radio_one_to_many = QRadioButton("Send to Many (CSV/SQLite)")
        self.radio_one_to_one.setChecked(True)
        form_layout.addRow(self.radio_one_to_one)
        form_layout.addRow(self.radio_one_to_many)

        # File/Database selection for bulk email
        self.btn_select_file = QPushButton("Select CSV File")
        self.btn_select_file.setEnabled(False)
        self.btn_select_file.clicked.connect(self.select_csv_file)
        form_layout.addRow(self.btn_select_file)

        self.btn_select_db = QPushButton("Select SQLite Database")
        self.btn_select_db.setEnabled(False)
        self.btn_select_db.clicked.connect(self.select_db_file)
        form_layout.addRow(self.btn_select_db)

        # Send Button
        self.btn_send = QPushButton("Send Email")
        self.btn_send.clicked.connect(self.send_mail)
        form_layout.addRow(self.btn_send)

        # Create tab layout
        new_tab_widget = QWidget()
        new_tab_widget.setLayout(form_layout)
        self.tabs.addTab(new_tab_widget, f"Email {self.tabs.count() + 1}")

        # Connect radio buttons to enable/disable file selection buttons
        self.radio_one_to_many.toggled.connect(self.update_file_selection)
        self.radio_one_to_one.toggled.connect(self.update_to_email_visibility)

    def update_file_selection(self):
        self.btn_select_file.setEnabled(self.radio_one_to_many.isChecked())
        self.btn_select_db.setEnabled(self.radio_one_to_many.isChecked())

    def update_to_email_visibility(self):
        self.input_to_email.setVisible(self.radio_one_to_one.isChecked())

    def select_csv_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if file_name:
            self.csv_file_path = file_name

    def select_db_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select SQLite Database", "", "Database Files (*.db)")
        if file_name:
            self.db_file_path = file_name

    def send_mail(self):
        try:
            host_choice = self.combo_host.currentIndex()
            email = self.input_email.text()
            password = self.input_password.text()
            subject = self.input_subject.text()
            message = self.input_message.toPlainText()

            if host_choice == 0:
                HOST = "smtp-mail.outlook.com"
                PORT = 587
            else:
                HOST = "smtp.gmail.com"
                PORT = 587

            if self.radio_one_to_one.isChecked():
                to_email = self.input_to_email.text()
                if to_email:
                    self.tool(email, to_email, password, HOST, PORT, subject, message)
                else:
                    QMessageBox.warning(self, "Input Error", "Please enter the recipient email.")
            elif self.radio_one_to_many.isChecked():
                if hasattr(self, 'csv_file_path'):
                    self.send_bulk_from_csv(email, password, HOST, PORT, subject, message)
                elif hasattr(self, 'db_file_path'):
                    self.send_bulk_from_db(email, password, HOST, PORT, subject, message)

            QMessageBox.information(self, "Success", "Email sent successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to send email: {e}")

    def tool(self, FROM_EMAIL, TO_EMAIL, PASSWORD, HOST, PORT, subject, message):
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = TO_EMAIL
        msg['Subject'] = subject  
        msg.attach(MIMEText(message, 'plain', 'utf-8'))

        smtp = smtplib.SMTP(HOST, PORT)
        smtp.starttls()  
        smtp.login(FROM_EMAIL, PASSWORD)
        smtp.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
        smtp.quit()

    def send_bulk_from_csv(self, FROM_EMAIL, PASSWORD, HOST, PORT, subject, message):
        with open(self.csv_file_path) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                for to_email in row:
                    self.tool(FROM_EMAIL, to_email, PASSWORD, HOST, PORT, subject, message)

    def send_bulk_from_db(self, FROM_EMAIL, PASSWORD, HOST, PORT, subject, message):
        connection = sqlite3.connect(self.db_file_path)
        cursor = connection.cursor()
        cursor.execute("SELECT email FROM email")
        rows = cursor.fetchall()
        connection.close()

        for row in rows:
            to_email = row[0]
            self.tool(FROM_EMAIL, to_email, PASSWORD, HOST, PORT, subject, message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernMailSenderApp()
    window.show()
    sys.exit(app.exec_())

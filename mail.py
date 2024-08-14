import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass
import sqlite3
import csv





def send_mail():
    
        main_choice = input("Choose a host \n 1 : outlook \n 2 : gmail \n")

        if int(main_choice) != 1 and int(main_choice) != 2:
            raise ValueError(f"{main_choice} is invalid, Must use 1 or 2..")

        if int(main_choice) == 1:
            HOST = "smtp-mail.outlook.com"
            PORT = 587
        elif int(main_choice) == 2:
            HOST = "smtp.gmail.com"
            PORT = 587
        

        e_mail = input("Enter your e-mail: ")
        FROM_EMAIL = e_mail
        PASSWORD = getpass.getpass("Enter password: ")
        subject = input("Subject : ")
        message = input("Text your message :\n")

        choice_type = input("Choose a email send type \n 1 : one to one \n 2 : one to many ")

        if int(choice_type) == 1:
            to_email_one_to_one = input("Enter the to e-mail: ")
            TO_EMAIL = to_email_one_to_one
            tool(FROM_EMAIL,TO_EMAIL,PASSWORD,HOST,PORT,subject,message)
        
        if int(choice_type) == 2:
            print("""
            Warning; this usage just working with csv and sqlite3. 
            sqlite3 db name must be mail.db, and must be have one table also this table name should be email,
            If you will use csv, also name should be mail.csv""")
            
            read_type = input("1 : sqlite3, \n2 : csv \n")

            if int(read_type) == 1:
                    
                    connection = sqlite3.connect("mail.db")
                    cursor = connection.cursor()

                    cursor.execute("SELECT * FROM email")

                    rows = cursor.fetchall()
                    data = []
                    for row in rows:
                        data.append(row)
                
                    connection.close()
                    for mail in data:
                         for _ in mail:
                              TO_EMAIL = _
                              tool(FROM_EMAIL,TO_EMAIL,PASSWORD,HOST,PORT,subject,message)
            
            if int(read_type) == 2:
                 
                with open('mail.csv') as csvfile:
                     reader = csv.reader(csvfile)
                     
                     for row in reader:
                          for _ in row:
                            TO_EMAIL = _
                            tool(FROM_EMAIL,TO_EMAIL,PASSWORD,HOST,PORT,subject,message)
                        

def tool(FROM_EMAIL,TO_EMAIL,PASSWORD,HOST,PORT,subject,message):
        
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = TO_EMAIL
        msg['Subject'] = subject  
        msg.attach(MIMEText(message, 'plain', 'utf-8'))

        try:
            smtp = smtplib.SMTP(HOST, PORT)
            smtp.starttls()  

            status_code, response = smtp.ehlo()
            print(f"[*] Echoing the server: {status_code} {response}")

            status_code, response = smtp.login(FROM_EMAIL, PASSWORD)
            print(f"[*] Logging in: {status_code} {response}")

            smtp.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
            print("Email sent successfully!")

        except Exception as e:
            print(f"Failed to send email: {e}")

    

def main():
     send_mail()

if __name__ == "__main__":
     main()


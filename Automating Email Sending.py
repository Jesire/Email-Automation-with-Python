#import the necessary libraries
import os
import smtplib
from email.message import EmailMessage
import time
import schedule
import logging

# Define a function 'Email_Automation' where the script will be built
def Email_Automation():

    # Declare variables in which email credentials/login details (email id and password) will be stored
    # NB: gmail allows connection from eternal apps only if you use app password
    email_id='address@gmail.com'
    email_pass='password'

    # Declare recipient(s) list variable to store recipient addresses
    recipient_list=['address@gmail.com']

    # Declare an object instance of email message using the email library in the var 'msg'
    msg=EmailMessage()

    # Define the structure of the 'msg' by adding the email parts "Subject","From","To" 
    msg['Subject']='Email Subject'
    msg['From']=email_id
    msg['To']=recipient_list

    # Use the method "set_content" to add strings/texts to the body of the message
    msg.set_content('Input your message')

    # Locate the file(s) to use as attachments to the message and change the working directory to the path of the file(s) location
    # Use "chdir" method of the os library to change the cwd
    os.chdir(r'path of files to be attached')

    # Use a for loop to run through the files in the directory, open each file, read and add as attachment to the email
    for file in os.listdir():

        # Open each file in "read binary" mode, read, add file as attachment and close the file using "with_as"
        with open(file,'rb') as f: 
            file_data=f.read()
            file_name=f.name
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream',filename=file_name)

    # Create an instance of connection with a specified email server using the "smtp_ssl" method of the smtp library
    # Also specify the port number 
    # Alternately, smtp server can be used 
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:

        # Use the "login" method of smtp with the email_id and password
        smtp.login(email_id,email_pass)

        try:
            # Use the "send_message" of smtp to send the message
            smtp.send_message(msg)
            print('Email sent successfully')

            # Create a log file to keep records of the script excecutions
            logging.basicConfig(filename="logfilename.log", level=logging.DEBUG,format="%(asctime)s %(message)s")
            logging.info("Email sent successfully")
        except:
            print('An error occurred while sending email')
            logging.basicConfig(filename="logfilename.log", level=logging.DEBUG,format="%(asctime)s %(message)s")
            logging.warning("An error occurred while sending email")

Email_Automation()


# Use the schedule library to run the script daily at a specified time with the function "Email_Automation" as an input
schedule.every().day.at("HH:MM").do(Email_Automation)
while True:
    schedule.run_pending()
    time.sleep(1)
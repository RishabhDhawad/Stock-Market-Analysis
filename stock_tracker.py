'''
TODO:
NOTE: make sure to create separate functions for each task (email one function, WhatsApp one function)

1) Use Groww URL to scrape the name and price - DONE
2) Find the second child of a div using XPath - DONE
3) How to send an email using SMTP in Python - DONE
4) How to send WhatsApp message using Python (explore Twilio module) - DONE
7) Stock info(name and price) should be sent to Email and WhatsApp at 9:17 am IST, and how much is the difference in Plus/Minus from the last day, that info should  also be sent
8)      Last day price: 100 Rs Store it before 9 am
        Email: 9.17 am
        IRCON:
        Today's Price: 50 Rs
        Difference from yesterday: -50Rs and -50%

9)  Send the price alert every 15 minutes:    
        15 Minutes Alert:
        IRCON:203

- 1. create one single function for taking stock name and price - DONE
- 2. Send emails to multiple email ids -DONE
- 3. Changes in Mail function with function arguments - IN PROGRESS
- 4. search all possible scheduling packages in python and use the one which suites the most - IN PROGRESS

'''

import os
import time
import smtplib
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


# SCRAPING NAME AND PRICE OF THE STOCK
url = "https://groww.in/stocks/ircon-international-ltd"

def get_stock_data(url):
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        time.sleep(3)  # Allow JS to load

        # Get stock name
        name_element = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/h1")
        stock_name = name_element.text.strip()

        # Get stock price
        price_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/div[2]/div[3]/div/div[1]/span[2]')
        stock_price = price_element.text.strip()

        mail_response = sending_mail(stock_name, stock_price)
        if mail_response == "Success":
            print("Mail sent sucessfully")
        else:
            print("Mail failed")

    except Exception as e:
        print("Error fetching stock data:", e)
        return "Error", "Error"
    
    finally:
        driver.quit()

def sending_mail(stock_name, stock_price):
# def sending_mail(Sender, Receiver, Subject, Body):
    
    # loading sensitive data from env file
    sender_email = os.getenv("EMAIL_SENDER")
    app_password = os.getenv("APP_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL").split(",")

    subject = f"Stock Alert: {stock_name}"
    body = f"{stock_name}\nCurrent Price: ₹{stock_price}"

    # creating the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ",".join(receiver_email)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    #Creating a server for sending an email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email has been sent to " + ",".join(receiver_email))
        return "Success"
    except Exception as e:
        print("Failed to send email:", e)
        return "Failed"

"""
twilio module
datetime module
time module

1) twilio client setup
2) user inputs
3) scheduling logic
4) send message
"""


# SEND WHATSAPP MESSAGE
def send_whatsapp_msg(recipient_number, message_body):
    
    # Twilio Credentials
    account_sid = os.getenv('ACCOUNT_SID')
    auth_token = os.getenv('AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body = message_body,
            to = f"whatsapp:{recipient_number}"
        )
        print(f"Message sent sucessfully! Message SID{message.sid}")
    except Exception as e:
        print('An error occured', e)

# user input
recipient_name  = input('Enter the recipient name: ')
recepient_number = input('Enter the recipient whatsapp number with conuntry code (e.g, +91): ')
# custom_msg  = input(f"Enter the message you want to send to {recipient_name }: ")

# parse date/time and calculation delay
date_str = input("Enter the date to send the message (YYY-MM-DD) eg 2025-05-22: ")
time_str = input("Enter the time to send the message (HH:MM in 24 hour format): ")

#date time
schedule_datetime = datetime.strptime(f'{date_str} {time_str}', "%Y-%m-%d %H:%M")
current_datetime = datetime.now()

#calculate delay
time_difference = schedule_datetime - current_datetime
delay_seconds = time_difference.total_seconds()

if delay_seconds <= 0:
    print('The specified time is in the past. Please eanter a future date and time')
else:
    print(f'Message scheduled to be send to {recipient_name } at {schedule_datetime}')

    # Fetch stock data
    stock_name, stock_price = get_stock_data(url)
    
    # Compose message using fetched stock data
    custom_msg = f"""
    Hello {recipient_name},
    📈 Stock Alert:
    ✨ {stock_name}
    ✨ Current Price: ₹{stock_price}
    
    Stay updated and invest wisely!
    """

    #wait untill the schedule time
    time.sleep(delay_seconds) #1000

    #send the message
    send_whatsapp_msg(recepient_number, custom_msg)

    email_subject = f"Stock Alert: {stock_name}"
    email_status = sending_mail(email_subject, custom_msg)
    print("Mail send status: ", email_status)


# PRINTING ALL THE DATA

name, price = get_stock_data(url)
print("Stock Name:", name)
print("Stock Price:", price)

# email_status = sending_mail(name, price)
# print("Mail send status: ", email_status)

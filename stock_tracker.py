'''
TODO:
NOTE: make sure to create separate functions for each task (email one function, WhatsApp one function)

1) Use Groww URL to scrape the name and price - DONE
2) Find the second child of a div using XPath - DONE
3) How to send an email using SMTP in Python - DONE
4) How to send WhatsApp message using Python (explore Twilio module)
5) How to call Python script at a specific time
6) Find other Python packages for scheduling the job
7) Stock info(name and price) should be sent to Email and WhatsApp at 9:17 am IST, and how much is the difference in Plus/Minus from the last day, that info should  also be sent
8)      Last day price: 100 Rs Store it before 9 am
        Email: 9.17 am
        IRCON:
        Today's Price: 50 Rs
        Difference from yesterday: -50Rs and -50%

9)  Send the price alert every 15 minutes:    
        15 Minutes Alert:
        IRCON:203

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
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# SCRAPING NAME AND PRICE OF THE STOCK
url = "https://groww.in/stocks/ircon-international-ltd"

def get_stock_title(url):
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        time.sleep(1) # allow JS to load
        name_element = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/h1")
        return name_element.text.strip()
    
    except Exception as e:
        print("Error fetching title:", e)
        return "Error"
    
    finally:
        driver.quit()

def get_stock_price(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        time.sleep(3)  # allow JS to load
        price_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/div[2]/div[3]/div/div[1]/span[2]')
        return price_element.text.strip()
    
    except Exception as e:
        print("Error fetching price:", e)
        return "Error"
    
    finally:
        driver.quit()

def sending_mail(stock_name, stock_price):
    
    # loading sensitive data from env file
    sender_email = os.getenv("EMAIL_SENDER")
    app_password = os.getenv("EMAIL_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL")

    subject = f"Stock Alert: {stock_name}"
    body = f"{stock_name}\nCurrent Price: ₹{stock_price}"

    # creating the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    #Creating a server for sending an email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())

    print("Email has been sent to " + receiver_email)
    return "Success"


# PRINTING ALL THE DATA

name = get_stock_title(url)
print("Stock Name: ", name)

price  = get_stock_price(url)
print("Stock Price: ", price)

email_status = sending_mail(name, price)
print("Mail send status: ", email_status)

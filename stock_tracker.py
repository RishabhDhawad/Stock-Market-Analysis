import os
import time
import json
import smtplib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from twilio.rest import Client
from datetime import datetime, timedelta
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from whatsapp import WhatsApp
from mail import Mail

load_dotenv()

scheduler = BlockingScheduler()

# Configuration For this Project
url = "https://groww.in/stocks/ircon-international-ltd"
Sender = os.getenv("EMAIL_SENDER")
Receiver = os.getenv("RECEIVER_EMAIL").split(",")
# Twilio Credentials - For Whatsapp
recipient_name = os.getenv('RECIPIENT_NAME')
recipient_number = os.getenv('RECIPIENT_NUMBER')

# Scrapes the stock name and price from Groww using Selenium.
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

        return stock_name,stock_price

    except Exception as e:
        print("Error fetching stock data:", e)
        return "Error", "Error"
    
    finally:
        driver.quit()


# Sends an email via SMTP
def sending_mail(sender, receiver, subject, body):
    # Loading sensitive data from env file
    app_password = os.getenv("APP_PASSWORD")

    # Creating the email message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ",".join(receiver) if isinstance(receiver, list) else receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    # Creating a server for sending an email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, app_password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Email sent to {msg['To']}")
        return "Success"
    except Exception as e:
        print("Failed to send email:", e)
        return "Failed"


# Builds the message text for both email and WhatsApp.
def create_stock_message(stock_name, today_price, yesterday_price):
    diff = today_price - yesterday_price
    percent = (diff / yesterday_price) * 100 if yesterday_price else 0

    recipient_name = os.getenv("RECIPIENT_NAME", "User") 
    return f"""
    Hello {recipient_name},
    📈 Stock Alert:
    ✨ {stock_name}
    ✨ Current Price: ₹{today_price}
    ✨ Yesterday Price: ₹{yesterday_price}
    ✨ Difference: ₹{diff:2f} ({percent:+.2f}%)

    Stay updated and invest wisely!
    """


# Saves the stock's price to a JSON file.
def save_yesterday_price(stock_name, stock_price):
    data = {stock_name: stock_price}
    with open('yesterday_prices.json', 'w') as file:
        json.dump(data, file)


# Reads yesterday's stock price from the JSON file.
def get_yesterday_price(stock_name):
    try:
        if not os.path.exists("yesterday_prices.json"):
            print("Creating yesterday_prices.json with empty data.")
            with open('yesterday_prices.json', 'w') as f:
                json.dump({}, f)

        with open('yesterday_prices.json', 'r') as file:
            data = json.load(file)
            return float(data.get(stock_name))
    except (ValueError, TypeError):
        return None


# Sends daily summary email and WhatsApp at 9:17 AM.
def job_send_daily_summary():
    stock_name, stock_price = get_stock_data(url)
    try:
        stock_price = float(stock_price.replace(',',''))
    except:
        print("Stock price conversion failed")
        return
    
    yesterday_price = get_yesterday_price(stock_name)

    if stock_price is None or yesterday_price is None:
        print("Missing Price Data")
        return 
    
    message = create_stock_message(stock_name, stock_price, yesterday_price)

    mail_obj = Mail()
    mail_response = mail_obj.sending_mail(Sender, Receiver, subject=f"{stock_name} Daily Summary", body=message)
    print(mail_response)
    
    whatsapp_obj = WhatsApp()
    whatsapp_response = whatsapp_obj.send_message(recipient_number, message)
    print(whatsapp_response)


# Sends alerts every 15 minutes during market hours.
def job_send_15_min_alert():
    stock_name, stock_price = get_stock_data(url)
    try:
        stock_price = float(stock_price.replace(',',''))
    except:
        print("Stock price conversion failed")
        return
    
    yesterday_price = get_yesterday_price(stock_name)

    if stock_price is None or yesterday_price is None:
        print("Missing price Data")
        return

    message = create_stock_message(stock_name, stock_price, yesterday_price)

    mail_obj = Mail()
    mail_response = mail_obj.sending_mail(Sender, Receiver, subject=f"{stock_name} 15-Min Price Update", body=message)
    print(mail_response)
    
    whatsapp_obj = WhatsApp()
    whatsapp_response = whatsapp_obj.send_message(recipient_number, message)
    print(whatsapp_response)


# Saves the stock price at 4 PM to be used as yesterday's reference.
def job_save_yesterday_price():
    stock_name, stock_price = get_stock_data(url)
    
    try:
        stock_price = float(stock_price.replace(',',''))
        save_yesterday_price(stock_name, stock_price)
        print(f"Saved yesterday's price for {stock_name}: ₹{stock_price}")
    except:
        print("Failed to fetch or save yesterday's price")



# Main function
def main():
    print("Stock Price Monitoring Starting...")

    print("Testing Stock Data Fetch")
    stock_name, stock_price = get_stock_data(url)
    print(f"Stock Name: {stock_name}")
    print(f"Stock Price: {stock_price}")

    if stock_name == "Error" or stock_price == "Error":
        print("Warning: Initial stock data fetch failed. Check your internet connection and URL.")

    # Sets up and starts the APScheduler jobs.
    scheduler.add_job(
        job_save_yesterday_price,
        CronTrigger(hour=16, minute=0, day_of_week='mon-fri'),
        name="Save Yesterday's Price (4 PM)"
    )

    # Daily Summary eamil at 9:17 AM
    scheduler.add_job(
        job_send_daily_summary,
        CronTrigger(hour=9, minute=17, day_of_week='mon-fri'),
        name='Daily Summary Email'
    )

    # Alert every 15 minute
    scheduler.add_job(
        job_send_15_min_alert,
        CronTrigger(minute='*/15', hour='9-16', day_of_week='mon-fri'),
        name='15 min Alert'
    )

    print("Scheduler configured:")
    print("Daily Summary: 9:17 AM")
    print("15 min alerts: Every 15 min from 9 AM to 4 PM")
    print("\nStarting scheduler... Press Ctrl+C to stop")

    # starting scheduler 
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\nShutting down scheduler....")
        scheduler.shutdown()
        print("Scheduler stopped.")


if __name__ == "__main__":
    main()

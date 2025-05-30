# 📈 Stock Price Alert System

A Python-based automation system to track and alert stock prices from [Groww](https://groww.in) via **Email** and **WhatsApp**, with real-time updates every 15 minutes and a daily summary at 9:17 AM IST.

---

## 🚀 Features

- ✅ Scrape real-time **stock name** and **price** from Groww using Selenium
- ✅ Store previous day’s stock price at 4:00 PM
- ✅ Send **daily summary** email and WhatsApp message at 9:17 AM with:
  - Current Price
  - Yesterday's Price
  - ₹ Difference and % Change
- ✅ Send **15-minute interval alerts** during market hours (9:00 AM - 4:00 PM)
- ✅ Environment variable-based configuration
- ✅ Modularized code: mail and WhatsApp functionality in separate files


---

## 🛠️ Setup Instructions

### 1. Clone the repository

    
    git clone https://github.com/your-username/stock-price-alert.git
    cd stock-price-alert

### 2. Install Dependences

    pip install -r requirements.txt

### 3. Add Environment Variables
Create a .env file and fill it with your credentials:

    EMAIL_SENDER = youremail@gmail.com
    RECEIVER_EMAIL = receiver1@example.com,receiver2@example.com
    APP_PASSWORD = your_app_password
    RECIPIENT_NAME = John Doe
    RECIPIENT_NUMBER = whatsapp:+91xxxxxxxxxx
    TWILIO_ACCOUNT_SID = your_twilio_sid
    TWILIO_AUTH_TOKEN = your_twilio_token
    TWILIO_NUMBER = whatsapp:+14xxxxxxxxxx

💡 Gmail users need to generate an App Password from their Google Account if 2FA is enabled.

## 📬 Email Example

    Subject: IRCON Daily Summary

    Hello John Doe,
    📈 Stock Alert:
    ✨ IRCON
    ✨ Current Price: ₹203
    ✨ Yesterday Price: ₹200
    ✨ Difference: ₹3.00 (+1.50%)

    Stay updated and invest wisely!

## 🔗 Technologies Used

- Python 3
- Selenium – Web scraping
- BeautifulSoup – HTML parsing
- Twilio API – WhatsApp messaging
- SMTP – Email notifications
- APScheduler – Task scheduling
- dotenv – Environment variable management


## 📌 Notes

- Make sure ChromeDriver is compatible with your Chrome version.
- This script uses headless Chrome; ensure your system supports it.
- Run the script continuously (e.g., with a server or as a background service) to allow the scheduler to function properly.

## 📥 Run the Script

    python main.py

You’ll see scheduled tasks begin at their respective times. Press Ctrl + C to stop the scheduler.

## 📄 License
This project is licensed under the MIT License.

## 🙋‍♂️ Author

Made with ❤️ by Rishabh Dhawad

Feel free to reach out or contribute!
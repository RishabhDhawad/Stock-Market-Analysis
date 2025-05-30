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

    EMAIL_SENDER = your_email@email.com
    APP_PASSWORD = app_pass_from_gamil
    RECEIVER_EMAIL = you_want_to_send1@mail.com, you_want_to_send2@mail.com
    ACCOUNT_SID = your_account_sid
    AUTH_TOKEN = twilio_auth_token
    RECIPIENT_NAME = your_name
    RECIPIENT_NUMBER = +91xxxxxxxxxx
    TWILIO_WHATSAPP_NUMBER = +14xxxxxxxxxx


💡 Gmail users need to generate an App Password from their Google Account if 2FA is enabled.

## 📬 Email Example

    Subject: IRCON Daily Summary

    Hello Rishabh Dhawad,
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
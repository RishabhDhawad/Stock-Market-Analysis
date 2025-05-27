class WhatsApp:
    def send_message(self, recipient_number, message_body):
        from twilio.rest import Client
        import os
        account_sid = os.getenv('ACCOUNT_SID')
        auth_token = os.getenv('AUTH_TOKEN')
        try:
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                from_='whatsapp:os.env("TWILIO_WHATSAPP_NUMBER")',
                body=message_body,
                to=f"whatsapp:{recipient_number}"
            )
            print(f"Message sent successfully! Message SID: {message.sid}")
            return "Success"
        except Exception as e:
            print('Error sending WhatsApp message:', e)
            return "Failed" 
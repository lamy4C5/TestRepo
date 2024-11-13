from flask import Flask
from flask_mail import Mail, Message
from config import Config
import traceback
import ssl

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)

with app.app_context():
    try:
        # Print configuration for debugging
        print("\nMail Configuration:")
        print(f"MAIL_SERVER: {app.config['MAIL_SERVER']}")
        print(f"MAIL_PORT: {app.config['MAIL_PORT']}")
        print(f"MAIL_USE_TLS: {app.config['MAIL_USE_TLS']}")
        print(f"MAIL_USERNAME: {app.config['MAIL_USERNAME']}")
        print(f"MAIL_DEFAULT_SENDER: {app.config['MAIL_DEFAULT_SENDER']}")
        
        # Create and send test email
        msg = Message('Test Email',
                    sender=app.config['MAIL_DEFAULT_SENDER'],
                    recipients=['liamye0412@gmail.com'])
        msg.body = "This is a test email from Flask app."
        
        # Try to create SSL context
        context = ssl.create_default_context()
        
        # Send email
        mail.send(msg)
        print("\nEmail sent successfully!")
        
    except Exception as e:
        print(f"\nError sending email: {str(e)}")
        print("\nFull traceback:")
        print(traceback.format_exc()) 
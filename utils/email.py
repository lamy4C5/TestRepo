from flask_mail import Message
from flask import current_app
from threading import Thread
import random
import string

def generate_otp():
    """Generate 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))

def send_async_email(app, msg, mail):
    with app.app_context():
        mail.send(msg)

def send_otp_email(to_email, otp, mail):
    """Send OTP email"""
    msg = Message('Your OTP Verification Code',
                  recipients=[to_email])
    msg.body = f'Your OTP verification code is: {otp}'
    
    # Send email asynchronously
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg, mail)).start() 
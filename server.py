from flask import Flask, render_template, request, session, redirect, url_for
from helperFuncs import *
import random
from flask_mail import Mail
from config import Config
from utils.email import generate_otp, send_otp_email
import os
from functools import wraps
from flask_wtf.csrf import CSRFProtect
from flask_mail import Message

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = os.urandom(24)
csrf = CSRFProtect(app)
mail = Mail(app)

# Add login verification decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('Login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('homepage.html', message = "")

@app.route('/homepage/')
def homepage():
   return render_template('homepage.html', message = "")

@app.route('/SignUp/')
def SignUp():
    return render_template('SignUp.html')

@app.route('/SignUpRequest/', methods = ['GET', 'POST'])
def SignUpRequest():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')  # Get original password
        email = request.form.get('email', '')
        
        # Basic validation
        if not username or not password or not email:
            return render_template('SignUp.html', message="All fields are required")
            
        # Password length validation
        if len(password) < 3 or len(password) > 20:
            return render_template('SignUp.html', message="Password must be between 3 and 20 characters")
            
        # Hash the password
        hashed_password = hashText(password)
        
        # Call add user function
        success, message = addUser(username, hashed_password, email)
        
        if success:
            return render_template("Login.html", message="Sign up successful! Please login.")
        else:
            return render_template('SignUp.html', message=message)
            
    return render_template('SignUp.html')

@app.route('/Login/')
def Login():
  return render_template('Login.html',message = "")

@app.route('/LoginRequest/', methods=['GET', 'POST'])
def LoginRequest():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = hashText(request.form.get('password', ''))
        
        qlReturn = queryLogin(username, password)
        if qlReturn[0]:  # If login credentials are correct
            try:
                # Generate OTP
                otp = str(random.randint(100, 999))
                email = getEmailFromUsername(username)
                
                if not email:
                    return render_template("Login.html", message="Email not found for user")
                
                # Create and send email
                msg = Message('Your OTP Code',
                            sender=app.config['MAIL_DEFAULT_SENDER'],
                            recipients=[email])
                msg.body = f'Your OTP verification code is: {otp}'
                
                # Send the email
                mail.send(msg)
                
                # Save OTP to database and session
                if sendOTP(otp, username):
                    session['pending_username'] = username
                    return render_template("verification.html", email=email)
                
            except Exception as e:
                print(f"Error sending email: {e}")  # For debugging
                return render_template("Login.html", message="Failed to send OTP email. Please try again.")
        
        return render_template("Login.html", message=qlReturn[1])
    
    return render_template("Login.html", message="")

@app.route('/Verification')
def Verification():
   return render_template('verification.html', email = "ERROR")

@app.route('/VerificationRequest/', methods = ['GET','POST'])
def VerificationRequest():
    dv = "000"
    return render_template("secret_page.html",name = username)

@app.route('/send-otp', methods=['POST'])
def send_email():
    email = request.form.get('email')
    if not email:
        return 'Email is required', 400
    
    otp = generate_otp()
    session['otp'] = otp
    session['email'] = email
    
    try:
        send_otp_email(email, otp, mail)
        return redirect(url_for('verification'))
    except Exception as e:
        print(f"Error sending email: {e}")
        return 'Failed to send email', 500

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    if 'pending_username' not in session:
        return redirect(url_for('Login'))
        
    email = request.form.get('email')
    otp = request.form.get('otp')
    username = session['pending_username']
    
    if not email or not otp:
        return render_template('verification.html', 
                             email=email,
                             message='Email and OTP are required')
    
    # Verify OTP from database
    db = load_database()
    if username in db['users']:
        stored_otp = db['users'][username].get('otp')
        if stored_otp == otp:
            # Verification successful
            session['username'] = username  # Set login status
            session.pop('pending_username', None)  # Clear temporary username
            return redirect(url_for('secret_page'))
    
    return render_template('verification.html', 
                         email=email,
                         message='Invalid OTP')

@app.route('/secret-page')
@login_required
def secret_page():
    return render_template('secret_page.html', name=session.get('username'))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('homepage'))

if __name__ == '__main__':
  app.run(debug=True)
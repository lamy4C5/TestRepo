import hashlib
import json
import os

DATABASE_FILE = 'database.json'

def hashText(text):
    """Hash the input text using SHA-256"""
    return hashlib.sha256(text.encode()).hexdigest()

def load_database():
    """Load the database from file"""
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as f:
            return json.load(f)
    return {'users': {}}

def save_database(db):
    """Save the database to file"""
    with open(DATABASE_FILE, 'w') as f:
        json.dump(db, f, indent=4)

def addUser(username, password, email):
    """Add a new user to the database"""
    # Load current database
    db = load_database()
    
    # Check if username already exists
    if username in db['users']:
        return False, "Username already exists"
    
    # Check if email already exists
    for user in db['users'].values():
        if user['email'] == email:
            return False, "Email already registered"
    
    # Add new user
    db['users'][username] = {
        'password': password,
        'email': email
    }
    
    # Save updated database
    try:
        save_database(db)
        return True, "User registered successfully"
    except Exception as e:
        return False, f"Error saving user: {str(e)}"

def queryLogin(username, password):
    """Verify login credentials"""
    db = load_database()
    
    if username not in db['users']:
        return False, "Username not found"
    
    if db['users'][username]['password'] != password:
        return False, "Incorrect password"
    
    return True, "Login successful"

def getEmailFromUsername(username):
    """Get email address for a username"""
    db = load_database()
    
    if username in db['users']:
        return db['users'][username]['email']
    return None

def sendOTP(otp, username):
    """Store OTP for verification"""
    db = load_database()
    
    if username in db['users']:
        db['users'][username]['otp'] = otp
        save_database(db)
        return True
    return False
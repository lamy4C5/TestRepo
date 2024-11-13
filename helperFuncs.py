import hashlib
import smtplib

DATABASE_NAME = "database.txt"

def addUser(username,password,email):
    file = open(DATABASE_NAME, "r")
    retMsg  = ""
    retBool = True
    if not username.isalnum():
        retMsg = "INVALID USERNAME, MUST BE ALPHANUMERIC"
        retBool = False
    elif not (password.isalnum() and len(password >= 3 and len(password <= 20))):
        retMsg = "INVALID PASSWORD, MUST BE ALPHANUMERIC AND BETWEEN 3-20 CHARACTERS"
        retBool = False
    elif not (email.count("@") == 1 and email.split("@")[1].count(".") == 1):
        retMsg = "INVALID EMAIL"
        retBool = False

    if retBool == False: #no need to loop through file if already invalid
        return (retBool,retMsg)
    
    for line in file:
        user = line.split(",")
        if username.lower() == user[0].lower():
            retMsg =  "USER HAS ALREADY SIGNED UP"
            retBool = False
        elif email.lower() == user[2].lower():
            retMsg =  "EMAIL HAS ALREADY SIGNED UP"
            retBool = False
    file.close()
    
    
    if retBool == True: #if the signup is still good
        file = open(DATABASE_NAME,"w")
        file.write(username+","+password+","+email)
        retMsg =  "USER SIGNED UP SUCCESSFULLY"
        file.close()
    
    return (retBool,retMsg)

def queryLogin(username,encrypted_password):
    file = open(DATABASE_NAME,"r")
    retMsg = "USERNAME NOT FOUND"
    retBool = False
    for line in file:
        curUserStuff = line.split(",")
        #print(curUserStuff)
        #print("ur:"+username+" "+"pw:"+encrypted_password)
        if username == curUserStuff[0]:
            if encrypted_password == curUserStuff[1]:
                retMsg =  "LOGIN SUCCESSFUL"
                retBool = True
            else:
                retMsg =  "INCORRECT PASSWORD"
                retBool = False
    file.close()
    return (retBool,retMsg)
        
def hashText(text):
    hashed_password = hashlib.sha256(text.encode()).hexdigest()
    return hashed_password

def sendOTP(username):
    pass #https://www.geeksforgeeks.org/send-mail-gmail-account-using-python/
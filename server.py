from flask import Flask, render_template, request
from helperFuncs import *
import random

app = Flask(__name__)

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
    dv = "ERROR"
    username = request.form.get('username',dv)
    password = hashText(request.form.get('password',dv))
    email = request.form.get('email',dv)
    auReturn = addUser(username,password,email)
    if auReturn[0]: #successfully signed up user
       return render_template("homepage.html",message = auReturn[1])
    else:
       return render_template('SignUp.html',message = auReturn[1])

@app.route('/Login/')
def Login():
  return render_template('Login.html',message = "")

@app.route('/LoginRequest/', methods = ['GET', 'POST'])
def LoginRequest():
    dv = "ERROR"
    username = request.form.get('username',dv)
    password = hashText(request.form.get('password',dv))
    qlReturn = queryLogin(username,password)
    if qlReturn[0]: #successfully logged in (sunglasses emoji)
        key = str(random.randint(100,999))
        sendOTP(key,username)
        return render_template("verification.html",email = getEmailFromUsername(username))
    else: #did not log in (sob emoji)
        return render_template("Login.html", message = qlReturn[1])
  
@app.route('/Verification')
def Verification():
   return render_template('verification.html', email = "ERROR")

@app.route('/VerificationRequest/', methods = ['GET','POST'])
def VerificationRequest():
    dv = "000"
    return render_template("secret_page.html",name = username)

  
if __name__ == '__main__':
  app.run(debug=True)
from flask import Flask
from flask_mail import Mail, Message
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)

@app.route('/')
def test():
    try:
        msg = Message('Test Email',
                    recipients=['您的测试接收邮箱'])
        msg.body = "This is a test email."
        mail.send(msg)
        return 'Email sent successfully!'
    except Exception as e:
        return f'Error: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True) 
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailVerification:
    def __init__(self):
        self.verification_code = 0

    def send_verification_code(self, email):
        # Generate a 6-digit verification code
        self.verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])

        receiver_email =  email
        # Email configuration
        sender_email = 'youremail@gmail.com'
        sender_password = 'yourpassword'

        # Create a multipart message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = 'Verification Code'

        # Add message body
        body = f'Your verification code is: {self.verification_code}'
        message.attach(MIMEText(body, 'plain'))

        # Send email
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print()
            print("\033[92m{}\033[0m".format('Verification code sent successfully!'))
            server.quit()
        except Exception as e:
            print(f"Error: {str(e)}")

    # Usage example:
# email_address = 'spamss906@gmail.com'
# send_verification_code(email_address)

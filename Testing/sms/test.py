import smtplib, ssl
from email.message import EmailMessage
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import imghdr

def send(content, to, subject):
    # message = EmailMessage()
    message = MIMEMultipart()
    message.attach(MIMEText(content, "plain"))
    # message.set_content(content)
    message['to'] = to
    message['subject'] = subject
    message['doorbotalerts@gmail.com']

    # message.add_attachment("/Users/ryanhebert/Downloads/blue.jpg")
    filename = "/Users/ryanhebert/Downloads/blue.jpg"

    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        #part = MIMEBase("application", "octet-stream")
        #part.set_payload(attachment.read())
        image_data = attachment.read()
        image_type = imghdr.what(attachment.name)
        image_name = attachment.name



    # Encode file in ASCII characters to send by email
    # encoders.encode_base64(part)
    #
    # # Add header as key/value pair to attachment part
    # part.add_header(
    #     "Content-Disposition",
    #     f"attachment; filename= {filename}",
    # )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login("doorbotalerts@gmail.com", "fzeickjavxdxwnrc")
        server.sendmail("doorbotalerts@gmail.com", "rrheb31@gmail.com", text)
    #
    # user = "doorbotalerts@gmail.com"
    # password = "fzeickjavxdxwnrc"
    #
    # # server = smtplib.SMTP("smtp.gmail.com", 587)
    # server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    # server.ehlo()
    # # server.starttls()
    # server.login(user, password)
    # server.send_message(message, "doorbotalerts@gmail.com")
    #
    # server.quit()


send("You have new activity at your doorbell.", "rhebert@muhlenberg.edu", "DoorBot Alerts")
# send("You have new activity at your doorbell.", "9732703058@txt.att.net", "DoorBot Alerts")
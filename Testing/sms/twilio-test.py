from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
# from flask_ngrok import run_with_ngrok
from twilio import twiml

sid = "AC87f189511d21d6480cdc84350cbbbb84"
auth = "edaa37009bb656376a02bb33a2ac6a4c"
# body = "This is a test alert from DoorBot Alert System"
twilio_number = "+112393091468"
to_number = "+19732703058"
# to_number = "+12014682558"

def sendMessage(body):
    client = Client(sid, auth)
    message = client.messages.create(body=body, from_=twilio_number, to=to_number)
    print(message.sid)


app = Flask(__name__)
@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    body = request.values.get('Body', None)

    response = MessagingResponse()
    message = Message()

    if body == 'Hello':
        text = "Hi!"
    else:
        text = "Hello!"

    message.body(text)
    response.append(message)

    ## write the response to DB

    return str(response), 200, {'Content-Type': 'text/xml'}

## https://www.twilio.com/docs/sms/tutorials/how-to-receive-and-reply-python#custom-responses-to-incoming-sms-messages


sendMessage("this is a test")

if __name__ == "__main__":
    app.run(port=5002)





    # twim.writeHead(200, {
    #     'Content-Type': 'text/xml'
    # })
####################### Twilio-Server ####################### 
# Flask applicaton to run on localhost for HTTP reception
# of Twilio texts

from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
from twilio import twiml
import re
import DatabaseHelper


## Twilio auth and phone number variables
sid = "AC87f189511d21d6480cdc84350cbbbb84"
auth = "edaa37009bb656376a02bb33a2ac6a4c"
twilio_number = "+112393091468"
to_number = "+19732703058"

app = Flask(__name__)
# declare flask app
database = DatabaseHelper.db("root", "localhost", "doorbot")
print(database.cursor.connection)

def sendMessageWithURL(body, url):
    """ Sends a text message using Twilio that contains media
        
        Parameters:
        body (string): body of text to be sent
        url (string): imgur url containing image

    """
    client = Client(sid, auth)
    message = client.messages.create(body=body, from_=twilio_number, to=to_number, media_url=url)
    # create message with body, phone numbers and media 
    print(message.sid)


def sendMessage(body):
     """ Sends a text message using Twilio
        
        Parameters:
        body (string): body of text to be sent

    """
    print(body)
    client = Client(sid, auth)
    message = client.messages.create(body=body, from_=twilio_number, to=to_number)
    # create message with body, phone numbers and media 
    print(message.sid)


@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """ Receives incoming text message as GET or POST request from Twilio API. Writes
        to database the message received. Called when localhost:5002/sms is hit
        
        Returns:
        empty string because return is necessary but we don't need to send anything back
    """
    
     #database = DatabaseHelper.db("root", "localhost", "doorbot")
    
    body = request.values.get('Body', None)
    # get body of message received
    
    code = "---" 
    database.cursor.execute(f"INSERT INTO messageIn (code, message) VALUES ('{code}', '{body}');")
    database.connection.commit() 
    # write to database the message received
    
    #database.write("in", "---", body)
    # tempDB.connection.close()

    return ""
    #return str(response), 200, {'Content-Type': 'text/xml'}


@app.route("/out", methods=['POST'])
def retrieveNewMessage():
    """ Picks up new message from database at the maxId of messageOut table. Calls
        twilio send message methods. Called when localhost:5002/out is hit
        
        Returns:
        empty string because return is necessary but we don't need to send anything back
    """
    newDB = DatabaseHelper.db("root", "localhost", "doorbot")
    
    newDB.cursor.execute("select max(id) from messageOut;")
    vals = newDB.cursor.fetchall()
    maxId = vals[0][0]
    
    #gets latest entry in out table
    entry = newDB.read("out", maxId)[0]
    message = entry[2]
    print(message)
    
    reg = re.search(r"(https://.*)", message, re.DOTALL) #find url
    if reg is not None:
        url = reg.group(0)
        message.replace(url, "")
        sendMessageWithURL(message, url)
    else:    
        sendMessage(message)
    
    newDB.connection.close()

    return ""
#sendMessage("this is a test")

if __name__ == "__main__":
    app.run(port=5002)
    database.connection.close()



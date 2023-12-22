#Daniel Kantor, Ryan Hebert, Patrick Kim
#DoorBot - SMSHelper file
#File that sets up the interaction/conversation flow between the user and the bot based on the responses of the user
#then will write the responses to the database and ping the server to look for these database changes

from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
# from flask_ngrok import run_with_ngrok
from twilio import twiml
import requests, cv2, os, pyimgur
import DatabaseHelper, LoadingHelper
from Classes import Person


_sid = "AC87f189511d21d6480cdc84350cbbbb84"
_auth = "edaa37009bb656376a02bb33a2ac6a4c"
_twilioNumber = "+112393091468"
_imgur = pyimgur.Imgur("4ec7aa3c636204e")

"""
    Method that gets the frame, temporarily saves it to a directory uploads it to imgur, deletes the image and returns the imgur link

    Parameters:
    _currentFrame: the frame image to upload imgur

    Returns:
    image.link: the link to the image that was uploaded
    """ 
def createImgurURL(_currentFrame):
    cv2.imwrite('temp.png', _currentFrame) #save the image locally
    image = _imgur.upload_image("temp.png", title="DoorBot")
    os.remove("temp.png")
    
    return image.link

"""
    Method that pings the server when something new is written to the database so the server knows to check

    Parameters:
    None

    Returns:
    None
    """   
def sendRequest():
    r = requests.post("http://localhost:5002/out")
    

def sendTextWithBody(body, _database):
    _database.write("out", "---", body)
    sendRequest()
    
"""
    Method that will get the information of the current person being detected and store the text response in the database
    and then call the method that pings the server

    Parameters:
    guess: the person being detected
    _statusCode: code of if the person being detected is known or not
    _database: instance of the database connection
    _currentFrame: frame of the person being detected

    Returns:
    None
    """ 
def sendText(guess, _statusCode, _database, _currentFrame):
    if _statusCode == 101:
        text = "There has been motion at your front door. I believe it is " + guess + ". Would you like to let them in? "
    elif _statusCode == 102:
        text = "There has been motion at your front door. I do not recognize who it is. Do you? "
    elif _statusCode == 104:
        text = "An unauthorized user has been detected at your front door. Would you like me to call the police? "
    
    text += createImgurURL(_currentFrame) #get the url of the image of the person and add it to the text saved to the database
    #_database.write("out", str(_statusCode), text)
    code = str(_statusCode)
    _database.cursor.execute(f"INSERT INTO messageOut (code, message) VALUES ('{code}', '{text}');")
    _database.connection.commit()
    sendRequest() #ping the server
    

"""
    Method that passes the message details to the databaseHelper file and writes it to the database and
    then calls the method that pings the server

    Parameters:
    text: the text to write 
    _database: instance of DatabaseHelper
    _statusCode: current status of where the conversation is

    Returns:
    None
    """    
def sendResponse(text, _database, _statusCode):
    _database.write("out", str(_statusCode), text)
    sendRequest()
    
    
def sendStartText(_database):
    _database.write("out", "000", "DoorBot is now running...")
    sendRequest()

"""
    Method that sets up the sets up what the response of the bot will be depending on message from the user
    Sets up the conversation flow of the interaction

    Parameters:
    _lastinId: the id of the most recent entry in the database
    _database: instance of DatabaseHelper
    _statusCode: current status of where the conversation is
    _currentFrame: the current frame being seen
    _guess: the person who is currently being detected
    _lastEncoding: the last person that was seen in the frame
    _people: list of people that are stored


    Returns:
    _database: instance of DatabaseHelper
    _lastInId + 1
    _statusCode: current status of where the conversation is
    lastProcessedName: name of last person seen
    _people: list of people stored
    """ 
def getNewMessage(_lastInId, _database, _statusCode, _currentFrame, guess, _lastEncoding, _people, video):
    _database.connection.close()
    _database = DatabaseHelper.db("root", "localhost", "doorbot") #Reboot database connection
    
    record = _database.readRecord(_lastInId + 1)  #check if new records in database
    
    if record[0] is None or record[0] == None:
        ## No new records in db since last message
        return _database, _lastInId, _statusCode, "", _people  
    
    body = record[1]
    ## contents of text message picked up from database
    
    
    #If statements settings up the conversation flow and possible responses from the user to interact with the bot  

    if _statusCode == 101:
        if "yes" in body or "Yes" in body or "Y" in body or "y" in body:
            text = "Okay, I have let them in."
            _statusCode = 000
        elif "no" in body or "No" in body or "n" in body or "n" in body:
            text = "Okay, I will not let them in."
            _statusCode = 000
        elif "Send a picture" in body or "send a picture" in body or "send picture" in body or "Send picture" in body:
            _statusCode = 103
            url = createImgurURL(_currentFrame) #get picture url 
            text = "Here is a picture. "
            text += url
            
    elif _statusCode == 102:
        if "yes" in body or "Yes" in body or "Y" in body or "y" in body:
            text = "Please respond with the name you would like to save this user as."
            _statusCode = 201
        elif "no" in body or "No" in body or "n" in body or "n" in body:
            text = "Okay, I will not let them in."
            _statusCode = 000
        elif "Send a picture" in body or "send a picture" in body or "send picture" in body or "Send picture" in body:
            _statusCode = 103
            url = createImgurURL(_currentFrame)
            text = "Here is a picture. Do you recognize this person? "
            text += url
            
    elif _statusCode == 103:
        if "Let them in" in body or "let them in" in body:
            text = "Okay, I have let them in."
            _statusCode = 000
        elif "do not let them in" in body or "Do not let them in" in body or "do not let them in" in body or "Do not let them in" in body:
            text = "Okay, I will not let them in."
            _statusCode = 000
        elif "yes" in body or "Yes" in body or "Y" in body or "y" in body:
            text = "Okay, what is their name? I will save this user so I recognize them next time."
            _statusCode = 201
        elif "no" in body or "No" in body or "n" in body or "n" in body:
            text = "Okay, I will not let them in? Their face has been saved in case they come back."
            _statusCode = 000
    elif _statusCode == 104:
        if "yes" in body or "Yes" in body or "Y" in body or "y" in body:
            text = "Okay, I have notified the police."
            _statusCode = 000
        elif "no" in body or "No" in body or "n" in body or "n" in body:
            text = "Okay, if you change your mind you can always respond with 911! to alert the police."
            _statusCode = 000    
    elif _statusCode == 201:
        text = "Okay, I have saved " + body + " to the database" #add new person to list of encodings and update the json file storing them
        _people.append(Person(105, body, 1, _lastEncoding))
        LoadingHelper.updateDB(_people)
        _statusCode = 000
    elif _statusCode == 911:
        if "yes" in body or "Yes" in body or "Y" in body or "y" in body:
            text = "Okay, I have notified the police."
            _statusCode = 000
        elif "no" in body or "No" in body or "n" in body or "n" in body:
            text = "Okay, if you change your mind you can always respond with 911! to alert the police."
            _statusCode = 000

    if "thank you" in body or "thanks" in body or "Thank you" in body or "Thanks" in body:
        text += "\nIt is my pleasure to serve you."
        _statusCode = 000
    elif "911!" in body:
        _statusCode = 911
        text = "Are you sure you want to alert the police?"
    elif "Send picture" in body or "send picture" in body or "status" in body or "Status" in body or "picture" in body:
        text = "Here is the current frame" + createImgurURL(_currentFrame)

    if _statusCode == 000:
        if guess == "Unknown": #if the person was previously unknown and was added to the database, change the last person seen to the person added
            lastProcessedName = LoadingHelper.getNames(_people)[-1]
        else:
            lastProcessedName = guess
    
    else:
        lastProcessedName = "N/A"
    
    if text is None:
        text = "I am DoorBot"
        
    sendResponse(text, _database, _statusCode) #write the message to the database

    
    return _database, _lastInId + 1, _statusCode, lastProcessedName, _people 


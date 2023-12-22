#Daniel Kantor, Ryan Hebert, Patrick Kim
#DoorBot - Bot file
#File that opens the camera and calls methods to figure out if person is in frame and if there is, find out who it is and then start
#the conversation between the bot and the user

import json
import random
import time
import cv2  
import os, re
import face_recognition
import numpy as np
import asyncio
#import LogoHelper
from Classes import Person
import LoadingHelper
import threading
import DatabaseHelper
import FacialRecHelper
import SMSHelper
import requests
import timeit
import Features

_people = []
_lastEncoding = []
_previousPrediction = None
_lastInId = 0
_locked = True
_statusCode = 000
_currentFrame = np.empty(0)
_lastProcessedName = ""
_database = DatabaseHelper.db("root", "localhost", "doorbot") #open connection to databaes


def tryFindLogo(frame):
    logo_img = cv2.imread('amazon.jpeg') #get pic of amazon logo
    train_features = Features.getFeatures(logo_img)

    region = Features.detectFeatures(frame, train_features)
    
    if region is not None:
        return True
    return False        
        

"""
    Method that opens the camera, calls the method to find out if there is someone in frame and based on the information returned
    from that, send a text, idle and do nothing or continue the conversation if it has already started

    Parameters:
    None

    Returns:
    None
    """ 
def main():
    global _locked
    global _people
    global _statusCode
    global _currentFrame
    global _lastProcessedName
    global _database
    global _lastInId
    
    video = cv2.VideoCapture(0) #open the camera
    process_this_frame = True #boolean to process every other frame to save some load on the pi

    _people = LoadingHelper.loadPeople() #get the list of people saved
    
    names = LoadingHelper.getNames(_people) #get the names associated with people
    
    previousPrediction = "" 

    guess = ""
    
    while True: #infinite loop
        if _statusCode == 000: #beginning of interaction with a person
            #idle
            
            if process_this_frame: #get every other frame
                ret, frame = video.read()
                _currentFrame = frame
                
                motionDetected, _lastEncoding = FacialRecHelper.idle(frame)  #check if someone in frame
                if motionDetected is True:
                    #SMSHelper.sendTextWithBody("There has been motion at your front door...", _database)
                    
                    #logo = tryFindLogo(frame)
                    #if logo:
                        #_statusCode = 301
                    
                    #get the person who is in frame
                    guess, _lastEncoding, previousPrediction  = FacialRecHelper.facePrediction(frame, names, previousPrediction, _people)
                
                    if guess == _lastProcessedName:
                        for i in range(15): # stall a few seconds
                            ret, frame = video.read()
                        continue
                    if guess == "first":
                        # Double checking each prediction with more than one frame. "First" means the first time a face was recognized. If
                        # same frame results in same prediction, then we consider them predicted. 
                        continue
                    if guess == "Unknown":
                        _statusCode = 102
                    elif guess == "Unauthorized":
                        # Predicted somebody with unauthorized access 
                        _statusCode = 104
                    else:
                        # Predicted somebody in the database of names 
                        _statusCode = 101
                
                    SMSHelper.sendText(guess, _statusCode, _database, _currentFrame) #send a text based on what was found in the frame
        else:   
            #conversation has started, continue the conversation and don't look for new people
            _database, _lastInId, _statusCode, _lastProcessedName, _people = SMSHelper.getNewMessage(_lastInId, _database, _statusCode, _currentFrame, guess, _lastEncoding, _people)
        #process every other frame
        process_this_frame = not process_this_frame

_lastInId = _database.getLastId()
# SMSHelper.sendStartText(_database)
main()
_database.connection.close()
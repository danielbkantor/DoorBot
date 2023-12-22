####################### FacialRecHelper ####################### 
# Method file for all functions related to face_recognition library
# and logic for recognizng and guessing faces. 


import face_recognition
import cv2
import LoadingHelper
import numpy as np
import DatabaseHelper


def idle(frame):
    """ Method to idle or read each frame until a face is seen. Returns flag
        of whether or not a face was picked up as well as the encodings.
        
        Parameters:
        frame (OpenCV frame): frame object that was read from cv2 Object

        Returns:
        bool:True if face seen, False if not
        list<float>: face encoding list of float valus (None if face not seen)
    """
    
    faceLocations = face_recognition.face_locations(frame)
    faceEncodings = face_recognition.face_encodings(frame, faceLocations)
    
    if faceEncodings == []: # if no faces found
        return False, None
    else:
        lastEncoding = list(faceEncodings[0])
        return (True, lastEncoding)


def getBestMatch(names, faceEncoding, people):
    """ Finds which name in list of people matches current faceEncoding best
        
        Parameters:
        names (list<string>): list of all names of people in the database
        faceEncoding (nparray): numpy array of encodings of face recognized by camera
        people (list<Person>): list of people as Person objects from json file

        Returns:
        name (string):Predicted name of face ("Unknown" if applicable, "first" if to double checked)
        list<float>: face encoding list of float valus for last recognized face to be stored later
    """
    faces = LoadingHelper.getFacesDict(people)
    # See if the face is a match for the known faces

    matches = face_recognition.compare_faces(list(faces.values()), faceEncoding)
    # list of clsoe matches in initial check
    
    name = "Unknown"
    lastEncoding = []
    faceDistances = face_recognition.face_distance(list(faces.values()), faceEncoding)
    bestMatchIndex = int(np.argmin(faceDistances))
    #distance formula check for the closest matching face
    try:
        if matches[bestMatchIndex]:
            name = names[bestMatchIndex]
        lastEncoding = list(faceEncoding)
    except IndexError:
        print("Please restart your DoorBot to save changes to the database.")
        # if best match is not in database, restart to update
        people = LoadingHelper.loadPeople()
        names = LoadingHelper.getNames(people)
        getBestMatch(names, faceEncoding, people)
        
    return name, lastEncoding


def predict(names, frame, people):
    """ Given a frame and names, predict which is closest match
        
        Parameters:
        frame (OpenCV frame): frame object that was read from cv2 Object
        names (list<string>): list of all names of people in the database
        people (list<Person>): list of people as Person objects from json file

        Returns:
        name (string):Predicted name of face ("Unknown" if applicable, "first" if to double checked)
        list<float>: face encoding list of float valus for last recognized face to be stored later
    """
    faceLocations = face_recognition.face_locations(frame)
    faceEncodings = face_recognition.face_encodings(frame, faceLocations)
    name = "Unknown"
    lastEncoding = []
    
    for faceEncoding in faceEncodings:
        name, lastEncoding = getBestMatch(names, faceEncoding, people)
    
    if name == "Unknown" and len(faceEncodings) > 0:
        lastEncoding = list(faceEncodings[0])
    
    return name, lastEncoding


def facePrediction(frame, names, _previousPrediction, people):
    """ Begin face prediction process with frame from cv2 camera 
        
        Parameters:
        frame (OpenCV frame): frame object that was read from cv2 Object
        names (list<string>): list of all names of people in the database
        _previousPrediction (string): name of last predicted face
        people (list<Person>): list of people as Person objects from json file

        Returns:
        name (string):Predicted name of face ("Unknown" if applicable, "first" if to double checked)
        list<float>: face encoding list of float valus for last recognized face to be stored later
        prediction (string): string of prediction to hold value in case of double check or unknown
    """
    print("Predicting...")

    smallFrame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    #smaller frame for portability

    rgbSmallFrame = smallFrame[:, :, ::-1]
    # change from bgr to rgb 
     
    prediction, lastEncoding = predict(names, rgbSmallFrame, people)
    if prediction == _previousPrediction:
        ## if prediction is the same as last prediction, consider it valid
        print("Detected ", prediction)
        
        return prediction, lastEncoding, prediction 

    return "first", lastEncoding, prediction
    ## return "first" the first time a name is guessed to force a double-check
    

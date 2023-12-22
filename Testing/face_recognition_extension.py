import json
from re import L
import face_recognition
import cv2
import numpy as np
import os
import glob
import time

# import tensorflow as tf
# from tensorflow.keras.models import load_model


def updateDB(faces):
    with open("encodings.json", "w") as outfile:
        json.dump(faces, outfile, indent = 4)

def tryGetNewFaces(path):
    list_of_files = [f for f in glob.glob(path+'*.jpg')]
    number_files = len(list_of_files)
    faces = {}
    if number_files > 0:
        
        names = list_of_files.copy()
        names = [n.rsplit( ".", 1 )[0] for n in names]

        for i in range(number_files):
            try:
                globals()['image_{}'.format(i)] = face_recognition.load_image_file(list_of_files[i])
                globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]
                
                faces[names[i].replace("known_people/", "")] = list(globals()['image_encoding_{}'.format(i)])
                
                names[i] = names[i].replace("known_people/", "")  
                # known_face_names.append(names[i])
                print('Added face', names[i].replace("known_people/", ""), "to database")
            except IndexError: 
                print('Unable to detect face in', names[i].replace("known_people/", ""))
                pass
           
        
    return faces

def getKnownFaces():
    try:
        with open('encodings.json', 'r') as js:
            data = json.load(js)
            return data
    except: 
        open('encodings.json', 'w')
        return {}

def numpify(faces):
    return faces


    

    
### TODO: Specify this for multiple cam use case
video_capture = cv2.VideoCapture(0)

known_face_names = []
dirname = os.path.dirname(__file__)
path = os.path.join(dirname, 'known_people/')

newFaces = tryGetNewFaces(path)
faces = getKnownFaces()

faces.update(newFaces)
updateDB(faces)
faces = numpify(faces)

names = list(faces.keys())
names = [x.replace("known_people/", "") for x in names]

face_locations = []
face_encodings = []
process_this_frame = True

# mpHands = mp.solutions.hands
# hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
# mpDraw = mp.solutions.drawing_utils

# model = load_model('mp_hand_gesture')
import Features
def tryGetLogo(frame):
    logo_img = cv2.imread('amazon.jpeg') #get pic of amazon logo
    train_features = Features.getFeatures(logo_img)
    
    region = Features.detectFeatures(frame, train_features)
    
    if region is not None:
        return True
    return False  


f = open('gesture.names', 'r')
classNames = f.read().split('\n')
f.close()

face = True
count = 0

while True:
    ret, frame = video_capture.read()
    x, y, c = frame.shape

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get hand landmark prediction
    # result = hands.process(framergb)
    className = ''
    if not face:
    # post process the result
        # if result.multi_hand_landmarks:
        #     landmarks = []
        #     for handslms in result.multi_hand_landmarks:
        #         for lm in handslms.landmark:
        #             # print(id, lm)
        #             lmx = int(lm.x * x)
        #             lmy = int(lm.y * y)

        #             landmarks.append([lmx, lmy])

        #         # Drawing landmarks on frames
        #         mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

        #         # Predict gesture
        #         prediction = model.predict([landmarks])
        #         # print(prediction)
        #         classID = np.argmax(prediction)
        #         className = classNames[classID]

        # show the prediction on the frame
        cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

    else:
        # Convert the image from BGR color to RGB color 
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            
            print(tryGetLogo(frame))
            
            
            count += 1
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            
            if len(face_encodings) > 0:
                print("face")
           
            # if count == 5:
            #     screenshot = list(face_encodings[0])
               


            face_names = []
            for face_encoding in face_encodings:
                
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(list(faces.values()), face_encoding)
                name = "Unknown"

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(list(faces.values()), face_encoding)
                best_match_index = int(np.argmin(face_distances))
                if matches[best_match_index]:
                    name = names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # print(top, right, bottom, left)
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

for file in [f for f in glob.glob(path+'*.jpg')]:
    os.remove(file)

# faces[str(input("Dectected new face. Enter name: "))] = screenshot
# updateDB(faces)
video_capture.release()
cv2.destroyAllWindows()
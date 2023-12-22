##### Helper file for loading data to and from json files.

import json
import cv2
import os
from Classes import Person, AccessLevel
import glob
import face_recognition
import LoadingHelper


def getNextId():
    return 10002

def obj_dict(obj):
    return obj.__dict__


def getJSString(faces):

    """Creates and returns dictionary of lists, each list refering to a person in the database

    Parameters:
    faces (list): list of people used to create dictionary

    Returns:
    dict: biggerDict
    """
    i = 1
    biggerDict = {}
    for face in faces:
        smallerDict = {}
        smallerDict["Id"] = face.id[0]
        smallerDict["Name"] = face.name
        smallerDict["Access"] = face.access[0]
        smallerDict["Encodings"] = face.encoding
        biggerDict[i] = smallerDict
        i = i + 1

    print(biggerDict)
    return biggerDict


def updateDB(faces):

    """Updates JSON file with new face
    
    Parameters:
    faces (list): list of faces with new face appended to it

    Returns:
    None
    """
    js = getJSString(faces)
    # with open("encodings.json", "w") as outfile:
    #     outfile.write(getJSString(faces))
    with open("encodings.json", "w") as of:
        json.dump(js, of, indent=4)


def getNames(people):

    """Returns a list of names of all people in the JSON file
    
    Parameters:
    people (list): list of tuples, each tuple being a person

    Returns:
    list: out
    """
    out = []
    for p in people:
        out.append(p.name)
    return out


def getNewPeople(path):

    """Gets List of new People from directory

    Parameters:

    path (str): directory path to jgp files of new person to add

    Returns:

    list: faces 
    """

    id = getNextId()
    list_of_files = [f for f in glob.glob(path + '*.jpg')]
    number_files = len(list_of_files)
    faces = []
    if number_files > 0:
        names = list_of_files.copy()
        names = [n.rsplit(".", 1)[0] for n in names]
        for i in range(number_files):
            getFaceFromFile(faces, i, id, list_of_files, names)
    return faces


def getFaceFromFile(faces, i, id, list_of_files, names):

    """Gets face encodings from a jpg file and add person to JSON file

    Parameters:
    faces (list): list of faces gets appended with new encoding
    i (int): index number for list list_of_files/names
    list_of_files (list): list of jpg files
    names (list): list of names of known people

    Returns:
    None
    """
    try:
        globals()['image_{}'.format(i)] = face_recognition.load_image_file(list_of_files[i])
        globals()['image_encoding_{}'.format(i)] = \
            face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]

        names[i] = names[i].replace("known_people/", "")
        faces.append(Person(id, names[i].replace("known_people/", ""), AccessLevel.GUEST,
                            list(globals()['image_encoding_{}'.format(i)])))
        print('Added face', names[i].replace("known_people/", ""), "to database")
    except IndexError:
        print('Unable to detect face in', names[i].replace("known_people/", ""))
        pass


def getKnownPeople():

    """Gets List of People from encodings database

    Parameters:
    None

    Returns:
    list: people
    """
    ####
    # 
    ####
    people = []
    with open('encodings.json', 'r') as js:
        data = json.load(js)
    for k, v in data.items():
        people.append(Person(int(k), str(v["Name"]), v["Access"], v["Encodings"]))
    return people


def getFacesDict(people):

    """Creates and returns dictionary of known people to be used for face comparison

    Parameters:
    people(list): list of people used to create dictionary

    Returns:
    dict: out
    
    """
    
    out = {}
    for p in people:
        out[p.name] = p.encoding
    return out


def loadPeople():

    """Creates and returns a list of every person from the JSON file

    Parameters:
    None

    Returns:
    list: people
    
    """

    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, 'known_people/')
    people = getKnownPeople()
    newPeople = getNewPeople(path)
    if len(newPeople) > 0:
        people.append(newPeople)
    
    return people

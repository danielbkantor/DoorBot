#### classes used in our project (Pat)

from enum import Enum
from os import getuid


class AccessLevel(Enum):
    ADMIN = 1
    ALLOWED = 2
    GUEST = 3
    RESTRICTED = 4


class Person:
    def __init__(self, id, name, AccessLevel, encoding):
        
        """ initializes person and attributes

        Parameters:
        self (Person): referring to person
        id (int): ID number associated with person
        name (str): Name of person
        AccessLevel (int): Given 1 out of 4 different access levels
        encoding (): Facial encoding of person for facial recognition

        Returns:
        None
        
        """
        self.id = id,
        self.name = name
        self.access = AccessLevel,
        self.encoding = encoding

    def changeName(self, name):

        """Changes name of person
        
        Parameters:
        self (Person): referring to person
        name (str): New name of person

        Returns:
        None
        """
        self.name = name

    def changeAccess(self, AccessLevel):
        
        """Changes access of person
        
        Parameters:
        self (Person): referring to person
        AccessLevel (int): New access level of person

        Returns:
        None
        """
        self.access = AccessLevel


class Object:
    def __init__(self, name, encoding):
        self.name = name
        self.id = getuid
        self.encoding = encoding

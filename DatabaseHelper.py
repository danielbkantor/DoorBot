#Daniel Kantor, Ryan Hebert, Patrick Kim
#DoorBot - DatabaseHelper file
#File used to set up the connection to our database and includes methods that allow reading and writing to the database

import mariadb
import sys

class db:
    cursor = 1
    connection = 1
    
    def __init__(self, user, host, database):
        #set up the connection with the database
        self.connection = mariadb.connect(
            user=user,
            password="georgebenjamin",
            host=host,
            # port=3306,
            database=database
        )
    
        self.cursor = self.connection.cursor()
        
        
    """
    Write method that includes a query for info being written to either of our two tables

    Parameters:
    table: which table to write to
    code1: the status code of the message
    message1: the text of the message

    Returns:
    None
    """ 
    def write(self, table, code1, message1):
        # triggered by flask app incoming_sms()
        if table == "in":
            self.cursor.execute(f"INSERT INTO messageIn (code, message) VALUES ('{code1}', '{message1}');")
        # triggered by sending a text
        elif table == "out":
            self.cursor.execute(f"INSERT INTO messageOut (code, message) VALUES ('{code1}', '{message1}');")
    
        self.connection.commit()
        

    """
    Read method that includes a query for info being read from either of our two tables

    Parameters:
    table: which table to read from
    maxId - read the message that has the max id number

    Returns:
    vals - the results of the query
    """     
    def read(self, table, maxId): 
        if table == "in":
            self.cursor.execute(f"SELECT max(id), message from messageIn where id >= {maxId};") 
        elif table == "out":
            self.cursor.execute(f"SELECT max(id), code, message from messageOut where id = {maxId} ;")
            
        vals = self.cursor.fetchall()
        return vals
            
    """
    Method that gets the message associated with a specific ID

    Parameters:
    nextId - the id number to get the message associated with it

    Returns:
    vals - the results of the query
    """         
    def readRecord(self, nextId):
        self.cursor.execute(f"SELECT max(id), message from messageIn where id = {nextId} ;")
        vals = self.cursor.fetchone()
        
        return vals
            
    """
    Method that gets the maxId from messageIn

    Parameters:
    None

    Returns:
    The result of the query (the max id)
    """    
    def getLastId(self):
        self.cursor.execute(f"SELECT max(id) from messageIn;")
        return self.cursor.fetchone()[0]
    
        

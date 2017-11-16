'''
Created on 15.11.2017

@author: adrian
'''
import os.path
import configparser

class Credentials(object):
    '''
    classdocs
    '''
    username = ""
    password = ""
     

    def __init__(self, username, password):
        '''
        Constructor
        '''
        self.username = username
        self.password = password
          
     
    def LoadFromFile(self, file):
        
        if not os.path.isfile(file):
            print('ATENTIE: Nu se pot citi utilizatorul si parola din fisier, fisierul nu exista: ' + file)
        else:     
            
            config = configparser.ConfigParser()
            config.read(file)
       
            self.username = config.get('Download', 'username')
            self.password = config.get('Download', 'password')
    

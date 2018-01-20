'''
Created on 15.11.2017

@author: Adrain Mos
'''
import os.path
import configparser

class Credentials(object):

    def __init__(self):
        self.username = ""
        self.password = ""
     
    def LoadFromFile(self, file):
        
        if not os.path.isfile(file):
            print('ATENTIE: Nu se pot citi utilizatorul si parola din fisier, fisierul nu exista: ' + file)
        else:     
            
            config = configparser.ConfigParser()
            config.read(file)
       
            self.username = config.get('Download', 'username')
            self.password = config.get('Download', 'password')
    

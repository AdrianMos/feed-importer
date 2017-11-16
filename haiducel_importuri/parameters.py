'''
Created on 15.11.2017

@author: adrian
'''
import os.path
import configparser

class Parameters(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''       
        self.downloadUrl = ''   
        self.delimiter = '|'
        self.quotechar = '"' 
        self.categoryMappingFile = ''
                 
     
    def LoadFromFile(self, file):
        ''' 
        Reads configuration parameters from the configuration file
        '''
        
        if not os.path.isfile(file):
            print('ATENTIE: Fisierul de configurare nu exista: ' + file)
        else:        
            config = configparser.ConfigParser()
            config.read(file)
            
            self.downloadUrl = config.get('Download', 'url')   
            self.delimiter = config.get('Import', 'delimiter') 
            self.quotechar = config.get('Import', 'quotechar') 
            self.categoryMappingFile = config.get('Import', 'categoryMappingFile')
        print("categ mapping: " + self.categoryMappingFile)

        
        
    def ReadMapFromFile(self, file):
        
        map = {}
        
        if not os.path.isfile(file):
            print('ATENTIE: Fisierul de sortare articole nu exista: ' + file)
        else:  
            config = configparser.RawConfigParser(allow_no_value=True)
            config.read(file)    
            sections = config.sections()
                        
            #create mapping dictionary
            for section in sections:
                #print(" section: " + str(section))
                for key in config[section]: 
                  #print("   ->key: " + key)
                  strippedKey = "".join(key.split())
                  map[strippedKey] = section
        
        return map
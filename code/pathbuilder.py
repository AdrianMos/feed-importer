'''
Created on 05.05.2014

@author: Adrian Mos
'''
import os.path
import time

class PathBuilder(object):
    '''
    classdocs
    '''
    allImagesFolder = os.path.join("data", "_ imagini noi", "mari neprocesate")
    mainImagesFolder = os.path.join("data", "_ imagini noi", "mici neprocesate")
    feedFileNamePath = ""
    configFile = ""  
    credentialsFile = ""
    

    def __init__(self, code):
        '''
        Constructor
        ''' 
        self.feedFileNamePath = os.path.join("data", code, "feed" + code + ".csv")
        self.configFile = os.path.join(os.getcwd(), "config", "config" + code + ".ini")
        self.credentialsFile = os.path.join(os.getcwd(), "config", "credentials", "credentials" + code + ".ini")
    

    @staticmethod
    def getLogPath(code):
        return os.path.join('data', code, 'erori ' + code + '.log')


    @staticmethod
    def getOutputPath(name, code):
        '''
        Returns the file path for converted output feeds.
        '''
        return ('data/'
                + code
                + '/out/' 
                + code 
                + ' ' + name + ' ' 
                + time.strftime('%Y-%m-%d')
                + '.csv')
    
    @staticmethod
    def getOutputFolderPath(code):
        return os.path.join(os.getcwd(), "data", code, "out");
    
    
    


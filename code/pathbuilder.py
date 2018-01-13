'''
Created on 05.05.2014

@author: Adrian Mos
'''
import os.path

class PathBuilder(object):
    '''
    classdocs
    '''
    allImagesFolder = ""
    mainImagesFolder = ""
    feedFileNamePath = ""
    configFile = ""  
    credentialsFile = ""
    

    def __init__(self, code):
        '''
        Constructor
        '''
        print("PathBuilder input code : " + str(code))
        self.allImagesFolder =  os.path.join("data", "_ imagini noi", "mari neprocesate")
        self.mainImagesFolder = os.path.join("data", "_ imagini noi", "mici neprocesate")
        self.feedFileNamePath = os.path.join("data", code, "feed" + code + ".csv")
        self.configFile = os.path.join(os.getcwd(), "config", "config" + code + ".ini")
        self.credentialsFile = os.path.join(os.getcwd(), "config", "credentials", "credentials" + code + ".ini")
    

    @staticmethod
    def getLogPath(code):
        return os.path.join('data', code, 'erori ' + code + '.log')        


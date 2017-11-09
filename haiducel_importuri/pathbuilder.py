'''
Created on 05.05.2014

@author: adrian
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
    

    def __init__(self, code):
        '''
        Constructor
        '''
                
        #self.allImagesFolder = code + "/out/imagini/mari/"
        #self.mainImagesFolder = code + "/out/imagini/_de generat imagini mici/" 
        self.allImagesFolder =  os.path.join("_ imagini noi", "mari neprocesate")
        self.mainImagesFolder = os.path.join("_ imagini noi", "mici neprocesate")
        self.feedFileNamePath = os.path.join(code, "feed" + code + ".csv")
        self.configFile = os.path.join(os.getcwd(), "config", "config" + code + ".ini");


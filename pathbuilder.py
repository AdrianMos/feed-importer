'''
Created on 05.05.2014

@author: adrian
'''

class PathBuilder(object):
    '''
    classdocs
    '''
    allImagesFolder = ""
    mainImagesFolder = ""
    feedFileNamePath = ""
      
    

    def __init__(self, code):
        '''
        Constructor
        '''
                
        #self.allImagesFolder = code + "/out/imagini/mari/"
        #self.mainImagesFolder = code + "/out/imagini/_de generat imagini mici/" 
        self.allImagesFolder = "_ imagini noi\\mari neprocesate\\"
        self.mainImagesFolder = "_ imagini noi\\mici neprocesate\\"
        self.feedFileNamePath = code + "/feed" + code + ".csv"

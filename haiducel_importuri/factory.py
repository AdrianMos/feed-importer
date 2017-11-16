from articles import *
from article import Article

from pathbuilder import PathBuilder
from parameters import Parameters

class Factory(object):
    """Factory for articles objects"""
    
      
    
    def CreateSupplierFeedObject(self, code):
        
        #TODO(ArianMos): include the use of str_to_class()
        #TODO(AdrianMos): decouple from user interface
        # return reduce(getattr, str.split("."), sys.modules[__name__]).
        
        
        paths = PathBuilder(code)
        credentials = Credentials("","")
        credentials.LoadFromFile(paths.configFile)
        parameters = Parameters()
        parameters.LoadFromFile(paths.configFile)
        
        
        mappingFile = os.path.join("config", parameters.categoryMappingFile);
        parameters.categoryMap = parameters.ReadMapFromFile(mappingFile)
        
        
        if code == "NAN":
            newObject = NANArticles(code)    
        elif code == "HDRE":
            newObject = HDREArticles(code)
        elif code == "BEB":
            newObject = BEBArticles(code)
        elif code == "HBBA":
            newObject = BebeBrandsArticles(code)
        elif code == "HMER":
            newObject = BabyShopsArticles(code)
        elif code == "HDEC":
            newObject = KidsDecorArticles(code)
        elif code == "HHUB":
            newObject = HubnersArticles(code)
        else:
            newObject = None
           
        if newObject is not None:
            newObject.credentials = credentials
            newObject.paths = paths
            newObject.parameters = parameters
            
        print("3")
        
        return newObject;
    

    
    
    
    def CreateHaiducelFeedObject(self):
        code = "Haiducel"
        paths = PathBuilder(code)
        newObject = HaiducelArticles(code, False);
        newObject.paths = paths
        
        return newObject
    


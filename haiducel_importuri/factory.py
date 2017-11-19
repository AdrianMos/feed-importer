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
            newObject = NANArticles(code, paths, credentials, parameters)    
        elif code == "HDRE":
            newObject = HDREArticles(code, paths, credentials, parameters)
        elif code == "BEB":
            newObject = BEBArticles(code, paths, credentials, parameters)
        elif code == "HBBA":
            newObject = BebeBrandsArticles(code, paths, credentials, parameters)
        elif code == "HMER":
            newObject = BabyShopsArticles(code, paths, credentials, parameters)
        elif code == "HDEC":
            newObject = KidsDecorArticles(code, paths, credentials, parameters)
        elif code == "HHUB":
            newObject = HubnersArticles(code, paths, credentials, parameters)
        else:
            newObject = None
        
        return newObject;
    

    
    def CreateHaiducelFeedObject(self):
        code = "Haiducel"
        paths = PathBuilder(code)
        newObject = HaiducelArticles(code, paths, None, None);
        
        return newObject
    


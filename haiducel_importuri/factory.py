from articles import *
from article import Article
from suppliers.haiducel import ArticlesHaiducel
from suppliers.nancy import ArticlesNancy
from suppliers.bebex import ArticlesBebex
from suppliers.bebebrands import ArticlesBebeBrands
from suppliers.kidsdecor import ArticlesKidsDecor
from suppliers.babydreams import ArticlesBabyDreams
from suppliers.babyshops import ArticlesBabyShops
from suppliers.hubners import ArticlesHubners

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
        credentials.LoadFromFile(paths.credentialsFile)
        parameters = Parameters()
        parameters.LoadFromFile(paths.configFile)
        
        
        mappingFile = os.path.join("config", parameters.categoryMappingFile);
        parameters.categoryMap = parameters.ReadMapFromFile(mappingFile)
        
        
        if code == "NAN":
            newObject = ArticlesNancy(code, paths, credentials, parameters)    
        elif code == "HDRE":
            newObject = ArticlesBabyDreams(code, paths, credentials, parameters)
        elif code == "BEB":
            newObject = ArticlesBebex(code, paths, credentials, parameters)
        elif code == "HBBA":
            newObject = ArticlesBebeBrands(code, paths, credentials, parameters)
        elif code == "HMER":
            newObject = ArticlesBabyShops(code, paths, credentials, parameters)
        elif code == "HDEC":
            newObject = ArticlesKidsDecor(code, paths, credentials, parameters)
        elif code == "HHUB":
            newObject = ArticlesHubners(code, paths, credentials, parameters)
        else:
            newObject = None
        
        return newObject;
    

    
    def CreateHaiducelFeedObject(self):
        code = "Haiducel"
        paths = PathBuilder(code)
        newObject = ArticlesHaiducel(code, paths, None, None);
        
        return newObject
    


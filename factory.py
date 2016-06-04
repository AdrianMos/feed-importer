from articles import *
from article import Article

class Factory(object):
    """Factory for articles objects"""
    
    def CreateSupplierFeedObject(self, userInput):
        
        #TODO(ArianMos): include the use of str_to_class()
        #TODO(AdrianMos): decouple from user interface
        # return reduce(getattr, str.split("."), sys.modules[__name__]).
        
        if userInput=="2":
            newObject = NANArticles("NAN")    
        elif userInput=="3":
            newObject = HDREArticles("HDRE")
        elif userInput=="4":
            newObject = BEBArticles("BEB")
        elif userInput=="5":
            newObject = BebeBrandsArticles("HBBA")
        elif userInput=="6":
            newObject = BabyShopsArticles("HMER")
        elif userInput=="7":
            newObject = KidsDecorArticles("HDEC")
        elif userInput=="8":
            newObject = HubnersArticles("HHUB")
        else:
            newObject = None
        
        return newObject;
        
    def CreateHaiducelFeedObject(self):
        return HaiducelArticles("Haiducel");
    


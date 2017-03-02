from articles import *
from article import Article

class Factory(object):
    """Factory for articles objects"""

    def __init__(self):
        '''
        Constructor
        '''
        # Get all subclasses of Articles and create the suppliers dictionary
        self.suppliers = {}
        for x in Articles.__subclasses__():
            if x is not HaiducelArticles:
                key = x.friendlyName + ' (' + x.code + ')'
                self.suppliers[key]=[x.__name__, x.code, x.friendlyName]
        
    def GetSuppliersList(self):
        # The suppliers dictionary keys (friendly name + code)
        # are friendly enough to be shown to the user.
        return list(self.suppliers.keys())
    
    
    def CreateSupplierFeedObject(self, supplierKey):
        # Get the class type by name and return an object
        className=self.suppliers[supplierKey][0]
        newObject = getattr(sys.modules[__name__], className)
        return newObject()
        
            
        
    def CreateHaiducelFeedObject(self):
        return HaiducelArticles("Haiducel");
    


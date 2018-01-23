import os.path, sys

from code.suppliers.articles import *
from code.article import Article

from suppliers.haiducel import ArticlesHaiducel
from suppliers.nancy import ArticlesNancy
from suppliers.bebex import ArticlesBebex
from suppliers.bebebrands import ArticlesBebeBrands
from suppliers.kidsdecor import ArticlesKidsDecor
from suppliers.babydreams import ArticlesBabyDreams
from suppliers.babyshops import ArticlesBabyShops
from suppliers.hubners import ArticlesHubners

from code.pathbuilder import PathBuilder
from code.parameters import Parameters
from code.credentials import Credentials
from code.downloader import Downloader
from code.descriptionprocessor import DescriptionProcessor

class Factory(object):
    """Factory for articles objects"""
    
      
    @staticmethod
    def CreateSupplierFeedObject(objectName):
        
        code = Factory.GetSupplierCode(objectName)
        paths = PathBuilder(code)

        credentials = Credentials()
        credentials.LoadFromFile(paths.credentialsFile)

        downloader = Downloader(credentials, paths)
        
        parameters = Parameters()
        parameters.LoadFromFile(paths.configFile)

        descriptionProcessor = DescriptionProcessor()
        
        mappingFile = os.path.join("config", parameters.categoryMappingFile);
        parameters.categoryMap = parameters.ReadMapFromFile(mappingFile)

        
        try:
            #call constructor for supplier object
            #class name generated from objectName
            arguments = '(code, paths, parameters, downloader, descriptionProcessor)'
            newObject = eval(str(objectName)+ arguments)
        except:
            newObject = None
        
        return newObject;
    
 
    @staticmethod
    def CreateFeedObjectForShop():
        code = Factory.GetSupplierCode("ArticlesHaiducel")
        print("code " + str(code))
        paths = PathBuilder(code)
        newObject = ArticlesHaiducel(code, paths, None, None, None);
        
        return newObject

    @staticmethod
    def GetSupplierCode(objectName):       
        code = eval(str(objectName)+'.getSupplierCode()')     
        return code

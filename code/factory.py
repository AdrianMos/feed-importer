
import os.path
import sys


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

class Factory(object):
    """Factory for articles objects"""
    
      
    @staticmethod
    def CreateSupplierFeedObject(objectName):
        
        #TODO: decouple from user interface

        code = Factory.GetCodeForOption(objectName)
        print("code : " + str(code) + ' for option ' + str(objectName))
        paths = PathBuilder(code)
        credentials = Credentials("","")
        credentials.LoadFromFile(paths.credentialsFile)
        
        parameters = Parameters()
        parameters.LoadFromFile(paths.configFile)
        
        mappingFile = os.path.join("config", parameters.categoryMappingFile);
        parameters.categoryMap = parameters.ReadMapFromFile(mappingFile)

        try:
            #call constructor for supplier object
            #class name generated from objectName
            parameters = '(code, paths, credentials, parameters)'
            newObject = eval(str(objectName)+ parameters)
        except:
            newObject = None

        return newObject;
    
 
    @staticmethod
    def CreateHaiducelFeedObject():
        code = "Haiducel"
        paths = PathBuilder(code)
        newObject = ArticlesHaiducel(code, paths, None, None);
        
        return newObject

    @staticmethod
    def GetCodeForOption(option):

        code = None
        objects = [['ArticlesNancy', 'NAN'],
                   ['ArticlesBabyDreams', 'HDRE'],
                   ['ArticlesBebex', 'BEB'],
                   ['ArticlesBebeBrands', 'HBBA'],
                   ['ArticlesBabyShops', 'HMER'],
                   ['ArticlesKidsDecor', 'HDEC'],
                   ['ArticlesHubners', 'HHUB']]             

        for item in objects:
            if item[0]==option:
                code = item[1]
                break
        
        return code

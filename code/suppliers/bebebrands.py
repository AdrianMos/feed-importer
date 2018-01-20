import sys
import os.path
import csv
import configparser
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from code.suppliers.articles import Articles
from article import Article


class ArticlesBebeBrands(Articles):

    @staticmethod
    def getSupplierCode():
        return "HBBA"    
   
    def __init__(self, code, paths, credentials, parameters):
        super().__init__(code, paths, credentials, parameters)
                
        config = configparser.ConfigParser()
        config.read(self.paths.configFile)
        
        self.columnNo = {}
        self.columnNo["id"]= config.getint('Import', 'id')
        self.columnNo["title"] = config.getint('Import', 'title')
        self.columnNo["price"] = config.getint('Import', 'price')
        self.columnNo["pricePromo"] = config.getint('Import', 'pricePromo')
        self.columnNo["description"] = config.getint('Import', 'description')
        self.columnNo["available"] = config.getint('Import', 'available')
        self.columnNo["category"] = config.getint('Import', 'category')
        self.columnNo["image0"] = config.getint('Import', 'image0')
        self.columnNo["image1"] = config.getint('Import', 'image1')
        self.columnNo["image2"] = config.getint('Import', 'image2')
        self.columnNo["image3"] = config.getint('Import', 'image3')
        self.columnNo["image4"] = config.getint('Import', 'image4')
        self.columnNo["image5"] = config.getint('Import', 'image5')
        self.columnNo["image6"] = config.getint('Import', 'image6')
        self.columnNo["image7"] = config.getint('Import', 'image7')
        self.columnNo["image8"] = config.getint('Import', 'image8')
       
    
    def Import(self):
        '''
        Import articles from csv file
        '''    
        print ("    Fisier de import: " + self.paths.feedFileNamePath)
               
        with open(self.paths.feedFileNamePath, "rt") as csvfile:
             
             if self.parameters.quotechar!="":
                reader = csv.reader(csvfile, delimiter=self.parameters.delimiter, quotechar=self.parameters.quotechar)
             else:
                reader = csv.reader(csvfile, delimiter=self.parameters.delimiter)
            
                      
             for row in reader:
                           
                  pret = row[self.columnNo["price"]]
                  pretPromo = row[self.columnNo["pricePromo"]]
                  if pretPromo=="":
                      pretPromo="0"
                         
                  images = [row[self.columnNo["image0"]], 
                            row[self.columnNo["image1"]], 
                            row[self.columnNo["image2"]], 
                            row[self.columnNo["image3"]], 
                            row[self.columnNo["image4"]], 
                            row[self.columnNo["image5"]], 
                            row[self.columnNo["image6"]], 
                            row[self.columnNo["image7"]],
                            row[self.columnNo["image8"]], "", "", ""]
                  
                  
                  # print ("Articol: " + row[ self.columnNo["title"]])
                  # print ("price: " + row[ self.columnNo["price"]])
                  # print ("available: " + row[ self.columnNo["available"]])
                  # print ("cat: " + row[ self.columnNo["category"]])
                  # print ("des: " + row[ self.columnNo["description"]])
                  # print ("img: " + row[ self.columnNo["image0"]])
                  # print ("available: " + row[ self.columnNo["available"]])
                  
                  
                  if row[self.columnNo["id"]]!="":
                      self.articleList.append( Article(id = row[self.columnNo["id"]],
                                                       title = row[ self.columnNo["title"]],
                                                       price = pret,
                                                       pricePromo = pretPromo,
                                                       initialCategory = row[ self.columnNo["category"]],
                                                       category = row[ self.columnNo["category"]],
                                                       available = row[ self.columnNo["available"]],
                                                       description = row[ self.columnNo["description"]],
                                                       weight = 0, #no info in feed
                                                       supplier = "HBBA",
                                                       imagesUrl = images))
                  
                  else:
                      print("     * articol ignorat: ", row[self.columnNo["title"]])    

                 
        return -1            
          
           
    def ComputeAvailability(self, article):
        '''
        Computes the in-stock / out-of-stock status to our format (Active/Inactive)
        :param article: article used for computing.
        '''
        activeVariants = ["stoc suficient", "stoc limitat"]
        if article.available.lower() in activeVariants :
            return "Active"
        else:
            return "Inactive"
    

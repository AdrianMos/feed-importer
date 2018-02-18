import sys
import os.path
import csv
import configparser

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from code.suppliers.articles import Articles
from article import Article


class ArticlesBebex(Articles):
     
    @staticmethod
    def getSupplierCode():
        return "BEB" 

    def __init__(self, code, paths, parameters, downloader, descriptionProcessor):
        super().__init__(code, paths, parameters, downloader, descriptionProcessor)
                
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
        self.columnNo["weight"] = config.getint('Import', 'weight')
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
        print ("    Fisier de import: " + self.paths.feedFile)
               
        with open(self.paths.feedFile, "rt") as csvfile:
             
             if self.parameters.quotechar!="":
                reader = csv.reader(csvfile, delimiter=self.parameters.delimiter, quotechar=self.parameters.quotechar)
             else:
                reader = csv.reader(csvfile, delimiter=self.parameters.delimiter)
            
                      
             counter=0
             for row in reader:
                 counter=counter+1

                 isHeaderRow = counter==1

                 if not isHeaderRow:
                      pret = row[self.columnNo["price"]]
                      pretPromo = row[self.columnNo["pricePromo"]]
                      if pretPromo=="" or pretPromo=="NULL":
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

                      for i in range(0, len(images)):
                          if images[i] == "NULL":
                              images[i] = "";
                                
                      weight = row[self.columnNo["weight"]]
                      weight = weight.replace("kg","").replace(",", ".");
                      
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
                                                           weight = weight,
                                                           supplier = self.getSupplierCode(),
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
        if article.available.lower() in activeVariants:
            return "Active"
        else:
            return "Inactive"

    def GenerateImageNameFromUrl(self, imageUrl):
        '''
        Convert image name to our internal naming. 
          original image:              www.bebex.ro/2079/casuta-pentru-papusi-kaylee.jpg
          after conversion should be:  2079-casuta-pentru-papusi-kaylee.jpg
        :param article:
        '''
        url = imageUrl.replace("\\", "/")
        filename = ""
        if url!="":
            path,file=os.path.split(url)
            extension = url[url.rfind("."):]
            lastDirectoryName = url.split('/')[-2]	    
            
            filename = lastDirectoryName + "-" + file
            
            filename = filename.replace(" ", "-")
            filename = filename.replace("%20", "-")		
        return filename
    

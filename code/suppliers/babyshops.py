import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from code.suppliers.articles import Articles
from article import Article

import csv

class ArticlesBabyShops(Articles):
    '''
    Handles the BabyShops articles (HMER)
    '''
        
    def Import(self):
        '''
        Import articles from csv file
        '''    
        print ("    Fisier de import: " + self.paths.feedFileNamePath)
        
        with open(self.paths.feedFileNamePath, "rt") as csvfile:
             reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
                      
             for row in reader:     
                         
                  pret = str(row["Gross price"]).replace(".", "").replace(",", ".")
                  pretPromo = str(row["Sale gross price"]).replace(".", "").replace(",", ".")
                  if pretPromo=="":
                      pretPromo="0"
                  greutate = row["Weight"]
                     
                  
                  descriere = str(row["Long description"].replace("http://shop.unas.eu", "")) 
                                    
                  
                  if descriere=="":
                  	descriere = row["Short description"]    
                                    
                  categorie=row["Category"]
                    
                  images = [x.strip() for x in str(row["Image URL"]).split(',')]
                                 
               
                  if row["Sku"]!="":
                      #Adauga articolul
                      self.articleList.append( Article(id = row["Sku"],
                                                  title = row["Name"],
                                                  price = pret,
                                                  pricePromo = pretPromo,
                                                  initialCategory = categorie,
                                                  category = categorie,
                                                  available = row["Stock"],
                                                  description = descriere,
                                                  weight = greutate,
                                                  supplier = "HMER",
                                                  imagesUrl = images)) 
                  else:
                      print("     * articol ignorat, lipseste modelul (id): ", row["Name"])         
                 
        return -1             
          
           
    def ComputeAvailability(self, article):
        '''
        Computes the in-stock / out-of-stock status to our format (Active/Inactive)
        :param article: article used for computing.
        '''
        if article.available.lower()=="0":
            return "Inactive"
        else:
            return "Active"
        
        
##    def ComputeImages(self, article):
##        '''
##        Convert image names to our format. 
##          original image: http://babyshops.ro/shop_ordered/9413/shop_pic/20070101.jpg
##          after trimming should be: HMER/20070101.jpg
##        :param article:
##        '''
##        
##        #create a new first element that will include the link to small image
##        newImageNames = [article.imagesUrl[0]]
##        newImageNames.extend(article.images)          
##        
##        for i in range(0, len(newImageNames)):
##            fullPath = newImageNames[i].replace("//", "/")
##            
##            if fullPath=="":
##                newPath = ""
##            else:
##                path,file=os.path.split(fullPath)
##                extension = fullPath[fullPath.rfind("."):]
##                
##                #Extract all characters until second underscore.                
##                if i==0:
##                    #Path to small image, append an _s
##                    newPath = "HMER/" + file[:file.rfind(".")] + "_s" + extension
##                else:
##                    newPath = "HMER/" + file
##            
##            newPath = newPath.replace(" ", "-")
##            newPath = newPath.replace("%20", "-")  
##            newImageNames[i] = newPath
##        
##        # Extend the list to the maximum elements
##        for i in range(len(newImageNames), 13):
##            newImageNames.append("")
##        
##            
##        return newImageNames

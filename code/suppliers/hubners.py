import sys
import os.path
import logging
import csv

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from code.suppliers.articles import Articles
from article import Article


class ArticlesHubners(Articles):
    
    def Import(self):
        '''
        Import articles from csv file
        '''    
        print ("    Fisier de import: " + self.paths.feedFileNamePath)
        
        with open(self.paths.feedFileNamePath, "rt") as csvfile:
            
            reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
             
            for row in reader:
                
                pret = str(row["price"]).replace(".00","").replace(".", "").replace(",", "").replace("RON", "")  # @IndentOk
                pretPromo = str(row["special-price"]).replace(".00","").replace(".", "").replace(",", "").replace("RON", "")
                if pretPromo=="":
                    pretPromo="0"
                                   
              
                descriere = str(row["content:encoded"].replace("Hubners", "")) 
                                                                
                categorie=row["product_subcategory"]  
                
                images = [str(row["additional_image_link_1"]), str(row["additional_image_link_2"]), 
                          str(row["additional_image_link_3"]), str(row["additional_image_link_4"]), 
                          str(row["additional_image_link_5"]), str(row["additional_image_link_6"])]
                   
              
                for i in range(0, len(images)):
                    if (images[i] == None) or (images[i] == "None"):
                        images[i]=""
                                           
           
                if row["id"]!="":
                    #Adauga articolul
                    self.articleList.append( Article(id = row["id"],
                                              title = row["title"],
                                              price = pret,
                                              pricePromo = pretPromo,
                                              initialCategory = categorie,
                                              category = categorie,
                                              available = row["availability"],
                                              description = descriere,
                                              weight = "",
                                              supplier = "HHUB",
                                              imagesUrl = images)) 
                else:
                    print("     * articol ignorat, lipseste modelul (id): ", row["title"])         
         
        return -1        
                      
          
           
    def ComputeAvailability(self, article):
        '''
        Computes the in-stock / out-of-stock status to our format (Active/Inactive)
        :param article: article used for computing.
        '''
        activeVariants = ["in stoc"]
        if article.available.lower() in activeVariants:
            return "Active"
        else:
            return "Inactive"
        
        
##    def ComputeImages(self, article):
##        '''
##        Convert image names to our format. 
##          original image: http://www.hubners.ro/media/catalog/product/i/v/ivory_1.jpeg
##          after trimming should be: HMER/ivory_1.jpeg
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
##                    newPath = "HHUB/" + file[:file.rfind(".")] + "_s" + extension
##                else:
##                    newPath = "HHUB/" + file
##            
##            newPath = newPath.replace(" ", "-")
##            newPath = newPath.replace("%20", "-")
##            newImageNames[i] = newPath
##            
##        
##        # Extend the list to the maximum elements
##        for i in range(len(newImageNames), 13):
##            newImageNames.append("")
##        
##            
##        return newImageNames

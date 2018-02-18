import sys
import os.path
import logging
import csv

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from code.suppliers.articles import Articles
from article import Article


class ArticlesHubners(Articles):

    @staticmethod
    def getSupplierCode():
        return "HHUB" 
        
    def Import(self):
        '''
        Import articles from csv file
        '''    
        print ("    Fisier de import: " + self.paths.feedFile)
        
        with open(self.paths.feedFile, "rt") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
             
            for row in reader:                
                pret = str(row["price"]).replace(".00","").replace(".", "").replace(",", "").replace("RON", "")  # @IndentOk
                pretPromo = str(row["special-price"]).replace(".00","").replace(".", "").replace(",", "").replace("RON", "")
                if pretPromo=="":
                    pretPromo="0"
                                   
                description = str(row["content:encoded"].replace("Hubners", ""))                                           
                                
                images = [str(row["additional_image_link_1"]), str(row["additional_image_link_2"]), 
                          str(row["additional_image_link_3"]), str(row["additional_image_link_4"]), 
                          str(row["additional_image_link_5"]), str(row["additional_image_link_6"])]

                #Extend the list to the maximum elements
                for i in range(len(images), 12):
                    images.append("")

                for i in range(0, len(images)):
                    if (images[i] == None) or (images[i] == "None"):
                        images[i]=""
                
                if row["id"]!="":
                    #Adauga articolul
                    self.articleList.append( Article(id = row["id"],
                                              title = row["title"],
                                              price = pret,
                                              pricePromo = pretPromo,
                                              initialCategory = row["product_subcategory"],
                                              category = row["product_subcategory"],
                                              available = row["availability"],
                                              description = description,
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


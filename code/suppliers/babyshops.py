import sys
import os.path
import csv
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from code.suppliers.articles import Articles
from article import Article


class ArticlesBabyShops(Articles):

    @staticmethod
    def getSupplierCode():
        return "HMER"     
    
    def Import(self):
        '''
        Import articles from csv file
        '''    
        print ("    Fisier de import: " + self.paths.feedFile)
        
        with open(self.paths.feedFile, "rt") as csvfile:
             reader = csv.DictReader(csvfile, delimiter=self.parameters.delimiter, quotechar=self.parameters.quotechar)
                      
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

                  images = [row["Image URL"], 
                            row["Image URL alt1"], 
                            row["Image URL alt2"], 
                            row["Image URL alt3"], 
                            row["Image URL alt4"], 
                            row["Image URL alt5"], 
                            row["Image URL alt6"], 
                            row["Image URL alt7"],
                            row["Image URL alt8"],
                            row["Image URL alt9"], "", ""]           
               
                  if row["Sku"]!="":
                      self.articleList.append( Article(id = row["Sku"],
                                                  title = row["Name"],
                                                  price = pret,
                                                  pricePromo = pretPromo,
                                                  initialCategory = categorie,
                                                  category = categorie,
                                                  available = row["Stock"],
                                                  description = descriere,
                                                  weight = greutate,
                                                  supplier = self.getSupplierCode(),
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

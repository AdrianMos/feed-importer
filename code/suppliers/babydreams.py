import sys
import os.path
import logging
import csv

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from code.suppliers.articles import Articles
from article import Article


class ArticlesBabyDreams(Articles):
     
    @staticmethod
    def getSupplierCode():
        return "HDRE" 
   
    def Import(self):
        '''
        Import articles from csv file
        '''  
        numErrors = 0
          
        print ("    Fisier de import: " + self.paths.feedFile)
        with open(self.paths.feedFile, 'rt') as csvfile:
            #reader = csv.reader(csvfile, delimiter='|')
            reader = csv.DictReader(csvfile, delimiter='|', quotechar='"')
             
            for index, row in enumerate(reader):                 
                try:
                    pret = str(row["pret_recomandat"]).replace(".", "").replace(",", ".")
                    pretPromo = str(row["pret_promo"]).replace(".", "").replace(",", ".")
                    greutate = str(row["greutate_kg"]).replace(".", "").replace(",", ".")
                    
                    images = [x.strip() for x in row["imagini"].split(',')]

                    #Extend the list to the maximum elements
                    for i in range(len(images), 12):
                        images.append("")
                     
                    self.articleList.append( Article(id = row["cod"],
                                                  title = row["denumire"],
                                                  price = pret,
                                                  pricePromo = pretPromo,
                                                  initialCategory = row["categoria"],
                                                  category = row["categoria"],
                                                  available = row["stoc"],
                                                  description = row["descriere"],
                                                  weight = greutate,
                                                  supplier = self.getSupplierCode(),
                                                  imagesUrl = images)) 
                except:
                    logging.error('Import(): Eroare import articol index ' +  str(index) + ' cod (posibil eronat):' + row["cod"])
                    numErrors = numErrors + 1
                    continue
                
        return numErrors
            
           
    def ComputeAvailability(self, article):
        '''
        Computes the in-stock / out-of-stock status to our format (Active/Inactive)
        :param article: article used for computing.
        '''
        activeVariants = ["1"]
        if article.available.lower() in activeVariants:
            return "Active"
        else:
            return "Inactive"
        

    def GenerateImageNameFromUrl(self, imageUrl):
        '''
        Convert image name to our internal naming. 
          original image:             http://www.kidcity.ro/data_files/product_photos/9797/large_1.jpg
          after conversion should be: 9797_large_1.jpg
        :param article:
        '''
        url = imageUrl.replace("\\", "/")
        filename = ""
        if url!="":
            path,file=os.path.split(url)
            extension = url[url.rfind("."):]
            lastDirectoryName = url.split('/')[-2]	    
            
            filename = lastDirectoryName + "_" + file
            
            filename = filename.replace(" ", "-")
            filename = filename.replace("%20", "-")		
        return filename

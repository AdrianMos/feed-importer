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
    
    def DownloadFeed(self):
    
        print("*** Descarcare feed HDRE...")
        response = urllib.request.urlopen('http://www.kidcity.ro/products_feed_csv.php')           
        
        feedData = response.read().decode("cp1252").encode('unicode_escape')
        feedData = feedData.decode('unicode_escape').encode('ascii', 'ignore')       
              
        with open(self.paths.feedFileNamePath, 'wb') as textfile:
            textfile.write(feedData)
            textfile.close()
            
        print("    Feed HDRE descarcat.")
    
    def Import(self):
        '''
        Import articles from csv file
        '''  
        numErrors = 0
          
        print ("    Fisier de import: " + self.paths.feedFileNamePath)
        with open(self.paths.feedFileNamePath, 'rt') as csvfile:
            #reader = csv.reader(csvfile, delimiter='|')
            reader = csv.DictReader(csvfile, delimiter='|', quotechar='"')
             
            for index, row in enumerate(reader):                 
                try:
                    pret = str(row["pret_recomandat"]).replace(".", "").replace(",", ".")
                    pretPromo = str(row["pret_promo"]).replace(".", "").replace(",", ".")
                    greutate = str(row["greutate_kg"]).replace(".", "").replace(",", ".")
                    
                    images = [x.strip() for x in row["imagini"].split(',')]
                     
                    self.articleList.append( Article(id = row["cod"],
                                                  title = row["denumire"],
                                                  price = pret,
                                                  pricePromo = pretPromo,
                                                  initialCategory = row["categoria"],
                                                  category = row["categoria"],
                                                  available = row["stoc"],
                                                  description = row["descriere"],
                                                  weight = greutate,
                                                  supplier = "HDRE",
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

##    def ComputeImages(self, article):
##        '''
##        Convert image names to our format. 
##          original image:             http://www.kidcity.ro/data_files/product_photos/9797/large_1.jpg
##          after conversion should be: fileadmin/img/9797_large_1.jpg
##        :param article:
##        '''
##        #create a new first element that will include the link to small image
##        newImageNames = [article.imagesUrl[0]]
##        newImageNames.extend(article.images)          
##        
##        for i in range(0, len(newImageNames)):
##          fullPath = newImageNames[i].replace("\\", "/")
##          
##          if fullPath=="":
##            newPath = ""
##          else:
##            path,file=os.path.split(fullPath)
##            extension = fullPath[fullPath.rfind("."):]
##            lastDirectoryName = fullPath.split('/')[-2]	    
##            
##            #Extract all characters until second underscore.                
##            if i==0:
##              #Path to small image, append an _s
##              newPath = "fileadmin/img/" + lastDirectoryName + "_" + file[:file.rfind(".")] + "_s" + extension
##            else:
##              newPath = "fileadmin/img/" + lastDirectoryName + "_" + file
##          
##          newPath = newPath.replace(" ", "-")
##          newPath = newPath.replace("%20", "-")		
##          newImageNames[i] = newPath
##        
##        # Extend the list to the maximum elelemnts
##        for i in range(len(newImageNames), 13):
##            newImageNames.append("")
##        
##        	
##        return newImageNames

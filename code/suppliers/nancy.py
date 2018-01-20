import sys
import os.path
import csv
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from code.suppliers.articles import Articles
from article import Article



class ArticlesNancy(Articles):
    
    @staticmethod
    def getSupplierCode():
        return "NAN" 
        
    def Import(self):
         '''
         Import articles from csv file
         '''
         print("*** Import articole ...")     
         print ("    Fisier de import: " + self.paths.feedFileNamePath)

         with open(self.paths.feedFileNamePath, 'rt') as csvfile:
             reader = csv.reader(csvfile, delimiter='|')
             
             for row in reader:
                 self.articleList.append( Article(id = row[0],
                                                  title = row[1],
                                                  description = row[2],
                                                  price = row[3],
                                                  weight = row[5],
                                                  available = row[4],
                                                  initialCategory = row[7],
                                                  category = row[7],
                                                  supplier = "NAN",
                                                  imagesUrl = [row[8], row[9], row[10], row[11], row[12], row[13],
                                                               row[14], row[15], row[16],row[17],row[18], row[19]]))
         print("    Import terminat.")
         return -1


    def ComputeAvailability(self, article):
        '''
        Computes the in-stock / out-of-stock status to our format (Active/Inactive)
        :param article: article used for computing.
        '''
        activeVariants = ["produs pe stoc", "comanda speciala", "produs limitat"]
        if article.available.lower() in activeVariants:
            return "Active"
        else:
            return "Inactive"
    
    
    
    def GenerateImageNameFromUrl(self, imageUrl):
        '''
        Converts the image url into an internal file naming.
        e.g.
          url: http://www.importatorarticolecopii.ro/prodpics/p_105156c46838594_set lenjerie pat www.mykids.jpg
          returns: "p_105156c46838594.jpg", on success
                   "noimage.jpg", on failure
                   "" for empty url
        :param imageUrl:
        '''
        if imageUrl=="":
            return ""
            
        url = imageUrl.replace("\\", "/")
        path,file = os.path.split(url)
        
        isBrokenPath = (file=="" or path=="" or file.rfind("_")==-1 or file.rfind(".")==-1)
        if isBrokenPath:
            return "noimage.jpg"
        
        filename = file.replace(" ", "-").replace("%20", "-")
       
        wordsToBeRemoved = ["www.mykids", "my_kids", "my-kids", "mykids", "Mykids.ro", "baby-shop",
                            "MyKids.ro", "Mykids", "MyKids", "My-Kyds"]
        for word in wordsToBeRemoved:
            filename = filename.replace(word, "")
                   
        return filename



from articles import Articles
from article import Article

import csv
import os.path

class ArticlesKidsDecor(Articles):
     
    def Import(self):
         '''
         Import articles from csv file
         '''
         
         '''
         0 Categorie  | 1 Producator | 2 Cod produs | 3 Bucati? | 4 Denumire produs |
         5 Descriere  | 6 Link | 7 Imagine | 8 Pret | 9 Moneda  | 10  Empty | 11 Disponibilitate
         '''

         print ("    Fisier de import: " + self.paths.feedFileNamePath)
         with open(self.paths.feedFileNamePath, 'rt') as csvfile:
             reader = csv.reader(csvfile, delimiter='|')
             
             counter=0
             for row in reader:
                 counter=counter+1
                 
                           
                 # Append article to list
                 if row.__len__() == 13:
                     descriere = row[5]
                     #print(counter);
                     
                     self.articleList.append( Article(id = row[2],
                                                  title = row[4],
                                                  description = descriere,
                                                  price = row[8],
                                                  weight = 0,
                                                  available = row[11],
                                                  initialCategory = row[0],
                                                  category = row[0],
                                                  supplier = "HDEC",
                                                  imagesUrl = [row[7], "", "", "", "", "", "", "", "", "", "", ""]))
         return -1

    def ComputeAvailability(self, article):
        '''
        Computes the in-stock / out-of-stock status to our format (Active/Inactive)
        :param article: article used for computing.
        '''
        activeVariants = ["in stock", "2-3 zile", "pre-comanda"]
        if article.available.lower() in activeVariants :
            return "Active"
        else:
            return "Inactive"
          
                   
##    def ComputeImages(self, article):
##        '''
##        Convert image names to our format. 
##          original image: http://www.kidsdecor.ro/image/data/mobilier/patut-lemn-baby-italia-andreea-lux-gliter.jpg
##          after processing should be: HDEC/patut-lemn-baby-italia-andreea-lux-gliter.jpg
##        :param article:
##        '''
##        #create a new first element that will include the link to small image
##        newImageNames = [article.imagesUrl[0]]
##        newImageNames.extend(article.images)
##           
##        for i in range(0, len(newImageNames)):
##             
##             fullPath = newImageNames[i].replace("\\", "/")
##           
##             if fullPath=="":
##                 newPath = ""
##             else:
##                 path,file=os.path.split(fullPath)
##                 
##                 extension = fullPath[fullPath.rfind("."):]
##                 posPoint = file.rfind(".")
##                 
##                 #Extract all characters until point                
##                 if i==0:
##                     #Path to small image, append an _s
##                     newPath = "HDEC/" + file[:posPoint] + "_s" + extension  
##                 else:
##                     newPath = "HDEC/" + file[:posPoint] + extension
##             
##             newPath = newPath.replace(" ", "-")
##             newPath = newPath.replace("%20", "-")   
##             newImageNames[i] = newPath   
##        return newImageNames
     

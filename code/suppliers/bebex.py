import sys
import os.path
import logging
import csv

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from code.suppliers.articles import Articles
from article import Article


class ArticlesBebex(Articles):
     
    def Import(self):
         '''
         Import articles from csv file
         '''         
        
         '''        
         0 cod, 1 denumire, 2 categorie, 3 brand, 4 descriere, 5 url_produs, 6 imagine_principala,
         7 imagine_suplimentara, 8 imagine_suplimentara, 9 imagine_suplimentara, 10 imagine_suplimentara, 
        11 imagine_suplimentara, 12 imagine_suplimentara, 13 imagine_suplimentara, 14 imagine_suplimentara, 
        15 pret_recomandat_catre_client, 16 pret_de_achizitie_revanzator, 17 pret_promo_catre_client, 
        18 pret_promo_achizitie_revanzator, 19 info_pret, 20 tip, 21 pentru, 22 varsta,
        23 material, 24 culoare, 25 greutate, 26 garantie, 27 disponibilitate
         '''           
         print("*** Import articole ...")     
         print ("    Fisier de import: " + self.paths.feedFileNamePath)
         
         with open(self.paths.feedFileNamePath, 'rt', encoding="latin1") as csvfile:
             reader = csv.reader(csvfile, delimiter=',', quotechar='"')
             counter=0
             for row in reader:
                 counter=counter+1
                 
                 if counter>1:
                     
                      if row[17] != "NULL":
                          pretPromo = row[17]
                      else:
                          pretPromo = 0;
                         
                     
                      imagesArray = [row[6],  row[7],  row[8],  row[9], row[10],
                                    row[11], row[12], row[13], row[14],  "", "", ""]
                      
                      for i in range(0, len(imagesArray)):
                        if imagesArray[i] == "NULL":
                            imagesArray[i] = "";
                            
                      greutate = row[25].replace("kg","").replace(",", ".");
                                         
                     
                      self.articleList.append( Article(id = row[0],
                                                  title = row[1],
                                                  description = row[4],
                                                  price = row[15],
                                                  pricePromo = pretPromo,
                                                  weight = greutate,
                                                  available = row[27],
                                                  initialCategory = row[2],
                                                  category = row[2],
                                                  supplier = "BEB",
                                                  imagesUrl = imagesArray))
             
         print("    Import terminat.")     
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
          
                   
##    def ComputeImages(self, article):
##        '''
##        Convert image names to our format. 
##          original image: http://www.bebex.ro/701-thickbox_default/jucarie-educativa-din-plus-piramida.jpg
##          after processing should be: BEB/jucarie-educativa-din-plus-piramida.jpg
##        :param article:
##        '''
##        #create a new first element thath will include the link to small image
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
##                     newPath = "BEB/" + file[:posPoint] + "_s" + extension  
##                 else:
##                     newPath = "BEB/" + file[:posPoint] + extension
##             
##             newPath = newPath.replace(" ", "-")
##             newPath = newPath.replace("%20", "-")
##             newImageNames[i] = newPath
##        return newImageNames

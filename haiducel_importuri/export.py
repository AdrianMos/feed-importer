'''
Created on 26.04.2014

@author: adrian
'''
from articles import Articles
import csv
import collections


class Export(object):
    '''
    classdocs
    '''
        
    header = collections.OrderedDict()
    header.update( [("id" , "v_products_model"),
                   ("title2" , "v_products_name_2"),
                   ("description2" , "v_products_description_2"),
                   ("title1" , "v_products_name_1"),
                   ("description1" , "v_products_description_1"),
                   ("imageSmall" , "v_products_image")])
    
    for i in range(1, 13):
        header.update([("image"+str(i), "v_products_images_image_" + str(i))])
                       
        
    header.update([("supplier" , "v_products_supplier"),
                   ("price" , "v_products_price"),
                   #("priceSpecial" , "v_products_specials_price"),
                   ("quantity" , "v_products_quantity"),
                   ("weight" , "v_products_weight"),
                   ("category2" , "v_categories_name_1_2"),
                   ("category1" , "v_categories_name_1_1"),
                   ("subcategory2" , "v_categories_name_2_2"),
                   ("subcategory1" , "v_categories_name_2_1"),
                   ("available" , "v_status"),
                   ("eor" , "EOREOR")])
       
       
    def __init__(self):
        '''
        Constructor
        '''
        pass
        
    def ExportAllData(self, articles, filename):
        
        with open(filename, 'wt', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', 
                                quoting=csv.QUOTE_NONNUMERIC,
                                lineterminator='\n')
            writer.writerow(list(self.header.values()))
            
           
            for a in articles.articleList:
                
                row = [a.id, a.title, a.description, a.title, 
                       a.description, a.imagesNew[0], 
                       a.imagesNew[1], a.imagesNew[2], a.imagesNew[3], 
                       a.imagesNew[4], a.imagesNew[5], a.imagesNew[6],
                       a.imagesNew[7], a.imagesNew[8], a.imagesNew[9], 
                       a.imagesNew[10], a.imagesNew[11], a.imagesNew[12],
                       a.supplier, a.price, a.quantity, a.weight,
                       a.category, a.category, a.subcategory, a.subcategory,
                       a.available, "EOREOR"]
                writer.writerow(row)
                
        print ("    Fisier salvat:\n      \t" + filename)

    def ExportDataForOnlineshop(self, articles, filename):
            
        with open(filename, 'wt', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', 
                                quoting=csv.QUOTE_NONNUMERIC, 
                                lineterminator='\n')
            writer.writerow(list(self.header.values()))
            
            for a in articles.articleList:
                
                row = [a.id, a.title, a.description, a.title, 
                       a.description, "", 
                       a.images[0], a.images[1], a.images[2], a.images[3], 
                       a.images[4], a.images[5], a.images[6], a.images[7], 
                       a.images[8], a.images[9], a.images[10], a.images[11],
                       a.supplier, a.price, a.quantity, a.weight,
                       a.category, a.category, a.subcategory, a.subcategory,
                       a.available, "EOREOR"]
                writer.writerow(row)
                
        print ("    Fisier salvat:\n      \t" + filename)
    
    def ExportPriceAndAvailability(self, articles, filename):
        
        with open(filename, 'wt') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', 
                                quoting=csv.QUOTE_MINIMAL,
                                lineterminator='\n')
            writer.writerow([self.header["id"], self.header["price"], 
                             self.header["available"], self.header["eor"]])
           
            for a in articles.articleList:
                row = [a.id, a.price, a.available, "EOREOR"]
                writer.writerow(row)   
      
    def ExportArticlesForDeletion(self, articles, filename):
        
        with open(filename, 'wt') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL,
                                lineterminator='\n')
            writer.writerow([self.header["id"], self.header["available"],
                             self.header["eor"]])
           
            for a in articles.articleList:
                row = [a.id, "Delete", "EOREOR"]
                writer.writerow(row)              
                
        print ("    Fisier salvat:\n      \t" + filename)
    
    
    def ExportPriceAndAvailabilityAndMessages(self, 
                                              articles, 
                                              messages,
                                              filename):
        
        with open(filename, 'wt') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL,
                                lineterminator='\n')
            writer.writerow([self.header["id"], self.header["price"], 
                             self.header["available"], self.header["eor"], 
                             "", "Mesaj comparare"])
           
            for a in articles.articleList:
                row = [a.id, a.price, a.available, "EOREOR", 
                      "", messages[str(a.id)]]
                writer.writerow(row)
                
        print ("    Fisier salvat:\n      \t" + filename)
    
        

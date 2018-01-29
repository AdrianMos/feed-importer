'''
Created on 26.04.2014

@author: Adrian Mos
'''
from code.suppliers.articles import Articles
import csv
import collections


class Export(object):        
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
        pass
        
    def ExportAllData(self, articles, filename):
        
        with open(filename, 'wt', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', 
                                quoting=csv.QUOTE_NONNUMERIC,
                                lineterminator='\n')
            writer.writerow(list(self.header.values()))
            
           
            for a in articles.articleList:
                
                row = [a.id, a.title, a.description, a.title, a.description,
                       a.imageSmallPath]
                row.extend(a.imagesPaths)
                
                row.extend([a.supplier, a.price, a.quantity, a.weight,
                       a.category, a.category, a.subcategory, a.subcategory,
                       a.available, "EOREOR"])
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
                       a.imagesUrl[0], a.imagesUrl[1], a.imagesUrl[2],  a.imagesUrl[3], 
                       a.imagesUrl[4], a.imagesUrl[5], a.imagesUrl[6],  a.imagesUrl[7], 
                       a.imagesUrl[8], a.imagesUrl[9], a.imagesUrl[10], a.imagesUrl[11],
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
    
        

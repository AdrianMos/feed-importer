import sys
import os.path
import csv
import logging
from code.messages import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from code.suppliers.articles import Articles
from code.article import Article


class ArticlesHaiducel(Articles):
    '''
    Handles the articles already imported in our database.
    '''
    
    @staticmethod
    def getSupplierCode():
        return "Haiducel"     
    
    def Import(self):
         '''
         Import articles from csv file, oscommerce easypopulate format
         '''
         print ("    Fisier de import: " + self.paths.feedFile)
         
         if (not os.path.isfile(self.paths.feedFile)):
             message = '   \nEROARE: Nu s-a gasit feed-ul Haiducel la calea: ' \
                       + self.paths.feedFile             
             logging.error(message)
             PrintExeptionAndQuit(message, None)
             
          
         with open(self.paths.feedFile, 'rt', encoding="latin1") as csvfile:
             
             reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
                          
                          
             for row in reader:
                 self.articleList.append( Article(id = row["v_products_model"],
                                                  title = row["v_products_name_1"],
                                                  description = row["v_products_description_1"],
                                                  price = row["v_products_price"],
                                                  weight = row["v_products_weight"],
                                                  available = row["v_status"],
                                                  initialCategory = row["v_categories_name_1_1"] + "#" + row["v_categories_name_2_1"],
                                                  category = row["v_categories_name_1_1"],
                                                  subcategory = row["v_categories_name_2_1"],
                                                  quantity = row["v_products_quantity"],
                                                  supplier = row["v_products_supplier"],
                                                  imagesUrl = [row["v_products_image"], 
                                                               row["v_products_images_image_1"], row["v_products_images_image_2"], 
                                                               row["v_products_images_image_3"], row["v_products_images_image_4"],
                                                               row["v_products_images_image_5"], row["v_products_images_image_6"],
                                                               row["v_products_images_image_7"], row["v_products_images_image_8"],
                                                               row["v_products_images_image_9"], row["v_products_images_image_10"], 
                                                               row["v_products_images_image_11"],row["v_products_images_image_12"]])) 
         return -1          


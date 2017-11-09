'''
Created on 26.04.2014

@author: adrian mos
'''
from article import Article
from pathbuilder import PathBuilder
from descriptionprocessor import DescriptionProcessor

import codecs
import csv
import os
import collections
import urllib.request
import sys
import pdb
import logging
from _ast import Try
from bs4 import BeautifulSoup, NavigableString
import bleach
import re
import requests
import configparser


class Articles(object):
    '''
    classdocs
    '''
    articleList=[]
    paths = PathBuilder("")
    code = ""

    def __init__(self, code):
        '''
        Constructor
        '''
        self.articleList = []
        self.code = code
        self.paths = PathBuilder(code)
        
        
        # Check the folders availability for this client. Create the folder structure if necessary.
        clientFolder = os.path.join(os.getcwd(), self.code, "out");
        if not os.path.isdir(clientFolder):
            print("Folderul pentru acest cod nu exista, se va crea automat: " + clientFolder)
            
            try:
                os.makedirs(clientFolder)
            except OSError as ex:
                sys.exit("Nu se poate crea folderul pentru acest cod: " + ex.reason)
                logging.error("Articles constructor: nu se poate crea folderul <" + clientFolder + "> : mesaj : " + ex.reason)
                raise
            
             
    def DownloadFeed(self):
        '''
        Downloads articles feeds
        '''
        raise NotImplementedError
        print("*** Functionalitatea de download nu a fost implementata.")
        pass
    
    def ArticlesCount(self):
        return self.articleList.__len__()
    
    @staticmethod
    def DownloadAndSaveImage(imgUrl, imgSavePath1, imgSavePath2=""):
        try:
            #print ("trying to open url: *" + imgUrl + "*")
            # Download image
            
            #req = urllib.Request(imgUrl, headers={'User-Agent' : "Magic Browser"}) 
            #con = urllib.request
            #(, headers={'User-Agent' : "Magic Browser"}).urlopen(imgUrl)
            #data = con.read()
                  
            imgUrl = imgUrl.replace(" ", "%20")
                    
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) Ubuntu/12.04 Chromium/18.0.1025.168 Chrome/18.0.1025.168 Safari/535.19'
            req = urllib.request.Request(imgUrl, headers={'User-Agent': user_agent})
            
            response = urllib.request.urlopen(req)
            data = response.read()
          
            
            #print("--" + req.full_url + "--")
            #u = urllib.request.urlopen(req)
           
            
            
            #req = urllib.request.Request(url="http://localhost/",data=b'None',headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
            #data = urllib.request.urlopen(imgUrl)
            
            #urllib.urlretriev("http://www.gunnerkrigg.com//comics/00000001.jpg", "00000001.jpg")
            
            #response = urllib.request.urlopen(imgUrl)
            #data = response.read()
            
            
            # Save image
            with open(imgSavePath1, 'wb') as file:
                file.write(data)
            
            # If a second save path location has been given, save the image in this location
            if imgSavePath2!="":
                with open(imgSavePath2, 'wb') as file:
                    file.write(data)
            #print("#path" + imgSavePath1 + " #orig path:" + imgUrl)
        
        except OSError as ex:
            print("Eroare salvare fisier: " + imgSavePath1 + " si/sau " + imgSavePath2 +"\n   motiv:"+ ex.reason)  
            logging.error("DownloadAndSaveImage : eroare salvare fisier: " + imgSavePath1 + " si/sau " + imgSavePath2 +"\n   motiv:"+ ex.reason)   
        
       # except IOError as (errno, strerror):
       #      print ("I/O error({0}): {1}" + errno + strerror)
   
        #except IOError as ex: 
        #    print("Eroare salvare fisier: " + imgSavePath1 + " si/sau " + imgSavePath2  +"\n   motiv:"+ ex.reason)   
            
        except urllib.error.HTTPError as ex:
            print ("Unexpected error:",  ex.reason)
            logging.error("DownloadAndSaveImage : " + ex.reason)
      
        except urllib.error.URLError as ex:
            print("Eroare download: " + imgUrl + "\n  motiv: " + ex.reason + " ++" + str(sys.exc_info()[0]))
            logging.error("DownloadAndSaveImage : nu se poate downloada <" + imgUrl + "> motiv: " + ex.reason + " ++" + str(sys.exc_info()[0]))   
            raise
    
    
    
    def RemoveCrapArticles(self):
        '''
        Removes articles which shouldn't be imported.
        '''
        removedItems = 0
        crap = ['olita', 'olite', 'scutec', 'reductor wc', 'capac wc', 'servetel', 'tampoane', 'tampon', 'prosop', 'suzeta', 'sosetele', 'tacamuri']
        print("    Articolele ce contin in titlu ", crap, " sunt eliminate.")
        
                
        itemsBeforeRemoval = self.ArticlesCount()
        self.articleList = [art for art in self.articleList if not any(crapDetector in art.title.lower() for crapDetector in crap)]
         
        print("    Articole eliminate din feed: " + str(itemsBeforeRemoval - self.ArticlesCount()))
     
       
    def DownloadImages(self):
        '''
        Downloads the customer images
        '''
         
        ''' Images urls are stored in articlesList.images and new image names in articlesList.imagesNew.
            On the first position of articlesList.imagesNew the small image name is stored. '''
        
        print("\n*** Se descarca imaginile pentru " + str(self.articleList.__len__()) + " de articole")
        
        print("    Folder descarcare: " + self.paths.allImagesFolder)
        print("                       " + self.paths.mainImagesFolder + "\n")
        
        
        for art in self.articleList:
            
            #print('.', end='')
            #print("image next", end=" ")
            
            imgCounter=0
            
            # Download all images for current article
            for imgUrl in art.images:
                
                if imgUrl!="":
                    
                    # Image name; Extract only the filename from whole path
                    imgNameNew = art.imagesNew[imgCounter+1] 
                    imgNameNew = imgNameNew[imgNameNew.rfind("/")+1:]
                                                                                                   
                    # If the main image is downloaded, save it also to a separate folder - later used
                    # for generating the small image
                    try:
                        if imgCounter==0:
                            self.DownloadAndSaveImage(imgUrl, os.path.join(self.paths.allImagesFolder, imgNameNew), os.path.join(self.paths.mainImagesFolder,imgNameNew)) 
                        else:
                            self.DownloadAndSaveImage(imgUrl, os.path.join(self.paths.allImagesFolder, imgNameNew)) 
                    except:
                        e = sys.exc_info()[0]
                        print ("\nEROARE descarcare imagine pentru articolul: ", art.title, ' @ ', imgNameNew, "@", imgUrl, " eroare:", e)
                        logging.error('articles: articol <' + art.title + '> : eroare descarcare imagine <' + imgUrl + '> : mesaj eroare : ' + e)
                        
                    sys.stdout.write(".")
                    sys.stdout.flush()
                                              
                imgCounter = imgCounter+1                   
            
            sys.stdout.write("/")
            sys.stdout.flush()
    
            
        print("\n") 
    
    def Import(self):
         '''
         Import articles from file
         '''
         print ("*** Functionalitatea de import nu a fost implementata.")
         
         return -1
         
    def Add(self, id, title, price, available, category, supplier):
           
        if available=="Active" or available=="Inactive" or available=="Delete":
            activeStatus = available
        else:
            activeStatus = "Inactive"
        
        self.articleList.append( Article(id = id, title = title, price=price, available=activeStatus, category=category, supplier=supplier)) 
       
    def Add1(self, article):
        self.articleList.append(article)
        
    
    def ComputePrice(self, article):
        '''
        Calculates the new price that will be used in our database.
        Use the promo price if available; decrease prices with 1 leu; Don't display prices <160 lei
        :param article: article used for computing the price
        
        Requirements: 
          Prices less than 350 should be set to 0 (not displayed).
          Display promo price if available. 
          Displayed prices should be decreased with 1.
        '''  
        result = float(article.price)-0.1
        
        # If promo price available, and smaller than price     
        if (article.pricePromo < article.price and article.pricePromo > 0):
            result = float(article.pricePromo)-0.1
        
        # Prices less than 350 should be set to 0
        if result<350:
            return 0
        else:
            return result
        
        
    def ComputeAvailability(self, article):
        '''
        Computes the in-stock / out-of-stock status
        :param article: article used for computing.
        '''
        return "Active"
           
    
    def ComputeCategory(self, article):
        '''
        Computes the category for the current article.
        '''
        categorie = article.category.lower()
        
        '''
        First map element is the searched Key element; 
        second and third elements are the new Category and Subcategory.
        '''
        
        map = [["rucioare copii",               "_CARUCIOARE",          "2 in 1"],
			   ["crucioare|crucioare multifuncionale 2 in 1",                     "_CARUCIOARE",          "2 in 1"],
               ["rucioare pentru copii",        "_CARUCIOARE",          "2 in 1"],
               ["rucioare cu landou",           "_CARUCIOARE",          "3 in 1"],
               ["rucioare 3 in 1",              "_CARUCIOARE",          "3 in 1"],
               ["rucioare",                     "_CARUCIOARE",          "2 in 1"],
                          
               
               ["cosulete auto",                "_Cosulete AUTO",       ""],
               ["scaun - cos auto",             "_Cosulete AUTO",       ""],
               ["cos - auto",                   "_Cosulete AUTO",       ""],        
               ["scaun auto",                   "_Scaune AUTO",         ""],
                      
               ["inaltatoare auto",             "_Inaltatoare AUTO",    ""],
               ["inaltator auto",               "_Inaltatoare AUTO",    ""],
               
               ["marsupii",                     "_PLIMBARE COPII",    "Marsupii, portbebe"],
               ["ham de siguranta",             "_PLIMBARE COPII",    "Marsupii, portbebe"],
               ["ham pentru copii",             "_PLIMBARE COPII",    "Marsupii, portbebe"],
               ["portbebe",                     "_PLIMBARE COPII",    "Marsupii, portbebe"],
               
                               
               ["scaune auto",                  "_Scaune AUTO",         ""],
               ["scaune de masa",               "_Scaune de MASA",      ""],
               ["scaun de masa",                "_Scaune de MASA",      ""],
               ["scaun masa",                   "_Scaune de MASA",      ""],
                
               ["mobiliere camere copii",       "_CAMERA copilului",    "Mobilier"],
               ["fotolii pentru copii",         "_CAMERA copilului",    "Mobilier"],
               ["fotolii din burete",           "_CAMERA copilului",    "Mobilier"],
               ["mobilier copii",               "_CAMERA copilului",    "Mobilier"],
               ["bucatarii si accesorii",       "_CAMERA copilului",    "Mobilier"],
               ["bucatarii din lemn pentru copii", "_CAMERA copilului",    "Mobilier"],
                             
              
               ["lenjerie de pat",              "_CAMERA copilului",    "Lenjerie patut"],
               ["set lenjerie",                 "_CAMERA copilului",    "Lenjerie patut"],
               ["perna",                        "_CAMERA copilului",    "Lenjerie patut"], 
               ["lenjerie",                     "_CAMERA copilului",    "Lenjerie patut"], 
               ["patura",                       "_CAMERA copilului",    "Lenjerie patut"],  
               ["saci de dormit",               "_CAMERA copilului",    "Lenjerie patut"],  
               ["sac de dormit",                "_CAMERA copilului",    "Lenjerie patut"],            
               ["patuturi din lemn",            "_CAMERA copilului",    "Patuturi din lemn"],
               ["patut din lemn",               "_CAMERA copilului",    "Patuturi din lemn"],
               ["patut pliabil",                "_CAMERA copilului",    "Patuturi voiaj si tarcuri"],
               ["pat pliant",                   "_CAMERA copilului",    "Patuturi voiaj si tarcuri"],
               ["pat pliabil",                  "_CAMERA copilului",    "Patuturi voiaj si tarcuri"],
               ["patuturi voiaj si tarcuri",    "_CAMERA copilului",    "Patuturi voiaj si tarcuri"],
               ["patuturi in forma de masina",  "_CAMERA copilului",    "Patuturi in forma de masina"],               
               ["patut",                        "_CAMERA copilului",    "Patuturi voiaj si tarcuri"],
               ["spatii de joaca",              "_CAMERA copilului",    "Spatii de joaca"],
               ["masute si scaune",             "_CAMERA copilului",    "Spatii de joaca"],
               ["centre de activitate",         "_CAMERA copilului",    "Spatii de joaca"],
               ["tarc",                         "_CAMERA copilului",    "Spatii de joaca"],
               ["saritoare",                    "_CAMERA copilului",    "Spatii de joaca"],
               ["paturici",                     "_CAMERA copilului",    "Saci dormit si paturici"],
             
               
               ["comode",                       "_CAMERA copilului",    "Mobilier"],
               ["carusel",                      "_CAMERA copilului",    "Carusele"],
               ["saltele",                      "_CAMERA copilului",    "Saltele patut"],
               ["saltea",                       "_CAMERA copilului",    "Saltele patut"],
               ["blat si saltea de infasat",    "_CAMERA copilului",    "Saltele infasat"],
               ["saltelute de infasat",         "_CAMERA copilului",    "Saltele infasat"],
               ["blat de infasat",              "_CAMERA copilului",    "Saltele infasat"],
               ["saltea de infasat",            "_CAMERA copilului",    "Saltele infasat"],
               
               ["balansoare si leagane",        "_BALANSOARE si leagane",  ""],
               ["balansoar",                    "_BALANSOARE si leagane",  ""],
               ["leagane",                      "_BALANSOARE si leagane",  ""],
               
               ["incalzitor biberon",           "_IGIENA si siguranta",  "Incalzitor si sterilizator"],
               ["sterilizator",                 "_IGIENA si siguranta",  "Incalzitor si sterilizator"],
               
               ["monitoare de respiratie",      "_IGIENA si siguranta",  "Inlterfoane si video"],
               ["interfoane",                   "_IGIENA si siguranta",  "Interoane si video"],
               
               ["igiena",                       "_IGIENA si siguranta",  "Protectie si ingrijire"],
               ["siguranta copilului",          "_IGIENA si siguranta",  "Protectie si ingrijire"],
               ["bariere pentru patuturi",      "_IGIENA si siguranta",  "Protectie si ingrijire"],
               ["set de ingrijire",             "_IGIENA si siguranta",  "Protectie si ingrijire"],
               ["semn de avertizare",           "_IGIENA si siguranta",  "Protectie si ingrijire"],
               ["semne de avertizare",          "_IGIENA si siguranta",  "Protectie si ingrijire"],
               ["aspiratoare nazale",           "_IGIENA si siguranta",  "Protectie si ingrijire"],
               ["aspirator nazal",              "_IGIENA si siguranta",  "Protectie si ingrijire"],
               ["inele gingivale",              "_IGIENA si siguranta",  "Protectie si ingrijire"],              

               ["pompe de san",                 "_IGIENA si siguranta",  "Nutritie"],
               ["pompa de san",                 "_IGIENA si siguranta",  "Nutritie"],
               ["pompe pentru san",             "_IGIENA si siguranta",  "Nutritie"],
               ["pompa san",                    "_IGIENA si siguranta",  "Nutritie"],
               ["recipient stocarea laptelui",  "_IGIENA si siguranta",  "Nutritie"],
               ["recipient stocarea laptelui",  "_IGIENA si siguranta",  "Nutritie"],
               ["biberoane",                    "_IGIENA si siguranta",  "Nutritie"],
               ["bavetica",                     "_IGIENA si siguranta",  "Nutritie"],
               ["robot bucatarie",              "_IGIENA si siguranta",  "Nutritie"],
               
               ["aerosol",                      "_IGIENA si siguranta",  "Aerosol si umidificator"],
               ["aersol",                       "_IGIENA si siguranta",  "Aerosol si umidificator"],
               ["umidificator",                 "_IGIENA si siguranta",  "Aerosol si umidificator"],

               ["termometr",                    "_IGIENA si siguranta",  "Termometre"],
               
                              
               ["articole pentru baie",         "_IGIENA si siguranta",  "Baie"],
               ["cadita",                       "_IGIENA si siguranta",  "Baie"],
               ["cadite",                       "_IGIENA si siguranta",  "Baie"],
               
               
               ["cantare elect",                "_IGIENA si siguranta",  "Cantare"],
               ["cantar elect",                 "_IGIENA si siguranta",  "Cantare"],
               ["cantare mecanice",             "_IGIENA si siguranta",  "Cantare"],
               ["cantare pentru copii",         "_IGIENA si siguranta",  "Cantare"],
               ["cantare copii",                "_IGIENA si siguranta",  "Cantare"],
               
               ["accesorii ingrijire copii",    "_IGIENA si siguranta",  ""],
               ["manichiura si pedichiura bebe","_IGIENA si siguranta",  ""],             
               
               
               ["leagane de gradina",           "_BALANSOARE si leagane",  ""],
                              
               ["genti pentru mamici",          "_Viitoare MAMICI",  "Genti mamici"],
               ["geanta carucior",              "_Viitoare MAMICI",  "Genti mamici"],
               ["mmici|geni",                   "_Viitoare MAMICI",  "Genti mamici"],
               ["gentute",                      "_Viitoare MAMICI",  "Genti mamici"],
               ["genti pentru scutece",         "_Viitoare MAMICI",  "Genti mamici"],
               
               
               
                
               ["triciclet",                    "_PLIMBARE copii",  "Triciclete si trotinete"],
               ["trotinet",                     "_PLIMBARE copii",  "Triciclete si trotinete"],
               ["biciclet",                     "_PLIMBARE copii",  "Biciclete"],
               ["masin",                        "_PLIMBARE copii",  "Masinute"],
               ["tractoare",                    "_PLIMBARE copii",  "Masinute"],
               ["tractore cu pedale",           "_PLIMBARE copii",  "Masinute"],
               ["vehicule pentru copii",        "_PLIMBARE copii",  "Masinute"],
               
               
               
               ["premergatoare",                "_PLIMBARE copii",  "Premergatoare"],
               ["premergator",                  "_PLIMBARE copii",  "Premergatoare"],
               ["saniute",                      "_PLIMBARE copii",  "Saniute"],
               ["sanie",                        "_PLIMBARE copii",  "Saniute"],
              
               ["jocuri",                       "_JUCARII si jocuri",  ""],
               ["jucari",                      "_JUCARII si jocuri",  ""],
               ["jucrii",                       "_JUCARII si jocuri",  ""],
               ["jeep",                         "_JUCARII si jocuri",  ""],
               ["seturi de constructii",        "_JUCARII si jocuri",  ""],
               ["piste si garaje",              "_JUCARII si jocuri",  ""],
               ["joaca",                        "_JUCARII si jocuri",  ""],
               ["cort",                         "_JUCARII si jocuri",  ""],
               ["papusi",                       "_JUCARII si jocuri",  ""],
               ["trenuri",                      "_JUCARII si jocuri",  ""],
               ["seturi de bile colorate",      "_JUCARII si jocuri",  ""],
               
               
               ["scutece",                      "_DESTERS",            ""],
               ["olita",                        "_DESTERS",            ""],
               ["reductor capac wc",            "_DESTERS",            ""],
               ["suzete",                       "_DESTERS",            ""],
               ["cana",                         "_DESTERS",            ""],
               ["lingurite",                    "_DESTERS",            ""],
               ["servetele",                    "_DESTERS",            ""],
               
               ]
                 
        
        # Try to categorize the articles by the supplier's category
        #   Go through the map and check if the first element is included in the category
        for item in map:
            # Return the new category and subcategory if the element is included (second and third element of the map)
            if item[0] in categorie:
                return (item[1], item[2])
        
        
        title = article.title.lower()
               
        # If the article could not be chategorized so far, try to cathegorize them by title
        for item in map:
            # Return the new category and subcategory if the element is included (second and third element of the map)
            if item[0] in title:
                return (item[1], item[2])
               
        print("      * categorie necunoscuta:" + categorie + ". Articol neclasificat. Denumire: " + article.title)  
        logging.warning("ComputeCategory: categorie necunoscuta: <" + categorie + ">. Articol neclasificat: " + article.title)
        return ("_Neclasificate", "")
      
    def ComputeImages(self, article):
        '''
        Computes the new paths for images.
        :param article: article used for computing.
        '''
        print("*** Functionalitatea de prelucrare nume imagini nu a fost implementata.")
        pass
    
        
    def ComputeDescription(self, article):
        '''
        Computes the  product description. Removes html format which might destroy the site aspect.
        :param article: article to be processed
        '''
        # Remove the product name from description
        description = article.description.replace(article.title, "")
                
        # Replace &lt;b&gt; with <b> and &lt;/b&gt with </b>
        # Remove <b></b> tags with no text contained
        #newDescription = newDescription.replace("&lt;b&gt;","<b>").replace("&lt;/b&gt","</b>").replace("<b></b>","")
        #newDescription = newDescription.replace("<strong>:</strong>", "").replace("<strong> </strong>", "").replace("<strong></strong>", "")
        
        return DescriptionProcessor.CleanDescription(description)    
       
    def ConvertToOurFormat(self):
        '''
        Converts all data to our format
        '''
        for article in self.articleList:
            article.price        = self.ComputePrice(article)
            article.available    = self.ComputeAvailability(article)
            article.category, article.subcategory = self.ComputeCategory(article)
            article.imagesNew    = self.ComputeImages(article)
            article.description  = self.ComputeDescription(article)
            #print (article.description)
    
    def FilterBySupplier(self, supplier):
        
        filteredArticles = Articles(self.code)
        for article in self.articleList:
            if article.supplier == supplier:
                filteredArticles.Add1(article)
        
        return filteredArticles
        
      
class NANArticles(Articles):
    
    username = ""
    password = ""
    downloadUrl = ""
    
    def __init__(self, code):
        super().__init__(code)
                
        config = configparser.ConfigParser()
        config.read(self.paths.configFile)
        self.username = config.get('Download', 'username')
        self.password = config.get('Download', 'password')
        self.downloadUrl = config.get('Download', 'url')       
        
    
    def DownloadFeed(self):
    
        print("*** Descarcare feed NAN...")        
        
        response = requests.get(self.downloadUrl,
                                verify=False, 
                                auth=(self.username, self.password))

        feedData = response.text 
        
        with open(self.paths.feedFileNamePath, 'wb') as textfile:
            textfile.write(bytes(feedData, 'UTF-8'))
            textfile.close()
        
        print("    Feed NAN descarcat.")


    def Import(self):
         '''
         Import articles from csv file
         '''
         
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
                                                  category = row[7],
                                                  supplier = "NAN",
                                                  images = [row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16],row[17],row[18], row[19]]))
         return -1


    def ComputeAvailability(self, article):
        '''
        Computes the in-stock / out-of-stock status to our format (Active/Inactive)
        :param article: article used for computing.
        '''
        if article.available.lower()=="produs pe stoc" or article.available.lower()=="comanda speciala":
            return "Active"
        else:
            return "Inactive"
          
                   
    def ComputeImages(self, article):
        '''
        Convert image names to our format. 
          original image: http://www.importatorarticolecopii.ro/prodpics/p_105156c46838594_set lenjerie pat copii pek safari verde 1 my kids baby shop www.mykids.jpg
          after trimming should be: NAN/p_105156c46838594.jpg
        :param article:
        '''
        #create a new first element thath will include the link to small image
        newImageNames = [article.images[0]]
        newImageNames.extend(article.images)
           
        for i in range(0, len(newImageNames)):
             
             fullPath = newImageNames[i].replace("\\", "/")
             
             if fullPath=="":
                 newPath = ""
             else:
                 path,file=os.path.split(fullPath)
                 
                 extension = fullPath[fullPath.rfind("."):]
                 posLastUnderscore = file.rfind("_")
                 
                 #Extract all characters until second underscore.                
                 if i==0:
                     #Path to small image, append an _s
                     newPath = "NAN/" + file[:posLastUnderscore] + "_s" + extension  
                 else:
                     newPath = "NAN/" + file[:posLastUnderscore] + extension
                 
             newImageNames[i] = newPath   
        return newImageNames

class BEBArticles(Articles):
     
    def DownloadFeed(self):
    
        print("*** Descarcare feed BEBEX...")
        # response = urllib.request.urlopen('http://www.bebex.ro/feed/datafeed_produse_general_csv.php')
        response = urllib.request.urlopen('http://www.bebex.ro/datafeed/complete/csv/')
        
        feedData = response.read().decode("utf-8-sig").encode("raw_unicode_escape")
        feedData = feedData.decode('unicode_escape').encode('ascii','ignore')
       
        
        with open(self.paths.feedFileNamePath, 'wb') as textfile:
            textfile.write(feedData)
            textfile.close()
        
        print("    Feed BEBEX descarcat.")
        #print(feedData)

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
                                                  category = row[2],
                                                  supplier = "BEB",
                                                  images = imagesArray))
             
         return -1
        
        
        
              
    def ComputeAvailability(self, article):
        '''
        Computes the in-stock / out-of-stock status to our format (Active/Inactive)
        :param article: article used for computing.
        '''
        
        if article.available.lower()=="stoc suficient" or article.available.lower()=="stoc limitat":
            return "Active"
        else:
            return "Inactive"
          
                   
    def ComputeImages(self, article):
        '''
        Convert image names to our format. 
          original image: http://www.bebex.ro/701-thickbox_default/jucarie-educativa-din-plus-piramida.jpg
          after processing should be: BEB/jucarie-educativa-din-plus-piramida.jpg
        :param article:
        '''
        #create a new first element thath will include the link to small image
        newImageNames = [article.images[0]]
        newImageNames.extend(article.images)
           
        for i in range(0, len(newImageNames)):
             
             fullPath = newImageNames[i].replace("\\", "/")
           
             if fullPath=="":
                 newPath = ""
             else:
                 path,file=os.path.split(fullPath)
                 
                 extension = fullPath[fullPath.rfind("."):]
                 posPoint = file.rfind(".")
                 
                 #Extract all characters until point                
                 if i==0:
                     #Path to small image, append an _s
                     newPath = "BEB/" + file[:posPoint] + "_s" + extension  
                 else:
                     newPath = "BEB/" + file[:posPoint] + extension
                 
             newImageNames[i] = newPath   
        return newImageNames


class HDREArticles(Articles):
    '''
    Handles the BabyDreams artiles (HDRE)
    '''
     
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
                                                  category = row["categoria"],
                                                  available = row["stoc"],
                                                  description = row["descriere"],
                                                  weight = greutate,
                                                  supplier = "HDRE",
                                                  images = images)) 
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
        if article.available.lower()=="1":
            return "Active"
        else:
            return "Inactive"
        
        
    def ComputeImages(self, article):
        '''
        Convert image names to our format. 
          original image:             http://www.kidcity.ro/data_files/product_photos/9797/large_1.jpg
          after conversion should be: fileadmin/img/9797_large_1.jpg
        :param article:
        '''
        #create a new first element that will include the link to small image
        newImageNames = [article.images[0]]
        newImageNames.extend(article.images)          
        
        for i in range(0, len(newImageNames)):
        	fullPath = newImageNames[i].replace("\\", "/")
        	
        	if fullPath=="":
        		newPath = ""
        	else:
        		path,file=os.path.split(fullPath)
        		extension = fullPath[fullPath.rfind("."):]
        		lastDirectoryName = fullPath.split('/')[-2]	    
        		
        		#Extract all characters until second underscore.                
        		if i==0:
        			#Path to small image, append an _s
        			newPath = "fileadmin/img/" + lastDirectoryName + "_" + file[:file.rfind(".")] + "_s" + extension
        		else:
        			newPath = "fileadmin/img/" + lastDirectoryName + "_" + file
        			
        	newImageNames[i] = newPath
        
        # Extend the list to the maximum elelemnts
        for i in range(len(newImageNames), 13):
            newImageNames.append("")
        
        	
        return newImageNames

             
class HaiducelArticles(Articles):
    '''
    Handles the articles already imported in our database.
    '''
    
    def Import(self):
         '''
         Import articles from csv file, oscommerce easypopulate format
         '''
         print ("    Fisier de import: " + self.paths.feedFileNamePath)
         
         if (not os.path.isfile(self.paths.feedFileNamePath)):
             logging.error('HaiducelArticles: Import: Nu s-a gasit feed-ul Haiducel la calea: ' + self.paths.feedFileNamePath)
             sys.exit("   \nEROARE: Nu s-a gasit feed-ul Haiducel !!!")
         
          
         with open(self.paths.feedFileNamePath, 'rt', encoding="latin1") as csvfile:
             
             reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
                          
                          
             for row in reader:
                 self.articleList.append( Article(id = row["v_products_model"],
                                                  title = row["v_products_name_1"],
                                                  description = row["v_products_description_1"],
                                                  price = row["v_products_price"],
                                                  weight = row["v_products_weight"],
                                                  available = row["v_status"],
                                                  category = row["v_categories_name_1_1"],
                                                  subcategory = row["v_categories_name_2_1"],
                                                  quantity = row["v_products_quantity"],
                                                  supplier = row["v_products_supplier"],
                                                  images = [row["v_products_image"], 
                                                            row["v_products_images_image_1"], row["v_products_images_image_2"], 
                                                            row["v_products_images_image_3"], row["v_products_images_image_4"],
                                                            row["v_products_images_image_5"], row["v_products_images_image_6"],
                                                            row["v_products_images_image_7"], row["v_products_images_image_8"],
                                                            row["v_products_images_image_9"], row["v_products_images_image_10"], 
                                                            row["v_products_images_image_11"],row["v_products_images_image_12"]])) 
         return -1          

class BebeBrandsArticles(Articles):
    '''
    Handles the BebeBrands articles (HBBA)
    '''
        
    def DownloadFeed(self):
       
        print("*** Descarcare feed BebeBrands HBBA...")
        response = urllib.request.urlopen('http://www.bebebrands.ro/wp-content/themes/Emporium/feed-produse-csv.php')
                
        feedData = response.read().decode("utf-8-sig").encode("raw_unicode_escape")
        feedData = feedData.decode('unicode_escape').encode('ascii','ignore')
     
        with open(self.paths.feedFileNamePath, "wb") as textfile:
            textfile.write(feedData)
            textfile.close()
            
        print("    Feed BebeBrands descarcat.")
    
    
    def Import(self):
        '''
        Import articles from csv file
        '''    
        print ("    Fisier de import: " + self.paths.feedFileNamePath)
        
        with open(self.paths.feedFileNamePath, "rt") as csvfile:
             reader = csv.DictReader(csvfile, delimiter=',', quotechar='\'')
                      
             for row in reader:
                           
                  pret = str(row["price"]).replace(".", "").replace(",", ".")
                  pretPromo = str(row["specialprice"]).replace(".", "").replace(",", ".")
                  if pretPromo=="":
                      pretPromo="0"
                  greutate = 0 #nu exista informatia in feed
                  
                  
                  #Extrage categoria din "permalink"
                  #    permalink = http://www.bebebrands.ro/igiena-si-siguranta/summer-infant-19176-suport-de-baita-deluxe-cu-bara-de-jucarii
                  try:
                      categorie = str(row["permalink"])[25:]
                      categorie = categorie[:categorie.find("/")].replace("-"," ")
                  except:
                      categorie=""
                         
                  
                  #split the images by "g," because some image names contain "," and we cannot split only by comma
                  # afterwards "g" has to be added to the split image names          
                  images = [x.strip() +"g" for x in str(row["images"]).split('g,')]
                  
                  if images[images.__len__()-1]=="g":
                      images[images.__len__()-1]=""
               
                  if row["id"]!="":
                      #Adauga articolul
                      self.articleList.append( Article(id = row["id"],
                                                  title = row["title"],
                                                  price = pret,
                                                  pricePromo = pretPromo,
                                                  category = categorie,
                                                  available = row["availability"],
                                                  description = row["description"],
                                                  weight = greutate,
                                                  supplier = "HBBA",
                                                  images = images)) 
                  else:
                      print("     * articol ignorat, lipseste modelul (id): ", row["title"])         
                 
        return -1            
          
           
    def ComputeAvailability(self, article):
        '''
        Computes the in-stock / out-of-stock status to our format (Active/Inactive)
        :param article: article used for computing.
        '''
        if article.available.lower()=="yes":
            return "Active"
        else:
            return "Inactive"
        
        
    def ComputeImages(self, article):
        '''
        Convert image names to our format. 
          original image: http://www.bebebrands.ro/wp-content/uploads/products_img/t1lxjaxefxxxbasr.u_015645.jpg
          after trimming should be: HBBA/t1lxjaxefxxxbasr.u_015645.jpg
        :param article:
        '''
        
        #create a new first element that will include the link to small image
        newImageNames = [article.images[0]]
        newImageNames.extend(article.images)          
        
        for i in range(0, len(newImageNames)):
            fullPath = newImageNames[i].replace("//", "/")
            
            if fullPath=="":
                newPath = ""
            else:
                path,file=os.path.split(fullPath)
                extension = fullPath[fullPath.rfind("."):]
                
                #Extract all characters until second underscore.                
                if i==0:
                    #Path to small image, append an _s
                    newPath = "HBBA/" + file[:file.rfind(".")] + "_s" + extension
                else:
                    newPath = "HBBA/" + file
                    
            newImageNames[i] = newPath
        
        # Extend the list to the maximum elements
        for i in range(len(newImageNames), 13):
            newImageNames.append("")
        
            
        return newImageNames


class BabyShopsArticles(Articles):
    '''
    Handles the BabyShops articles (HMER)
    '''
        
    def DownloadFeed(self):
       
        print("*** Descarcare feed BabyShops HMER...")
        response = urllib.request.urlopen('http://shop.unas.eu/ro/admin_export.php?shop_id=9413&format=babyshops.ro')
                
        feedData = response.read().decode("utf-8-sig").encode("raw_unicode_escape")
        feedData = feedData.decode('unicode_escape').encode('ascii','ignore')
     
        with open(self.paths.feedFileNamePath, "wb") as textfile:
            textfile.write(feedData)
            textfile.close()
            
        print("    Feed BabyShops descarcat.")
    
    
    def Import(self):
        '''
        Import articles from csv file
        '''    
        print ("    Fisier de import: " + self.paths.feedFileNamePath)
        
        with open(self.paths.feedFileNamePath, "rt") as csvfile:
             reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
                      
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
                    
                  images = [x.strip() for x in str(row["Image URL"]).split(',')]
                                 
               
                  if row["Sku"]!="":
                      #Adauga articolul
                      self.articleList.append( Article(id = row["Sku"],
                                                  title = row["Name"],
                                                  price = pret,
                                                  pricePromo = pretPromo,
                                                  category = categorie,
                                                  available = row["Stock"],
                                                  description = descriere,
                                                  weight = greutate,
                                                  supplier = "HMER",
                                                  images = images)) 
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
        
        
    def ComputeImages(self, article):
        '''
        Convert image names to our format. 
          original image: http://babyshops.ro/shop_ordered/9413/shop_pic/20070101.jpg
          after trimming should be: HMER/20070101.jpg
        :param article:
        '''
        
        #create a new first element that will include the link to small image
        newImageNames = [article.images[0]]
        newImageNames.extend(article.images)          
        
        for i in range(0, len(newImageNames)):
            fullPath = newImageNames[i].replace("//", "/")
            
            if fullPath=="":
                newPath = ""
            else:
                path,file=os.path.split(fullPath)
                extension = fullPath[fullPath.rfind("."):]
                
                #Extract all characters until second underscore.                
                if i==0:
                    #Path to small image, append an _s
                    newPath = "HMER/" + file[:file.rfind(".")] + "_s" + extension
                else:
                    newPath = "HMER/" + file
                
            newImageNames[i] = newPath
        
        # Extend the list to the maximum elements
        for i in range(len(newImageNames), 13):
            newImageNames.append("")
        
            
        return newImageNames

    def ComputeCategory(self, article):
        '''
        Computes the category for the current article.
        '''
        categorie = article.category.lower()
        
        '''
        First map element is the searched Key element; 
        second and third elements are the new Category and Subcategory.
        '''
        
        map = [["camera copilului|accesorii",	 	 				"_CAMERA copilului", 	"Saci dormit si paturici"],
               ["jucrii|covorae de joac",							"_CAMERA copilului",  	"Spatii de joaca"],
               ["ptuuri pliabile",				  					"_CAMERA copilului",		"Patuturi voiaj si tarcuri"],
               ["jucrii|carusele muzicale",		  					"_CAMERA copilului",		"Carusele"],
               
               ["crucioare|accesorii carucioare",    				"_PLIMBARE COPII",   	"Marsupii, portbebe" ],
               ["marsupii",    										"_PLIMBARE COPII",   	"Marsupii, portbebe" ],
               
               ["crucioare|carucioare multifunctionale 3 in 1",		"_CARUCIOARE",		  	"3 in 1"],
               ["crucioare|carucioare nou-nascuti",					"_CARUCIOARE",		  	"Sport"],
               ["crucioare|crucioare sport",						"_CARUCIOARE",		  	"Sport"],
               ["crucioare|crucioare multifuncionale 2 in 1",		"_CARUCIOARE",		  	"2 in 1"],
               ["crucioare|crucioare pentru gemeni",				"_CARUCIOARE",		  	"Gemeni"],
              
               ["scaune auto",                   					"_Scaune AUTO",         ""],
               ["scaune de mas",                  					"_Scaune de MASA",      ""],
               
               ["camera copilului|paturici",                        "_CAMERA copilului",    "Lenjerie patut"],  
               ["camera copilului|lenjerii patuturi",               "_CAMERA copilului",    "Lenjerie patut"],  
               ["camera copilului|saltelute de infasat",            "_CAMERA copilului",    "Saltele infasat"],
                
               ["sanatate si igiena",				  				"_IGIENA si siguranta",  ""],
               ["la mas|",				  							"_IGIENA si siguranta",  ""],
               ["in baie|manusi de baie, halat de baie, prosoape",	"_IGIENA si siguranta",  ""],
               ["in baie|termometre",				  				"_IGIENA si siguranta",  ""],
               ["sigurana bebeluului|",				  				"_IGIENA si siguranta",  ""],
               
               ["jucrii|balansoare/leagne",        					"_BALANSOARE si leagane",  ""],
               ["jucrii|",						 					"_JUCARII si jocuri",  ""],            
                     
               ["pentru mmici|geni",		  						"_Viitoare MAMICI",  "Genti mamici"],
			   ["pentru mmici",			 	  						"_Viitoare MAMICI",  "Diverse"],
		  
               ["camera copilului|sosetele",                        "_DESTERS",          ""]
              
        
               ]
                 
        
        # Try to categorize the articles by the supplier's category
        #   Go through the map and check if the first element is included in the category
        for item in map:
            # Return the new category and subcategory if the element is included (second and third element of the map)
            if item[0] in categorie:
                return (item[1], item[2])
        
        
        title = article.title.lower()
               
        # If the article could not be chategorized so far, try to cathegorize them by title
        for item in map:
            # Return the new category and subcategory if the element is included (second and third element of the map)
            if item[0] in title:
                return (item[1], item[2])
               
        print("      * categorie necunoscuta:" + categorie + ". Articol neclasificat. Denumire: " + article.title)  
        logging.warning("BabyShopsArticles: ComputeCategory: categorie necunoscuta:" + categorie + ". Articol neclasificat: " + article.title)  
        return ("_Neclasificate", "")
     
class KidsDecorArticles(Articles):
     
    def DownloadFeed(self):
    
        print("*** Descarcare feed KidsDecor...")
        response = urllib.request.urlopen('http://kidsdecor.ro/feed/datafeed_kidsdecor.php')
         
        feedData = response.read().decode("utf-8-sig").encode("raw_unicode_escape")
        feedData = feedData.decode('unicode_escape').encode('ascii','ignore')
        
        with open(self.paths.feedFileNamePath, 'wb') as textfile:
            textfile.write(feedData)
            textfile.close()
        
        print("    Feed KidsDecor descarcat.")
        #print(feedData)

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
                                                  category = row[0],
                                                  supplier = "HDEC",
                                                  images = [row[7], "", "", "", "", "", "", "", "", "", "", ""]))
         return -1

    def ComputeAvailability(self, article):
        '''
        Computes the in-stock / out-of-stock status to our format (Active/Inactive)
        :param article: article used for computing.
        '''
        
        if article.available.lower()=="in stock" or article.available.lower()=="2-3 zile" or article.available.lower()=="pre-comanda" :
            return "Active"
        else:
            return "Inactive"
          
                   
    def ComputeImages(self, article):
        '''
        Convert image names to our format. 
          original image: http://www.kidsdecor.ro/image/data/mobilier/patut-lemn-baby-italia-andreea-lux-gliter.jpg
          after processing should be: HDEC/patut-lemn-baby-italia-andreea-lux-gliter.jpg
        :param article:
        '''
        #create a new first element that will include the link to small image
        newImageNames = [article.images[0]]
        newImageNames.extend(article.images)
           
        for i in range(0, len(newImageNames)):
             
             fullPath = newImageNames[i].replace("\\", "/")
           
             if fullPath=="":
                 newPath = ""
             else:
                 path,file=os.path.split(fullPath)
                 
                 extension = fullPath[fullPath.rfind("."):]
                 posPoint = file.rfind(".")
                 
                 #Extract all characters until point                
                 if i==0:
                     #Path to small image, append an _s
                     newPath = "HDEC/" + file[:posPoint] + "_s" + extension  
                 else:
                     newPath = "HDEC/" + file[:posPoint] + extension
                 
             newImageNames[i] = newPath   
        return newImageNames
     
     
class HubnersArticles(Articles):
    '''
    Handles the Hubners articles (HHUB)
    '''
        
    def DownloadFeed(self):
       
        print("*** Descarcare feed Hubners HHUB...")
        response = urllib.request.urlopen('http://www.hubners.ro/datafeed_csv.php')
                    
        feedData = response.read().decode("utf-8-sig").encode("raw_unicode_escape")
        feedData = feedData.decode('unicode_escape').encode('ascii','ignore')
             
        with open(self.paths.feedFileNamePath, "wb") as textfile:
            textfile.write(feedData)
            textfile.close()
            
        print("    Feed Hubners descarcat.")
    
    
    def Import(self):
        '''
        Import articles from csv file
        '''    
        print ("    Fisier de import: " + self.paths.feedFileNamePath)
        
        with open(self.paths.feedFileNamePath, "rt") as csvfile:
            
            reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
             
            for row in reader:
                
                pret = str(row["price"]).replace(".00","").replace(".", "").replace(",", "").replace("RON", "")  # @IndentOk
                pretPromo = str(row["special-price"]).replace(".00","").replace(".", "").replace(",", "").replace("RON", "")
                if pretPromo=="":
                    pretPromo="0"
                                   
              
                descriere = str(row["content:encoded"].replace("Hubners", "")) 
                                                                
                categorie=row["product_subcategory"]  
                
                images = [str(row["additional_image_link_1"]), str(row["additional_image_link_2"]), 
                          str(row["additional_image_link_3"]), str(row["additional_image_link_4"]), 
                          str(row["additional_image_link_5"]), str(row["additional_image_link_6"])]
                   
              
                for i in range(0, len(images)):
                    if (images[i] == None) or (images[i] == "None"):
                        images[i]=""
                                           
           
                if row["id"]!="":
                    #Adauga articolul
                    self.articleList.append( Article(id = row["id"],
                                              title = row["title"],
                                              price = pret,
                                              pricePromo = pretPromo,
                                              category = categorie,
                                              available = row["availability"],
                                              description = descriere,
                                              weight = "",
                                              supplier = "HHUB",
                                              images = images)) 
                else:
                    print("     * articol ignorat, lipseste modelul (id): ", row["title"])         
         
        return -1        
                      
          
           
    def ComputeAvailability(self, article):
        '''
        Computes the in-stock / out-of-stock status to our format (Active/Inactive)
        :param article: article used for computing.
        '''
        if article.available.lower()=="in stoc":
            return "Active"
        else:
            return "Inactive"
        
        
    def ComputeImages(self, article):
        '''
        Convert image names to our format. 
          original image: http://www.hubners.ro/media/catalog/product/i/v/ivory_1.jpeg
          after trimming should be: HMER/ivory_1.jpeg
        :param article:
        '''
        
        #create a new first element that will include the link to small image
        newImageNames = [article.images[0]]
        newImageNames.extend(article.images)          
        
        for i in range(0, len(newImageNames)):
            fullPath = newImageNames[i].replace("//", "/")
            
            if fullPath=="":
                newPath = ""
            else:
                path,file=os.path.split(fullPath)
                extension = fullPath[fullPath.rfind("."):]
                
                #Extract all characters until second underscore.                
                if i==0:
                    #Path to small image, append an _s
                    newPath = "HHUB/" + file[:file.rfind(".")] + "_s" + extension
                else:
                    newPath = "HHUB/" + file
                
            newImageNames[i] = newPath
        
        # Extend the list to the maximum elements
        for i in range(len(newImageNames), 13):
            newImageNames.append("")
        
            
        return newImageNames


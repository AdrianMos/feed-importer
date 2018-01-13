import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from code.article import Article
from code.pathbuilder import PathBuilder
from code.credentials import Credentials
from code.descriptionprocessor import DescriptionProcessor

import codecs
import csv
import os
import collections
import urllib.request
import pdb
import logging
from _ast import Try
from bs4 import BeautifulSoup, NavigableString
import bleach
import re
import requests
import configparser


class Articles(object):

    def __init__(self, code, paths, credentials, parameters):

        self.articleList = []
        self.code = code
        self.credentials = credentials
        self.paths = paths
        self.parameters = parameters
        
        # Check the folders availability for this client. Create the folder structure if necessary.
        clientFolder = PathBuilder.getOutputFolderPath(code)
        
        if not os.path.isdir(clientFolder):
            print("Folderul pentru acest cod nu exista, se va crea automat: " + clientFolder)
            
            try:
                os.makedirs(clientFolder)
            except OSError as ex:
                sys.exit("Nu se poate crea folderul pentru acest cod: " + ex.reason)
                logging.error("Articles constructor: nu se poate crea folderul <" + clientFolder + "> : mesaj : " + ex.reason)
                raise
        
        
    def DownloadFeed(self, credentials):

        print("*** Descarcare feed " + self.code + "...")     
               
        isPasswordRequired = credentials.username != ""               
        
        if isPasswordRequired: 
            response = requests.get(self.parameters.downloadUrl,
                                    verify=False, 
                                    auth=(credentials.username, credentials.password))
                                    
            if  response.status_code != 200:
                print("\nEROARE: Parola si/sau utilizatorul nu sunt valide, status: " + str(response.status_code))
                sys.exit("   \nEROARE: Parola si/sau utilizatorul nu sunt valide, status: " + str(response.status_code))
            
            feedData = response.text 
            
            with open(self.paths.feedFileNamePath, 'wb') as textfile:
                textfile.write(bytes(feedData, 'UTF-8'))
                textfile.close()
        else:
            response = urllib.request.urlopen(self.parameters.downloadUrl)
                          
            feedData = response.read().decode("utf-8-sig").encode("raw_unicode_escape")
            feedData = feedData.decode('unicode_escape').encode('ascii','ignore')
         
            with open(self.paths.feedFileNamePath, "wb") as textfile:
                textfile.write(feedData)
                textfile.close()
            
        print("    Feed " + self.code + " descarcat.")
        
            
    def ArticlesCount(self):
        return self.articleList.__len__()
    

    def DownloadAndSaveImage(self, imgUrl, credentials, imgSavePath1, imgSavePath2=""):
                
        try:
            imgUrl = imgUrl.replace(" ", "%20")
            imgUrl = self.RepairBrokenUrl(imgUrl)
            
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) ' + \
                         'Ubuntu/12.04 Chromium/18.0.1025.168 Chrome/18.0.1025.168 Safari/535.19'
            
            if credentials.username != "":
                                                        
                response = requests.get(imgUrl,
                                        verify=False, 
                                        auth=(credentials.username, credentials.password),
                                        headers={'user-agent': user_agent})
                                
                if response.status_code == 200:
                    with open(imgSavePath1, 'wb') as file:
                        file.write(response.content)
                    
                    # If a second save path location has been given, save the image in this location
                    if imgSavePath2!="":
                        with open(imgSavePath2, 'wb') as file:
                            file.write(response.content)
            
            else:
                req = urllib.request.Request(imgUrl, headers={'User-Agent': user_agent})
                response = urllib.request.urlopen(req)
                data = response.read()                
                
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
            
        except urllib.error.HTTPError as ex:
            print ("Unexpected error:",  ex.reason)
            logging.error("DownloadAndSaveImage : " + ex.reason)
      
        except urllib.error.URLError as ex:
            print("Eroare download: " + imgUrl + "\n  motiv: " + ex.reason + " ++" + str(sys.exc_info()[0]))
            logging.error("DownloadAndSaveImage : nu se poate downloada <" + imgUrl + "> motiv: " + ex.reason + " ++" + str(sys.exc_info()[0]))   
            raise
    
    def RepairBrokenUrl(self, url):
        repaired = url.replace(":www", "://www")
        return repaired
    
    def RemoveCrapArticles(self):
        '''
        Removes unwanted articles.
        '''
        crap = ['olita', 'olite', 'scutec', 'reductor wc', 'capac wc', 'servetel', 'tampoane', 'tampon', 'prosop', 'suzeta', 'sosetele', 'tacamuri']
        print("    Articolele ce contin in titlu ", crap, " sunt eliminate.")
        
                
        itemsBeforeRemoval = self.ArticlesCount()
        self.articleList = [art for art in self.articleList if not any(crapDetector in art.title.lower() for crapDetector in crap)]
         
        print("    Articole eliminate din feed: " + str(itemsBeforeRemoval - self.ArticlesCount()))
     
    #@staticmethod   
    def DownloadImages(self, credentials):
        '''
        Downloads the customer images
        '''
         
        ''' Images urls are stored in articlesList.images and new image names in articlesList.imagesNew.
            On the first position of articlesList.imagesNew the small image name is stored. '''
        
        print("\n*** Se descarca imaginile pentru " + str(self.articleList.__len__()) + " de articole")
        print("    Folder descarcare: " + self.paths.allImagesFolder)
        print("                       " + self.paths.mainImagesFolder + "\n")
        
        for art in self.articleList:       
            # Download all images for current article
            for i, imgUrl in enumerate(art.imagesUrl):
             
                if imgUrl!="":  
                    try:
                        # If the main image is downloaded, save it also to a separate folder - later used
                        # for generating the small image
                        isMainImage = (i==0)
                        if isMainImage:
                            self.DownloadAndSaveImage(imgUrl, credentials, 
                                                      imgSavePath1 = os.path.join(self.paths.allImagesFolder, art.imagesNames[i]),
                                                      imgSavePath2 = os.path.join(self.paths.mainImagesFolder,art.imagesNames[i])) 
                        else:
                            self.DownloadAndSaveImage(imgUrl, credentials, 
                                                       imgSavePath1 = os.path.join(self.paths.allImagesFolder,art.imagesNames[i])) 
                    except:
                        e = sys.exc_info()[0]
                        print ("\nEROARE descarcare imagine pentru articolul: ", art.title, ' @ ', art.imagesNames[i], "@", imgUrl, " eroare:", e)
                        logging.error('articles: articol <' + art.title + '> : eroare descarcare imagine <' + imgUrl + '> : mesaj eroare : ' + e)
                    
                    
                    sys.stdout.write(".")
                    sys.stdout.flush()
            
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
           
        if available in ["Active", "Inactive", "Delete"]:
            activeStatus = available
        else:
            activeStatus = "Inactive"
        
        self.articleList.append( Article(id = id, title = title, price=price, available=activeStatus, category=category, supplier=supplier)) 
       
    def Add1(self, article):
        self.articleList.append(article)
        
    
    def ComputePrice(self, article):
        '''
        Calculates the new price that will be used in our database.
        '''   
        return 0
        
    
    def GetMappingKey(self, article):
        '''
        Returns a mapping key, used for remapping an article.
        The key is used for finding a section for an article in the mapping configuration file.
        :param article: article for which the mapping key is returned
        '''
        return article.initialCategory.lower()
        
        
    def FindSectionForKey(self, searchKey, map):          
        searchKeyTrimedSpaces = "".join(searchKey.split())
        fallbackValue = ""
        section = map.get(searchKeyTrimedSpaces, fallbackValue)
        return section
        
    def UpdateArticleBasedOnMappedSection(self, article, section):
        ''' The section to which the article has been mapped to
            includes the new category & subcategory [category#subcategory]
            Extract the category & subcategory and update the article members.
        '''
        if section=="":
            article.category = "_Neclasificate"
            article.subcategory = ""
           
            print("      Articol neclasificat")
            print("        -> Denumire: " + article.title)
            print("        -> Cheie necunoscuta:" + self.GetMappingKey(article))  
        else:
            splitSection = section.split("#")
            if len(splitSection)!=2 :
                print("    EROARE: sectiunea [" + section + "] trebuie sa fie de forma [categorie#subcategorie]")
                sys.exit("   \nEROARE: Sectiune invalida in fisierul de mapare: [" + section + "] !!!")
            article.category = splitSection[0]
            article.subcategory = splitSection[1]
            #print("*** category:" + article.category + " subcategory:" + article.subcategory)
        
        return article
      
    def ComputeCategory(self, article):
        '''
        Computes the category for the current article.
        '''        
        section = self.FindSectionForKey(self.GetMappingKey(article), 
                                         self.parameters.categoryMap)  
        article = self.UpdateArticleBasedOnMappedSection(article, section)
        
        return article
        
    def ComputeAvailability(self, article):
        '''
        Computes the in-stock / out-of-stock status
        :param article: article used for computing.
        '''
        return "Active"
    
    def GenerateImageNameFromUrl(self, imageUrl):
        '''
        Converts the image url into our internal file naming. 
          e.g:
          url: http://www.supplieraddres.ro/image name.jpg
          returns: success: "image-name.jpg"
                   failure: "noimage.jpg" 
                   "" for empty url
        :param imageUrl:
        '''
        if imageUrl=="":
            return ""
        
        url = imageUrl.replace("\\", "/")
        path,filename = os.path.split(url)
        filename = filename.replace(" ", "-").replace("%20", "-")
               
        isBrokenPath = (filename=="" or path=="" or filename.rfind(".")==-1)               
        if isBrokenPath:
            return "noimage.jpg"      
        
        return filename
    
    def ComputeImages(self, article):
        '''
        Computes the images paths and names.
        :param article: article used for computing.
        '''
        for  i,imageUrl in  enumerate(article.imagesUrl):
            article.imagesNames[i] = self.GenerateImageNameFromUrl(imageUrl)
            article.imagesPaths[i] = self.GenerateImagePath(article, article.imagesNames[i])
            
        article.imageSmallName = self.GenerateSmallImageName(article.imagesNames[0])
        article.imageSmallPath = self.GenerateImagePath(article, article.imageSmallName)
        
    
        
    def ComputeDescription(self, article):
        '''
        Computes the  product description. Removes html format which might destroy the site aspect.
        :param article: article to be processed
        '''
        # Remove the product name from description
        description = article.description.replace(article.title, "")
        return DescriptionProcessor.CleanDescription(description)    
        
    def ConvertToOurFormat(self):
        '''
        Converts all data to our format
        '''
        for article in self.articleList:
            article.price        = self.ComputePrice(article)
            article.available    = self.ComputeAvailability(article)
            self.ComputeImages(article)
            
            article.description  = self.ComputeDescription(article)
            article = self.ComputeCategory(article)
    
    def GenerateImagePath(self, article, imageName):
        if imageName!="":
            return article.supplier + "/" + imageName
        else:
            return ""
    
    def GenerateSmallImageName(self, mainImageName):
        extension = mainImageName[mainImageName.rfind("."):]
        return mainImageName[:mainImageName.rfind(".")] + "_s" + extension

    
    def FilterBySupplier(self, supplier):
        
        filteredArticles = Articles(self.code, None, None, None)
        for article in self.articleList:
            if article.supplier == supplier:
                filteredArticles.Add1(article)
        
        return filteredArticles
      

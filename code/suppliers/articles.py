import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from code.article import Article
from code.pathbuilder import PathBuilder
from code.descriptionprocessor import DescriptionProcessor

import codecs
import csv
import os
import collections
#import urllib.request
import pdb
import logging
from _ast import Try
from bs4 import BeautifulSoup, NavigableString
import bleach
import re
#import requests
import configparser


class Articles(object):

    def __init__(self, code, paths, parameters, downloader):

        self.articleList = []
        self.code = self.getSupplierCode()
        self.paths = paths
        self.parameters = parameters
        self.downloader = downloader
        
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
    @staticmethod
    def getSupplierCode():
        raise NotImplementedError("Must override getSupplierCode")    
    
    
    def DownloadFeed(self):
        self.downloader.DownloadFeed(self.paths.feedFileNamePath,
                                     self.parameters.downloadUrl)         
            
    def ArticlesCount(self):
        return self.articleList.__len__()
    

    def DownloadAndSaveImage(self, imgUrl, imgSavePath1, imgSavePath2=""):
        self.downloader.DownloadAndSaveImage(imgUrl, imgSavePath1, imgSavePath2="")       
        
        
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
    def DownloadImages(self):
        self.downloader.DownloadImages(self.articleList)
       
       
    
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
        #traverse backwards: if we remove an element, the lower indexes are not affected  
        for article in reversed(self.articleList):
            #print('comparing: ' + str(article.id) )
            if article.supplier != supplier:
                self.articleList.remove(article)
    
    def RemoveInactiveArticles(self):
        #traverse backwards: if we remove an element, the lower indexes are not affected       
        for article in reversed(self.articleList):
            if article.available != "Active":
                self.articleList.remove(article)

    def IntersectWith(self, feed):
        '''
        Intersect the articles. The article items out of
        the intersection set are removed.
        '''                
        #we check elements backwards, from last element to first one
        #in this way, if we remove an element, the indexes for the
        #unchecked ones (which have a lower index) are not affected
        for i, art1 in reversed(list(enumerate(self.articleList))):
            found = False
            for art2 in feed.articleList:
                #print('comparing: ' + str(art1.id) + " with " + str(art2.id))
                if art1.IsSameArticle(art2):
                    found = True
                    break
            if found == False:
                #print("removing art " + str(art1.id))
                self.articleList.pop(i)

        #print("articles after intersection: ")
        #for art1 in self.articleList:
        #    print(" " + str(art1.id))


    def RemoveArticlesWithNoUpdatesComparedToReference(self, reference):
        for i, art1 in reversed(list(enumerate(self.articleList))):
            for art2 in reference.articleList:    
                if art1.IsSameArticle(art2):
                    hasNoUpdates = art1.price==art2.price and art1.available==art2.available
                    
                    if hasNoUpdates:
                        self.articleList.pop(i)
                    break

    def GetComparisonHumanReadableMessages(self, reference):
        messages=collections.OrderedDict()
        for i, art1 in reversed(list(enumerate(self.articleList))):
            for art2 in reference.articleList:
                if art1.IsSameArticle(art2):                
                    msg = ""
                    
                    if art1.price!=art2.price:
                        msg = msg + " pret " + str(art1.price) + "=/=" + str(art2.price) 
                    
                    if art1.available!=art2.available:
                        msg = msg + " stoc " + str(art1.available) + "=/=" + str(art2.available)

                    if art1.price==art2.price and art1.available==art2.available:
                        msg = msg + " articole identice ca pret si disponibilitate"

                    messages.update([(str(art1.id), msg)])
                    break
        return messages
                       
        

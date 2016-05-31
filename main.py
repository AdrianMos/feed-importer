'''
Created on 26.04.2014

@author: Adrian Raul Mos
'''
import os.path
import sys
import logging
#from _stat import filemode
#add the current folder to the python paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from article import Article
#from haiducel.articles import Articles
from articles import *
#from haiducel.articles import HaiducelArticles
from export import Export
from operations import Operations
from pathbuilder import PathBuilder
import time


def AskUserYesOrNo(question):
    '''
    Displays the question to the user and waits for a yes or no answer (y/n).
    '''
    userInput=""
    print('')
    while (userInput!="da" and userInput!="nu"):
        userInput = input(question + ' da/nu: >> ').lower()
    return userInput



def main():
    print("*******************************************")
    print("*** Actualizare date magazinul Haiducel ***")
    print("*******************************************")
    print("Adrian Mos, V 3.3, 01.06.2016\n")
    
    
    try:
        
        while True:
            print("Optiuni disponibile:")
            print("  1. Iesire\n"
                  "  2. Actualizare Nancy (NAN)\n"
                  "  3. Actualizare BabyDreams (HDRE)\n" 
                  "  4. Actualizare Bebex (BEB)\n"
                  "  5. Actualizare BebeBrands (HBBA)\n"
                  "  6. Actualizare BabyShops (HMER)\n"
                  "  7. Actualizare KidsDecor (HDEC) - nu merge, caractere ilegale in feed, feed-nu se descarca\n"
                  "  8. Actualizare Hubners (HHUB)\n"
                  )
            userInput = input('Introduceti numarul optiunii pentru a continua: >> ')
            
            if userInput=="1":
                sys.exit("Program terminat.")
                break
            elif userInput=="2":
                feed = NANArticles("NAN")    
                break
            elif userInput=="3":
                feed = HDREArticles("HDRE")
                break
            elif userInput=="4":
                feed = BEBArticles("BEB")
                break
            elif userInput=="5":
                feed = BebeBrandsArticles("HBBA")
                break
            elif userInput=="6":
                feed = BabyShopsArticles("HMER")
                break
            elif userInput=="7":
                feed = KidsDecorArticles("HDEC")
                break
            elif userInput=="8":
                feed = HubnersArticles("HHUB")
                break
            else:
                sys.exit("Optiune invalida. Program terminat.")
        
                
        print("  Procesare articole de tipul " + feed.__class__.__name__ + '.')
        
        # Configure the error log file.
        logging.basicConfig(filename=os.path.join(feed.code, 'erori ' + feed.code + '.log'),
                            level=logging.INFO,filemode='w',
                            format='%(asctime)s     %(message)s')
                  
        if AskUserYesOrNo('Descarc date noi pentru acest furnizor?') == 'da':    
            feed.DownloadFeed()
        
        print("\n*** Import date din feed " + feed.code)
        eroriImport = feed.Import()     
        
        print("\n*** Articole exportate pentru magazinul online")
        export2 = Export();
        fileShop = feed.code + "/out/" + feed.code + ' Onlineshop ' + time.strftime("%Y-%m-%d") + '.csv'
        export2.ExportDataForOnlineshop(feed, fileShop)		
    
        feed.ConvertToOurFormat()
        print("    Articole importate: "+ str(feed.articleList.__len__()) + ". Erori: " + str(eroriImport))
        
        if feed.articleList.__len__() < 50:
            logging.error('ATENTIE: Posibila eroare in datele furnizorului. Exista mai putin de 50 de articole.')
            if AskUserYesOrNo('    ATENTIE:\n    Posibila eroare in datele furnizorului.\n    Exista mai putin de 50 de articole. Continuati?') == 'nu':    
                sys.exit("Ati renuntat la procesare.")
        
        
        feed.RemoveCrapArticles()
        print("    Articole importate, dupa eliminare: "+ str(feed.articleList.__len__()))
        
        print("\n*** Import articole din baza de date Haiducel, distribuitor " + feed.code)
        haiducelArticles = HaiducelArticles("Haiducel")
        haiducelArticles.Import()
        haiducelArticlesFiltered = haiducelArticles.FilterBySupplier(feed.code)
        print("    Articole importate: "+ str(haiducelArticlesFiltered.articleList.__len__()))
        
        
        print("\n************ COMPARARI ************")
        
        print("\n*** Articole existente")
        updatedArticles, updateMessages = Operations.ExtractUpdatedArticles(haiducelArticlesFiltered, feed)
        # Set the saving paths & code for the updated articles identical to the supplier's paths
        # The updated articles belong to the supplier.
        updatedArticles.paths = feed.paths    
        print("    Articole actualizate: "+ str(updateMessages.__len__())) 
        export1 = Export()
        filenameArticlesToUpdate = feed.code + "/out/" + feed.code + ' articole existente cu modificari in pret sau status ' + time.strftime("%Y-%m-%d") + '.csv'
        export1.ExportPriceAndAvailabilityAndMessages(updatedArticles, updateMessages, filenameArticlesToUpdate)
        
        print("\n*** Articole noi active")
        newArticles = Operations.SubstractArticles(feed, haiducelArticlesFiltered)
        newArticles = Operations.RemoveUnavailableArticles(newArticles)
        newArticles.paths = feed.paths
        filenamenewArticles = feed.code + "/out/" + feed.code + ' articole noi ' + time.strftime("%Y-%m-%d") + '.csv'
        print("    Articole noi in feed: " + str(newArticles.articleList.__len__()))
        export1.ExportAllData(newArticles, filenamenewArticles)
        
        print("\n*** Toate articolele din feed transformate in formatul nostru")
        filenamefeedOurFormat = feed.code + "/out/" + feed.code + ' original ' + time.strftime("%Y-%m-%d") + '.csv'
        export1.ExportAllData(feed, filenamefeedOurFormat)		
        
        print("\n*** Articole sterse din feed")
        removedArticles = Operations.SubstractArticles(haiducelArticlesFiltered, feed)
        filenameArticlesToRemove = feed.code + "/out/" + feed.code + ' articole de sters ' + time.strftime("%Y-%m-%d") + '.csv'
        print("    Articole ce nu mai exista in feed: " + str(removedArticles.articleList.__len__()))
        export1.ExportArticlesForDeletion (removedArticles, filenameArticlesToRemove)
        
        if eroriImport > 0:
            print("\n\n***    Au fost gasite "+ str(eroriImport) + " ERORI in feed. Exista articole neimportate. ANUNTATI distribuitorul. Detalii in log.")
        
        if AskUserYesOrNo('Descarc imaginile pentru articolele noi?') == 'da':
            newArticles.DownloadImages();  
            
    except Exception as ex:
        print("\n\n Eroare: " + repr(ex) + "\n")
        logging.error("main: " + repr(ex))
      
   
    userInput = input('\nApasati enter pentru iesire. >> ')
    print("\n*** Program terminat ***")
    
    
    
    
    
    '''
    articles = BabyDreamsArticles()
    
    articles.Import()
    articles.CheckForDuplicity()
    articles.ComputePrices()
    articles.ComputeAvailability()
    articles.ComputeCategory()
                   --> read mappings from file
                   
    articles.ComputeDescription()
    articles.ComputeImagePaths()
    
    articles.SaveNewArticles()
    articles.SaveUpdatedArticles()
    '''
    
    
    
    
    '''
    articlesDummy1 = Articles()
    articlesDummy1.Add("5", "item2  ", 15, "Inactive", "category1", "NAN")
    articlesDummy1.Add("2", "item1", 10, "Active", "category1", "NAN")
    articlesDummy1.Add("3", "item2", 10, "Active", "category1", "NAN")
    
    articlesDummy2 = Articles()
    articlesDummy2.Add("2", "item1", 10, "Inactive", "category1", "NAN")
    articlesDummy2.Add("5", "item2", 10, "Active", "category1", "NAN")
    articlesDummy2.Add("3", "item2", 20, "Active", "category1", "NAN")
    '''



if __name__ == '__main__':
    main()

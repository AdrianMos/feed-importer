'''
Created on 26.04.2014

@author: Adrian Raul Mos
'''
import os.path
import sys
import logging
#add the current folder to the python paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from userinterface import UserInterface
from factory import Factory
from export import Export
from operations import Operations
import time

export = Export()

def main():
    factory = Factory()
    user = UserInterface()


    user.DisplayHeader()
    
    try:
        
        user.DisplayOptions()
        userInput = user.AskInput('Introduceti numarul optiunii: >> ')
        if userInput == "1": 
            sys.exit("Program terminat.")
        
        feed = factory.CreateSupplierFeedObject(userInput)
        if feed is None: 
            sys.exit("Optiune invalida. Program terminat.")
        
        InitLogFile(feed.code)
        
        print("  Procesare articole de tipul " + 
              feed.__class__.__name__ + '.')
        
       
                  
        if user.AskYesOrNo('Descarc date noi pentru acest furnizor?') == 'da':    
            feed.DownloadFeed()
        
        
        print("\n\n(1)--------- IMPORT DATE FEED --------")
        
        print("\n    Feed de la distributor: " + feed.code)
        errors = feed.Import()   
        
        if errors > 0:
            print("\n\n***    Au fost gasite "+ str(errors) + 
                  " ERORI in feed. Exista articole neimportate. " + 
                  "ANUNTATI distribuitorul. Detalii in log.")  
        
        feed.ConvertToOurFormat()
        print("    Articole importate: " + str(feed.ArticlesCount()) + ". " + 
              "Erori: " + str(errors))
        
        if feed.ArticlesCount() < 50:
            logging.error('ATENTIE: Posibila eroare in datele furnizorului.'+
                          ' Exista mai putin de 50 de articole.')
            
            if user.AskYesOrNo('    ATENTIE:\n    Posibila eroare in datele' +
                               ' furnizorului.\n    Exista mai putin de 50' + 
                               ' de articole. Continuati?') == 'nu':    
                sys.exit("Ati renuntat la procesare.")

        print("\n--------------------------------------\n\n")        
        
        
        
        print("\n\n(2)-- SALVARE FEED  FORMAT STANDARD --\n")

        filename = GenerateOutputFilename('Onlineshop', feed.code)
        export.ExportDataForOnlineshop(feed, filename)

        print("\n--------------------------------------\n\n")
        

      
        print("\n\n(3)---------- CURATARE FEED ----------\n")

        feed.RemoveCrapArticles()
        print("    Articole importate, dupa eliminare: " + 
               str(feed.ArticlesCount()))

        print("\n--------------------------------------\n\n")
        
        
        
        print("\n\n(4)------ IMPORT DATE HAIDUCEL -------\n")
        
        print("    Filtru distribuitor: " + feed.code)
        haiducelAllArticles = factory.CreateHaiducelFeedObject()
        haiducelAllArticles.Import()
        haiducelFiltered = haiducelAllArticles.FilterBySupplier(feed.code)
        print("    Articole importate: " + 
              str(haiducelFiltered.ArticlesCount()))
        
        print("\n--------------------------------------\n\n")
        
        
        
        print("\n(5)------------ COMPARARI ------------")
        
        print("\n\nARTICOLE MODIFICATE")
        ProcessUpdatedArticles(haiducelFiltered, feed)
        
        print("\n\nARTICOLE NOI")
        newArticles = ProcessNewArticles(haiducelFiltered, feed)

        print("\n\nARTICOLE STERSE")
        ProcessArticlesForDeletion(haiducelFiltered, feed)
        
        print("\n--------------------------------------\n\n")
        
        
        
        print("\n(6)----- DESCARCARE IMAGINI NOI ------")
        
        if user.AskYesOrNo('Descarc imaginile pentru articolele noi?') == 'da':
            newArticles.DownloadImages();  
        
        print("\n--------------------------------------\n\n")
            
            
            
    except Exception as ex:
        print("\n\n Eroare: " + repr(ex) + "\n")
        logging.error("main: " + repr(ex))
      
   
    user.AskInput('\nApasati enter pentru iesire. >> ')
    print("\n*** Program terminat ***")


def ProcessUpdatedArticles (haiducelFeed, supplierFeed):
    
    updatedArticles, updateMessages = Operations.ExtractUpdatedArticles(
                                                     haiducelFeed,
                                                     supplierFeed)
    # Set the saving paths & code for the updated articles identical to 
    # the supplier's paths
    # The updated articles belong to the supplier.
    updatedArticles.paths = supplierFeed.paths    
    print("    Articole actualizate: "+ str(updateMessages.__len__())) 

    filename = GenerateOutputFilename('articole existente cu' + 
                                      ' pret sau status modificat',
                                      supplierFeed.code)
    export.ExportPriceAndAvailabilityAndMessages(updatedArticles, 
                                                  updateMessages, 
                                                  filename)
    return updatedArticles

def ProcessArticlesForDeletion (haiducelFeed, supplierFeed):
    
    removedArticles = Operations.SubstractArticles(haiducelFeed, supplierFeed)
    
    print("    Articole ce nu mai exista in feed: " + 
          str(removedArticles.ArticlesCount()))
    export.ExportArticlesForDeletion(
                removedArticles,
                GenerateOutputFilename('articole de sters', supplierFeed.code))
    return removedArticles

def ProcessNewArticles (haiducelFeed, supplierFeed):
    
    newArticles = Operations.SubstractArticles(supplierFeed, haiducelFeed)
    newArticles = Operations.RemoveUnavailableArticles(newArticles)
    newArticles.paths = supplierFeed.paths
    print("    Articole noi in feed: " + 
          str(newArticles.ArticlesCount()))
    export.ExportAllData(
                newArticles, 
                GenerateOutputFilename('articole noi', supplierFeed.code))
    return newArticles

def GenerateOutputFilename(name, code):
    return (code
            + "/out/" 
            + code 
            + ' ' + name + ' ' 
            + time.strftime("%Y-%m-%d")
            + '.csv')

def InitLogFile(code):
    filename = os.path.join(code, 'erori ' + code + '.log')
    logging.basicConfig(filename = filename,
                        level = logging.INFO, 
                        filemode = 'w',
                        format ='%(asctime)s     %(message)s')

if __name__ == '__main__':
    main()

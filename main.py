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
        
        print("  Procesare articole de tipul " + feed.__class__.__name__ + '.')
        
       
                  
        if user.AskYesOrNo('Descarc date noi pentru acest furnizor?') == 'da':    
            feed.DownloadFeed()
        
        
        print("\n*** Import date din feed " + feed.code)
        errors = feed.Import()     
        
        #TODO(AdrianMos): check if needed
        print("\n*** Articole exportate pentru magazinul online")
        export2 = Export();
        export2.ExportDataForOnlineshop(
                    feed,
                    GenerateOutputFilename('Onlineshop', feed.code))		
    
    
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
        
        
        feed.RemoveCrapArticles()
        print("    Articole importate, dupa eliminare: " + 
               str(feed.ArticlesCount()))
        
        print("\n*** Import articole din baza de date Haiducel, " + 
              "distribuitor " + feed.code)
        haiducelAllArticles = factory.CreateHaiducelFeedObject()
        haiducelAllArticles.Import()
        haiducelFiltered = haiducelAllArticles.FilterBySupplier(feed.code)
        print("    Articole importate: "+ str(haiducelFiltered.ArticlesCount()))
        
        
        
        
        print("\n************ COMPARARI ************")
        
        print("\n*** Articole existente")
        updatedArticles, updateMessages = Operations.ExtractUpdatedArticles(
                                                         haiducelFiltered,
                                                         feed)
        # Set the saving paths & code for the updated articles identical to the supplier's paths
        # The updated articles belong to the supplier.
        updatedArticles.paths = feed.paths    
        print("    Articole actualizate: "+ str(updateMessages.__len__())) 
        export1 = Export()
        filename = GenerateOutputFilename('articole existente cu modificari'
                                          ' in pret sau status',
                                          feed.code)
        export1.ExportPriceAndAvailabilityAndMessages(updatedArticles, 
                                                      updateMessages, 
                                                      filename)
        
        
        print("\n*** Articole noi active")
        newArticles = Operations.SubstractArticles(feed, haiducelFiltered)
        newArticles = Operations.RemoveUnavailableArticles(newArticles)
        newArticles.paths = feed.paths
        print("    Articole noi in feed: " + 
              str(newArticles.ArticlesCount()))
        export1.ExportAllData(
                    newArticles, 
                    GenerateOutputFilename('articole noi', feed.code))
        
        #TODO(AdrianMos): check if needed
        print("\n*** Toate articolele din feed convertite in formatul nostru")
        export1.ExportAllData(
                    feed, 
                    GenerateOutputFilename('original', feed.code))		

        
        print("\n*** Articole sterse din feed")
        removedArticles = Operations.SubstractArticles(haiducelFiltered, feed)
                                                      
                                                      
        print("    Articole ce nu mai exista in feed: " + 
              str(removedArticles.ArticlesCount()))
        export1.ExportArticlesForDeletion(
                    removedArticles,
                    GenerateOutputFilename('articole de sters', feed.code))
        
        
        if errors > 0:
            print("\n\n***    Au fost gasite "+ str(errors) + 
                  " ERORI in feed. Exista articole neimportate. " + 
                  "ANUNTATI distribuitorul. Detalii in log.")
        
        if user.AskYesOrNo('Descarc imaginile pentru articolele noi?') == 'da':
            newArticles.DownloadImages();  
            
    except Exception as ex:
        print("\n\n Eroare: " + repr(ex) + "\n")
        logging.error("main: " + repr(ex))
      
   
    user.AskInput('\nApasati enter pentru iesire. >> ')
    print("\n*** Program terminat ***")


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

'''
Created on 26.04.2014

@author: Adrian Raul Mos
'''
import os.path
import sys
import logging

from code.userinterface import UserInterface
from code.factory import Factory
from code.export import Export
from code.operations import Operations
from code.pathbuilder import PathBuilder
from code.messages import *
from code.menu import Menu
from code.suppliers.articles import *

export = Export()

def exitApp(data):
    print("... bye")
    sys.exit(0)

def myFunc1(data):
    print("...hello " + str(data))
    return None

def constructMenu():
    menu = Menu(title = "Optiuni disponibile:",
                userMessage = 'Introduceti numarul optiunii:')
    menu.addMenuItem(name="Iesire", callback=exitApp, arguments="")
    menu.addMenuItem(name="Actualizare Nancy (NAN)",  callback=Factory.CreateSupplierFeedObject, arguments="ArticlesNancy")
    menu.addMenuItem(name="Actualizare BabyDreams (HDRE)",  callback=Factory.CreateSupplierFeedObject, arguments="ArticlesBabyDreams")
    
    menu.addMenuItem(name="dummy",  callback=myFunc1, arguments="yellow")
    return menu


def main():
    #factory = Factory()
    user = UserInterface()

    user.DisplayHeader()


    menu = constructMenu()
    feed = menu.openMenu()

    if isinstance(feed, Articles):
        print("YES it's an instance")
    else:
        print("NO it's not an instance")
        sys.exit('..bye bye')
    try:
        
        user.DisplayOptions()
##        userInput = user.AskInput('Introduceti numarul optiunii: >> ')
##        if userInput == '1': 
##            print('Program terminat.')
##            sys.exit('Program terminat.')
        
        
##        code = user.GetCodeForOption(userInput)
##        if code is None:
##            print('Optiune invalida. Program terminat.')
##            sys.exit('Optiune invalida. Program terminat.')
         
##        feed = factory.CreateSupplierFeedObject(code)
##        if feed is None:
##            print('Optiune invalida. Program terminat.')
##            sys.exit('Optiune invalida. Program terminat.')
        
        InitLogFile(feed.code)
        
        
        print('  Procesare articole de tipul ' +
              feed.__class__.__name__ + '.')

                
        if user.AskYesOrNo('Descarc date noi pentru acest furnizor?') == 'da':
            feed.DownloadFeed(feed.credentials)
        
        
        user.Title(' IMPORT DATE FEED ')
        print('\n    Feed de la distributor: ' + feed.code)
        errors = feed.Import()
        if errors > 0:
            print(MSG_FEED_ERRORS + str(errors))
        
        feed.ConvertToOurFormat()
        print('    Articole importate: ' + str(feed.ArticlesCount()) + '. ')

       
        if feed.ArticlesCount() < 50:
            logging.error(MSG_WARNING_LESS_50_ARTICLES)
            
            if user.AskYesOrNo(MSG_WARNING_LESS_50_ARTICLES +
                               ' Continuati?') == 'nu':
                sys.exit('Ati renuntat la procesare.')
        user.HorizontalLine()
        
        
        user.Title(' SALVARE FEED FORMAT STANDARD ')
        filename = PathBuilder.getOutputPath('Onlineshop', feed.code)
        export.ExportDataForOnlineshop(feed, filename)
        user.HorizontalLine()
        
        
        user.Title(' CURATARE FEED ')
        feed.RemoveCrapArticles()
        print('    Articole importate, dupa eliminare: ' + 
               str(feed.ArticlesCount()))
        user.HorizontalLine()
        
        
        user.Title(' IMPORT DATE HAIDUCEL ')
        print('    Filtru distribuitor: ' + feed.code)
        haiducelAllArticles = Factory.CreateHaiducelFeedObject()
        haiducelAllArticles.Import()
        haiducelFiltered = haiducelAllArticles.FilterBySupplier(feed.code)
        print('    Articole importate: ' + str(haiducelFiltered.ArticlesCount()))
        user.HorizontalLine()
        
        user.Title(' COMPARARI ')
        print('\n\nARTICOLE MODIFICATE')
        ProcessUpdatedArticles(haiducelFiltered, feed)
        
        print('\n\nARTICOLE NOI')
        newArticles = ProcessNewArticles(haiducelFiltered, feed)

        print('\n\nARTICOLE STERSE')
        ProcessArticlesForDeletion(haiducelFiltered, feed)
        user.HorizontalLine()
        
        
        user.Title(' DESCARCARE IMAGINI NOI ')
        if user.AskYesOrNo('Descarc imaginile pentru articolele noi?') == 'da':
            newArticles.DownloadImages(feed.credentials);  
        user.HorizontalLine()
            
            
    except Exception as ex:
        print('\n\n Eroare: ' + repr(ex) + '\n')
        logging.error('main: ' + repr(ex))
      
   
    user.AskInput('\nApasati enter pentru iesire. >> ')
    print('\n*** Program terminat ***')


def ProcessUpdatedArticles (haiducelFeed, supplierFeed):
    
    updatedArticles, updateMessages = Operations.ExtractUpdatedArticles(
                                                     haiducelFeed,
                                                     supplierFeed)
    # Set the saving paths & code for the updated articles identical to 
    # the supplier's paths
    # The updated articles belong to the supplier.
    updatedArticles.paths = supplierFeed.paths    
    print('    Articole actualizate: '+ str(updateMessages.__len__())) 

    outFile = PathBuilder.getOutputPath('articole existente cu' + 
                                        ' pret sau status modificat',
                                        supplierFeed.code)
    export.ExportPriceAndAvailabilityAndMessages(updatedArticles, 
                                                 updateMessages, 
                                                 outFile)
    return updatedArticles

    
def ProcessArticlesForDeletion (haiducelFeed, supplierFeed):
    
    removedArticles = Operations.SubstractArticles(haiducelFeed, supplierFeed)
    
    print('    Articole ce nu mai exista in feed: ' + 
          str(removedArticles.ArticlesCount()))
    outFile = PathBuilder.getOutputPath('articole de sters', supplierFeed.code)
    export.ExportArticlesForDeletion(
                removedArticles,
                outFile)
    return removedArticles

    
def ProcessNewArticles (haiducelFeed, supplierFeed):
    
    newArticles = Operations.SubstractArticles(supplierFeed, haiducelFeed)
    newArticles = Operations.RemoveUnavailableArticles(newArticles)
    newArticles.paths = supplierFeed.paths
    print('    Articole noi in feed: ' +  str(newArticles.ArticlesCount()))
    outFile = PathBuilder.getOutputPath('articole noi', supplierFeed.code)
    export.ExportAllData(newArticles,  outFile)
    return newArticles
    
def InitLogFile(code):
    filename = PathBuilder.getLogPath(code)
    logging.basicConfig(filename = filename,
                        level = logging.INFO, 
                        filemode = 'w',
                        format ='%(asctime)s     %(message)s')

if __name__ == '__main__':
    main()

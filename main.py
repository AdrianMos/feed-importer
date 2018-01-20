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
import copy

export = Export()


def main():
    user = UserInterface()
    user.DisplayHeader()

    menu = builMenu()
    feed = menu.openMenu()

    if isinstance(feed, Articles):
        print("YES it's an instance")
    else:
        print("NO it's not an instance")
        sys.exit('..bye bye')
    try:
        
        user.DisplayOptions()
        
        InitLogFile(feed.code)
        
        
        print('  Procesare articole de tipul ' +
              feed.__class__.__name__ + '.')

                
        if user.AskYesOrNo('Descarc date noi pentru acest furnizor?') == 'da':
            feed.DownloadFeed()       
        
        
        user.Title(' IMPORT DATE FEED ')
        print('\n    Feed de la distributor: ' + feed.code)
        feed.Import()
        #errors = feed.Import()
        #if errors > 0:
        #    print(MSG_FEED_ERRORS + str(errors))
        
        feed.ConvertToOurFormat()
        print('    Articole importate: ' + str(feed.ArticlesCount()) + '. ')

       
        if feed.ArticlesCount() < 50:
            logging.error(MSG_WARNING_LESS_50_ARTICLES)
            
            if user.AskYesOrNo(MSG_WARNING_LESS_50_ARTICLES + ' Continuati?') == 'nu':
                sys.exit('Ati renuntat la procesare.')
        user.HorizontalLine()
        
        
        user.Title(' SALVARE FEED FORMAT STANDARD ')
        filename = PathBuilder.getOutputPath('Onlineshop', feed.code)
        export.ExportDataForOnlineshop(feed, filename)
        user.HorizontalLine()
        
        
        user.Title(' CURATARE FEED ')
        feed.RemoveCrapArticles()
        print('    Articole importate, dupa eliminare: ' + str(feed.ArticlesCount()))
        user.HorizontalLine()
        
        
        user.Title(' IMPORT DATE HAIDUCEL ')
        print('    Filtru distribuitor: ' + feed.code)
        databaseFeed = Factory.CreateHaiducelFeedObject()
        databaseFeed.Import()
        print("5.1  - count:" + str(len(databaseFeed.articleList)))

        
        databaseFeed.FilterBySupplier(feed.code)
        print('    Articole importate: ' + str(databaseFeed.ArticlesCount()))
        user.HorizontalLine()
        
        user.Title(' COMPARARI ')
        print('\n\nARTICOLE MODIFICATE')
        ProcessUpdatedArticles(databaseFeed, feed)
        
        print('\n\nARTICOLE NOI')
        newArticles = ProcessNewArticles(databaseFeed, feed)

        print('\n\nARTICOLE STERSE')
        ProcessArticlesForDeletion(databaseFeed, feed)
        user.HorizontalLine()
        
        
        user.Title(' DESCARCARE IMAGINI NOI ')
        if user.AskYesOrNo('Descarc imaginile pentru articolele noi?') == 'da':
            newArticles.DownloadImages();  
        user.HorizontalLine()
            
            
    except Exception as ex:
        print('\n\n Eroare: ' + repr(ex) + '\n')
        logging.error('main: ' + repr(ex))
      
   
    user.AskInput('\nApasati enter pentru iesire. >> ')
    print('\n*** Program terminat ***')


def ProcessUpdatedArticles (haiducelFeed, supplierFeed):
    
    supplierFeedCopy = copy.deepcopy(supplierFeed)
    supplierFeedCopy.IntersectWith(haiducelFeed)
    supplierFeedCopy.RemoveArticlesWithNoUpdatesComparedToReference(reference=haiducelFeed)

    messagesList = supplierFeedCopy.GetComparisonHumanReadableMessages(reference=haiducelFeed)

            
    print('    Articole actualizate: '+ str(supplierFeedCopy.ArticlesCount())) 
    outFile = PathBuilder.getOutputPath('articole existente cu pret sau status modificat',
                                        supplierFeedCopy.code)
    export.ExportPriceAndAvailabilityAndMessages(supplierFeedCopy, 
                                                 messagesList, 
                                                 outFile)
    
    
def ProcessArticlesForDeletion (haiducelFeed, supplierFeed):
    
    removedArticles = Operations.SubstractArticles(haiducelFeed, supplierFeed)
    
    print('    Articole ce nu mai exista in feed: ' + str(removedArticles.ArticlesCount()))
    outFile = PathBuilder.getOutputPath('articole de sters', supplierFeed.code)
    export.ExportArticlesForDeletion(removedArticles,
                                     outFile)
    return removedArticles

    
def ProcessNewArticles (haiducelFeed, supplierFeed):
    
    newArticles = Operations.SubstractArticles(supplierFeed, haiducelFeed)
    newArticles.RemoveInactiveArticles()

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

def exitApp(data):
    print("... bye")
    sys.exit(0)


def builMenu():
    menu = Menu(title = "Optiuni disponibile:",
                userMessage = 'Alegeti:')
    menu.addMenuItem(name="Iesire",
                     callback=exitApp,
                     arguments="")

    suppliers = [["Actualizare Nancy (NAN) ok",        "ArticlesNancy"],
                 ["Actualizare BabyDreams (HDRE)",     "ArticlesBabyDreams"],
                 ["Actualizare Bebex (BEB)",           "ArticlesBebex"],
                 ["Actualizare BebeBrands (HBBA) ok",  "ArticlesBebeBrands"],
                 ["Actualizare BabyShops (HMER)",      "ArticlesBabyShops"],
                 ["Actualizare KidsDecor (HDEC)",      "ArticlesKidsDecor"],
                 ["Actualizare Hubners (HHUB) ok",     "ArticlesHubners"]]

    for supplier in suppliers:
        menu.addMenuItem(name = supplier[0],
                         callback = Factory.CreateSupplierFeedObject,
                         arguments = supplier[1])
        
    return menu
                        
if __name__ == '__main__':
    main()

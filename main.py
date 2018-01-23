'''
Created on 26.04.2014

@author: Adrian Raul Mos
'''
import os.path, sys, logging, copy

from code.userinterface import UserInterface
from code.factory import Factory
from code.export import Export
from code.messages import *
from code.menu import Menu
from code.suppliers.articles import *


export = Export()


def main():
    user = UserInterface()
    user.DisplayHeader()

    menu = builMenu()
    supplier = menu.openMenu()

    if isinstance(supplier, Articles):
        print("YES it's an instance")
    else:
        print("NO it's not an instance")
        sys.exit('..bye bye')
    try:
                
        InitLogFile(supplier)
        
                
        if user.AskYesOrNo('Descarc date noi pentru acest furnizor?') == 'da':
            supplier.DownloadFeed()       
        
        
        user.Title(' IMPORT DATE FEED ')
        print('\n    Feed de la distributor: ' + supplier.code)
        #supplier.Import()
        numErrors = supplier.Import()
        if numErrors > 0:
            print(MSG_FEED_ERRORS + str(errors))
        
        supplier.ConvertToOurFormat()
        print('    Articole importate: ' + str(supplier.ArticlesCount()) + '. ')

       
        if supplier.ArticlesCount() < 50:
            logging.error(MSG_WARNING_LESS_50_ARTICLES)
            
            if user.AskYesOrNo(MSG_WARNING_LESS_50_ARTICLES + ' Continuati?') == 'nu':
                sys.exit('Ati renuntat la procesare.')
        user.HorizontalLine()
        
        
        user.Title(' SALVARE FEED FORMAT STANDARD ')
        export.ExportDataForOnlineshop(supplier, supplier.paths.getSupplierFeedExportFile())
        user.HorizontalLine()
        
        
        user.Title(' CURATARE FEED ')
        supplier.RemoveCrapArticles()
        print('    Articole importate, dupa eliminare: ' + str(supplier.ArticlesCount()))
        user.HorizontalLine()
        
        
        user.Title(' IMPORT DATE HAIDUCEL ')
        print('    Filtru distribuitor: ' + supplier.code)
        
        shopData = Factory.CreateFeedObjectForShop()
        shopData.Import()
        shopData.FilterBySupplier(supplier.code)
        
        print('    Articole importate: ' + str(shopData.ArticlesCount()))
        user.HorizontalLine()
        
        user.Title(' COMPARARI ')
        print('\n\nARTICOLE MODIFICATE')
        ProcessUpdatedArticles(shopData, supplier)
        
        print('\n\nARTICOLE NOI')
        newArticles = ProcessNewArticles(shopData, supplier)

        print('\n\nARTICOLE STERSE')
        ProcessArticlesForDeletion(shopData, supplier)
        user.HorizontalLine()
        
        
        user.Title(' DESCARCARE IMAGINI NOI ')
        if user.AskYesOrNo('Descarc imaginile pentru '
                           + str(newArticles.ArticlesCount())
                           + ' articole noi?') == 'da':
            newArticles.DownloadImages();  
        user.HorizontalLine()
            
            
    except Exception as ex:
        print('\n\n Eroare: ' + repr(ex) + '\n')
        logging.error('main: ' + repr(ex))
      
   
    user.AskInput('\nApasati enter pentru iesire. >> ')
    print('\n*** Program terminat ***')


def ProcessUpdatedArticles (shopData, supplier):
    
    supplierCopy = copy.deepcopy(supplier)
    supplierCopy.IntersectWith(shopData)
    supplierCopy.RemoveArticlesWithNoUpdatesComparedToReference(reference=shopData)

    messagesList = supplierCopy.GetComparisonHumanReadableMessages(reference=shopData)

    print('    Articole actualizate: '+ str(supplierCopy.ArticlesCount())) 
    export.ExportPriceAndAvailabilityAndMessages(supplierCopy, 
                                                 messagesList, 
                                                 supplier.paths.getUpdatedArticlesFile())
    
    
def ProcessArticlesForDeletion (shopData, supplier):
    
    articlesToDelete = copy.deepcopy(shopData)
    articlesToDelete.RemoveArticles(supplier)
       
    print('    Articole ce nu mai exista in feed: ' + str(articlesToDelete.ArticlesCount()))
    export.ExportArticlesForDeletion(articlesToDelete,
                                     supplier.paths.getDeletedArticlesFile())
    


def ProcessNewArticles (shopData, supplier):
    
    newArticles = copy.deepcopy(supplier)
    newArticles.RemoveArticles(shopData)
    newArticles.RemoveInactiveArticles()

    print('    Articole noi in feed: ' +  str(newArticles.ArticlesCount()))
    export.ExportAllData(newArticles,  supplier.paths.getNewArticlesFile())
    return newArticles
    
def InitLogFile(supplier): 
    logging.basicConfig(filename = supplier.paths.getLogFile(),
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

    items = [["Actualizare Nancy (NAN) ok",        "ArticlesNancy"],
             ["Actualizare BabyDreams (HDRE)",     "ArticlesBabyDreams"],
             ["Actualizare Bebex (BEB)",           "ArticlesBebex"],
             ["Actualizare BebeBrands (HBBA) ok",  "ArticlesBebeBrands"],
             ["Actualizare BabyShops (HMER)",      "ArticlesBabyShops"],
             ["Actualizare KidsDecor (HDEC)",      "ArticlesKidsDecor"],
             ["Actualizare Hubners (HHUB) ok",     "ArticlesHubners"]]

    for item in items:
        menu.addMenuItem(name = item[0],
                         callback = Factory.CreateSupplierFeedObject,
                         arguments = item[1])
        
    return menu
                        
if __name__ == '__main__':
    main()

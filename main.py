import os.path, sys, logging, copy

from code.userinterface import UserInterface
from code.factory import Factory
from code.export import Export
from code.messages import *
from code.menu import Menu
from code.suppliers.articles import *


export = Export()

 
def main():
    ui = UserInterface()
    ui.DisplayHeader()

    menu = builMenu()
    #the menu callback creates the supplier feed object
    #according to the user selection
    supplier = menu.openMenu()

    if not isinstance(supplier, Articles):
        print("Error: the menu callback doesn't create an Articles instance")
        sys.exit(0)
        
    try:       
        LogInit(supplier)

        ui.Title(TITLE_IMPORT_SUPPLIER_DATA)
        GetSupplierData(ui, supplier)
        ui.HorizontalLine()
            
        
        ui.Title(TITLE_EXPORT_STANDARD_FORMAT)
        export.ExportDataForOnlineshop(supplier, supplier.paths.getSupplierFeedExportFile())
        ui.HorizontalLine()
        
        
        ui.Title(TITLE_REMOVE_IRELEVANT_ARTICLES)
        supplier.RemoveCrapArticles()
        print('    Numar articole: ' + str(supplier.ArticlesCount()))
        ui.HorizontalLine()
        
        
        ui.Title(TITLE_IMPORT_SHOP_DATA)      
        shopData = Factory.CreateFeedObjectForShop()
        shopData.Import()
        shopData.FilterBySupplier(supplier.code)
        print('    Numar articole: ' + str(shopData.ArticlesCount()))
        ui.HorizontalLine()

        
        ui.Title(TITLE_COMPARING_SHOP_AND_SUPPLIER_DATA)
        ProcessUpdatedArticles(shopData, supplier)
        newArticles = ProcessNewArticles(shopData, supplier)
        ProcessDeletedArticles(shopData, supplier)
        ui.HorizontalLine()

        
        DownloadImagesIfUserWants(ui, newArticles)
          
    except Exception as ex:
        print('\n\n Eroare: ' + repr(ex) + '\n')
        logging.error('main: ' + repr(ex))
      
    ui.AskInput(MSG_PRESS_ENTER_TO_QUIT)

def GetSupplierData(ui, supplier):
    if ui.AskYesOrNo(QUESTION_DOWNLOAD_FEED) == YES:
        supplier.DownloadFeed()       
        
    print('\n    Cod: ' + supplier.code)
    numErrors = supplier.Import()
    if numErrors > 0:
        print(MSG_FEED_ERRORS + str(numErrors))
        
    supplier.ConvertToOurFormat()
    print('    Numar articole: ' + str(supplier.ArticlesCount()))
    
    AskUserConfirmationIfPossibleErrorIsDetected(ui, supplier)

def AskUserConfirmationIfPossibleErrorIsDetected(ui, supplier):
    if supplier.ArticlesCount() < 50:            
        if ui.AskYesOrNo(MSG_WARNING_LESS_50_ARTICLES + ' Continuati?') == NO:
            print('Ati renuntat la procesare.')
            sys.exit(0)

def DownloadImagesIfUserWants(ui, articles):
    ui.Title(TITLE_DOWNLOAD_NEW_IMAGES)
    if ui.AskYesOrNo('Descarc imaginile pentru '
                           + str(articles.ArticlesCount())
                           + ' articole noi?') == YES:
            articles.DownloadImages();  
    ui.HorizontalLine()
  
def ProcessUpdatedArticles (shopData, supplier):
    print('\n\nARTICOLE MODIFICATE')
    supplierCopy = copy.deepcopy(supplier)
    supplierCopy.IntersectWith(shopData)
    supplierCopy.RemoveArticlesWithNoUpdatesComparedToReference(reference=shopData)

    messagesList = supplierCopy.GetComparisonHumanReadableMessages(reference=shopData)

    print('    Numar articole: '+ str(supplierCopy.ArticlesCount())) 
    export.ExportPriceAndAvailabilityAndMessages(supplierCopy, 
                                                 messagesList, 
                                                 supplier.paths.getUpdatedArticlesFile())
    
    
def ProcessDeletedArticles (shopData, supplier):
    print('\n\nARTICOLE STERSE')
    articlesToDelete = copy.deepcopy(shopData)
    articlesToDelete.RemoveArticles(supplier)
       
    print('    Numar articole: ' + str(articlesToDelete.ArticlesCount()))
    export.ExportArticlesForDeletion(articlesToDelete,
                                     supplier.paths.getDeletedArticlesFile())
    


def ProcessNewArticles (shopData, supplier):
    print('\n\nARTICOLE NOI')
    newArticles = copy.deepcopy(supplier)
    newArticles.RemoveArticles(shopData)
    newArticles.RemoveInactiveArticles()

    print('    Numar articole: ' +  str(newArticles.ArticlesCount()))
    export.ExportAllData(newArticles,  supplier.paths.getNewArticlesFile())
    return newArticles
    
def LogInit(supplier): 
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

    #format: display_text, invoked_supplier_class
    items = [["Actualizare Nancy (NAN) ok",          "ArticlesNancy"],
                ["Actualizare BabyDreams (HDRE)",     "ArticlesBabyDreams"],
                ["Actualizare Bebex (BEB)",               "ArticlesBebex"],
                ["Actualizare BebeBrands (HBBA) ok",  "ArticlesBebeBrands"],
                ["Actualizare BabyShops (HMER)",      "ArticlesBabyShops"],
                ["Actualizare KidsDecor (HDEC)",        "ArticlesKidsDecor"],
                ["Actualizare Hubners (HHUB) ok",      "ArticlesHubners"]]

    for item in items:
        menu.addMenuItem(name = item[0],
                         callback = Factory.CreateSupplierFeedObject,
                         arguments = item[1])
        
    return menu
                        
if __name__ == '__main__':
    main()

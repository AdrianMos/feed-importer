import os.path, sys, logging, copy

from code.userinterface import UserInterface
from code.factory import Factory
from code.export import Export
from code.messages import *
from code.menu import Menu
from code.suppliers.articles import *
from code.updater import Updater

export = Export()

def main():
    
    terminal = UserInterface()
    terminal.PrintTitle(TITLE_SOFTWARE)
    
    TryUpdateSoftware(terminal)

    menu = buildMenu()
    #the menu callback creates the supplier feed object
    #according to the user selection
    supplier = menu.openMenu()

    if not isinstance(supplier, Articles):
        print(ERROR_SUPPLIER_BAD_INSTANCE_TYPE)
        sys.exit(0)   
    try:       
        LogInit(supplier)

        terminal.PrintSection(TITLE_IMPORT_SUPPLIER_DATA)
        GetSupplierData(terminal, supplier)
           

        terminal.PrintSection(TITLE_EXPORT_STANDARD_FORMAT)
        export.ExportDataForOnlineshop(supplier, supplier.paths.getSupplierFeedExportFile())
        
        
        terminal.PrintSection(TITLE_REMOVE_IRRELEVANT_ARTICLES )
        supplier.RemoveIrrelevantArticles()
        print(MSG_NUMBER_OF_ARTICLES + str(supplier.ArticlesCount()))
        
        
        terminal.PrintSection(TITLE_IMPORT_SHOP_DATA)      
        shopData = Factory.CreateFeedObjectForShop()
        shopData.Import()
        shopData.FilterBySupplier(supplier.code)
        print(MSG_NUMBER_OF_ARTICLES + str(shopData.ArticlesCount()))

        
        terminal.PrintSection(TITLE_COMPARING_SHOP_AND_SUPPLIER_DATA)
        ProcessUpdatedArticles(shopData, supplier)
        newArticles = ProcessNewArticles(shopData, supplier)
        ProcessDeletedArticles(shopData, supplier)

        
        DownloadImagesIfUserWants(terminal, newArticles)
          
    except Exception as ex:
        print('\n\n Eroare: ' + repr(ex) + '\n')
        logging.error('main: ' + repr(ex))
      
    terminal.AskInput(MSG_PRESS_ENTER_TO_QUIT)


def TryUpdateSoftware(terminal):    
    updater = Updater(gitUrl='https://github.com/AdrianMos/feed-importer.git',
                      gitBranch='master',
                      softwarePath = os.getcwd())

    print(MSG_SOFTWARE_VERSION.upper()
          + updater.GetCurrentSoftwareVersion() + '\n')

    terminal.PrintSeparator()
    print(TITLE_SOFTWARE_UPDATE)
    
    try :
        updater.Download()
        if updater.IsUpdateRequired():
            print(updater.GetSoftwareUpdateMessage())
            if terminal.AskYesOrNo(QUESTION_UPDATE_SOFTWARE) == YES:
                updater.Install()
        else:
            print(MSG_NO_NEW_SOFTWARE)
            
    except Exception as ex:
        print(MSG_SOFTWARE_UPDATE_ERROR + repr(ex) + '\n')
        logging.error('TryUpdateSoftware: ' + repr(ex))
        sys.exit(0)


def GetSupplierData(terminal, supplier):
    if terminal.AskYesOrNo(QUESTION_DOWNLOAD_FEED) == YES:
        supplier.DownloadFeed()       
        
    print('\n    Cod: ' + supplier.code)
    numErrors = supplier.Import()
    if numErrors > 0:
        print(MSG_FEED_ERRORS + str(numErrors))
        
    supplier.ConvertToOurFormat()
    print(MSG_NUMBER_OF_ARTICLES + str(supplier.ArticlesCount()))
    
    AskUserConfirmationIfPossibleErrorIsDetected(terminal, supplier)

def AskUserConfirmationIfPossibleErrorIsDetected(terminal, supplier):
    if supplier.ArticlesCount() < 50:            
        if terminal.AskYesOrNo(MSG_WARNING_LESS_50_ARTICLES + QUESTION_CONTINUE) == NO:
            print('Ati renuntat la procesare.')
            sys.exit(0)


def DownloadImagesIfUserWants(terminal, articles):
    terminal.PrintSection(TITLE_DOWNLOAD_NEW_IMAGES)
    if terminal.AskYesOrNo('Descarc imaginile pentru '
                           + str(articles.ArticlesCount())
                           + ' articole noi?') == YES:
            articles.DownloadImages();
            
  
def ProcessUpdatedArticles (shopData, supplier):
    print('\n\nARTICOLE MODIFICATE')
    supplierCopy = copy.deepcopy(supplier)
    supplierCopy.IntersectWith(shopData)
    supplierCopy.RemoveArticlesWithNoUpdatesComparedToReference(reference=shopData)

    messagesList = supplierCopy.GetComparisonHumanReadableMessages(reference=shopData)

    print(MSG_NUMBER_OF_ARTICLES+ str(supplierCopy.ArticlesCount())) 
    export.ExportPriceAndAvailabilityAndMessages(supplierCopy, 
                                                 messagesList, 
                                                 supplier.paths.getUpdatedArticlesFile())
    
    
def ProcessDeletedArticles (shopData, supplier):
    print('\n\nARTICOLE STERSE')
    articlesToDelete = copy.deepcopy(shopData)
    articlesToDelete.RemoveArticles(supplier)
       
    print(MSG_NUMBER_OF_ARTICLES + str(articlesToDelete.ArticlesCount()))
    export.ExportArticlesForDeletion(articlesToDelete,
                                     supplier.paths.getDeletedArticlesFile())
    


def ProcessNewArticles (shopData, supplier):
    print('\n\nARTICOLE NOI')
    newArticles = copy.deepcopy(supplier)
    newArticles.RemoveArticles(shopData)
    newArticles.RemoveInactiveArticles()

    print(MSG_NUMBER_OF_ARTICLES +  str(newArticles.ArticlesCount()))
    export.ExportAllData(newArticles,  supplier.paths.getNewArticlesFile())
    return newArticles

    
def LogInit(supplier): 
    logging.basicConfig(filename = supplier.paths.getLogFile(),
                        level = logging.INFO, 
                        filemode = 'w',
                        format ='%(asctime)s     %(message)s')


def exitApplication(data):
    print("... bye")
    sys.exit(0)


def buildMenu():
    menu = Menu(title = "Optiuni disponibile:",
                       userMessage = 'Alegeti:')
    
    menu.addMenuItem(name="Iesire",
                     callback=exitApplication,
                     arguments="")

    #format: display_text, invoked_supplier_class
    items = [["Actualizare Nancy (NAN) OK",        "ArticlesNancy"],
             ["Actualizare BebeBrands (HBBA) OK",  "ArticlesBebeBrands"],
             ["Actualizare Hubners (HHUB) OK",     "ArticlesHubners"],
             ["Actualizare BabyDreams (HDRE) OK",  "ArticlesBabyDreams"],
             ["  Actualizare Bebex (BEB)",           "ArticlesBebex"],
             ["  Actualizare BabyShops (HMER)",      "ArticlesBabyShops"],
             ["  Actualizare KidsDecor (HDEC)",      "ArticlesKidsDecor"]
             ]

    for item in items:
        menu.addMenuItem(name = item[0],
                         callback = Factory.CreateSupplierFeedObject,
                         arguments = item[1])
        
    return menu
                        
if __name__ == '__main__':
    main()

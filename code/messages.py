import sys

MSG_WARNING_LESS_50_ARTICLES = 'ATENTIE: Posibila eroare in datele '  + \
                               'furnizorului. Exista mai putin de 50 ' + \
                               'de articole.'

MSG_FEED_ERRORS = '\n\n***    Au fost gasite ERORI in feed. Exista ' + \
                  'articole neimportate. ANUNTATI distribuitorul. ' + \
                  'Detalii in log. Erori gasite:'

MSG_PRESS_ENTER_TO_QUIT = '\nApasati enter pentru iesire. >> '
MSG_SOFTWARE_VERSION = 'Versiune:\n'
MSG_NO_NEW_SOFTWARE = '  Nu exista versiuni noi\n'
MSG_SOFTWARE_UPDATE_FAILED = '  Actualizare esuata\n'

MSG_NUMBER_OF_ARTICLES = '    Numar articole: '
MSG_USER_SELECTION_QUIT = 'Ati renuntat la procesare.'


YES = 'da'
NO = 'nu'

QUESTION_DOWNLOAD_FEED = 'Descarc date noi pentru acest furnizor?'
QUESTION_CONTINUE = ' Continuati?'
QUESTION_DOWNLOAD_FEED
QUESTION_UPDATE_SOFTWARE = '  Exista o versiune noua de software.\n  Doriti actualizare?'
QUESTION_DOWNLOAD_IMAGES_FOR_NEW_ARTICLES = 'Descarc imaginile pentru articolele noi?'

TITLE_SOFTWARE = ' Actualizare Haiducel '
TITLE_IMPORT_SUPPLIER_DATA = ' IMPORT DATE FURNIZOR '
TITLE_EXPORT_STANDARD_FORMAT = ' SALVARE DATE FURNIZOR IN FORMAT STANDARD '
TITLE_REMOVE_IRRELEVANT_ARTICLES = ' ELIMINARE ARTICOLE IRELEVANTE '
TITLE_IMPORT_SHOP_DATA = ' IMPORT DATE HAIDUCEL '
TITLE_COMPARING_SHOP_AND_SUPPLIER_DATA = ' COMPARARI '
TITLE_DOWNLOAD_NEW_IMAGES = ' DESCARCARE IMAGINI NOI '
TITLE_SOFTWARE_UPDATE = 'Actualizare software'

SUBTITLE_UPDATED_ARTICLES = '\n\nARTICOLE MODIFICATE'
SUBTITLE_DELETED_ARTICLES = '\n\nARTICOLE STERSE'
SUBTITLE_NEW_ARTICLES = '\n\nARTICOLE NOI'

ERROR_MSG = '\n\n Eroare: '

ERROR_SUPPLIER_BAD_INSTANCE_TYPE = "Error: the menu callback doesn't create an Articles instance"


def PrintExeptionAndQuit(messageHeader, exception):
    print(messageHeader + (repr(exception) if (exception!=None) else '') + '\n')
    input(MSG_PRESS_ENTER_TO_QUIT)
    sys.exit(0)

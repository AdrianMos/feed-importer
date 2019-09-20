import os.path, time

class PathBuilder(object):
    allImagesFolder = os.path.join("data", "_ imagini noi", "mari neprocesate")
    mainImagesFolder = os.path.join("data", "_ imagini noi", "mici neprocesate")

    
    def __init__(self, code): 
        self._code = code
        self.feedFile = os.path.join("data", code, "feed" + code + ".csv")
        self.configFile = os.path.join(os.getcwd(), "config", "config" + code + ".ini")
        self.credentialsFile = os.path.join(os.getcwd(), "config", "credentials", "credentials" + code + ".ini")
    
    def getLogFile(self):
        return os.path.join('data', self._code, 'erori ' + self._code + '.log')
        
    def getUpdatedArticlesFile(self):       
        return self._generateOutputFileName('articole existente cu pret sau status modificat')
        
    def getDeletedArticlesFile(self):       
        return self._generateOutputFileName('articole de sters')
                        
    def getNewArticlesFile(self):       
        return self._generateOutputFileName('articole noi')
    
    def getSupplierFeedExportFile(self):       
        return self._generateOutputFileName('Onlineshop')    
    
    def getOutputFolderPath(self):
        return os.path.join(os.getcwd(), "data", self._code, "out");
    
    def _generateOutputFileName(self, name):
        return os.path.join('data', self._code, 'out', 
                        '' + self._code  + ' ' + name + ' ' 
                        + time.strftime('%Y-%m-%d')
                        + '.csv')
    

    


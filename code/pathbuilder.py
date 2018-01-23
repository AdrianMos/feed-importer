import os.path, time

class PathBuilder(object):
    allImagesFolder = os.path.join("data", "_ imagini noi", "mari neprocesate")
    mainImagesFolder = os.path.join("data", "_ imagini noi", "mici neprocesate")

    
    def __init__(self, code): 
        self.code = code
        self.feedFile = os.path.join("data", code, "feed" + code + ".csv")
        self.configFile = os.path.join(os.getcwd(), "config", "config" + code + ".ini")
        self.credentialsFile = os.path.join(os.getcwd(), "config", "credentials", "credentials" + code + ".ini")
    
    def getLogFile(self):
        return os.path.join('data', self.code, 'erori ' + self.code + '.log')
        
    def getUpdatedArticlesFile(self):       
        return self.generateOutputFileName('articole existente cu pret sau status modificat')
        
    def getDeletedArticlesFile(self):       
        return self.generateOutputFileName('articole de sters')
                        
    def getNewArticlesFile(self):       
        return self.generateOutputFileName('articole noi')
    
    def getSupplierFeedExportFile(self):       
        return self.generateOutputFileName('Onlineshop')    
    
    
    def generateOutputFileName(self, name):
        return os.path.join('data', self.code, 'out', 
                        '' + self.code  + ' ' + name + ' ' 
                        + time.strftime('%Y-%m-%d')
                        + '.csv')
    
    def getOutputFolderPath(self):
        return os.path.join(os.getcwd(), "data", self.code, "out");
    


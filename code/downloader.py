import os.path
import requests
import urllib.request
import sys
from code.messages import *

class Downloader(object):
   
    def __init__(self, credentials, paths):
        self.credentials = credentials
        self.paths = paths
    
    def DownloadFeed(self, savePath, downloadUrl):
        print("*** Descarcare feed " + savePath + "...")     
               
        isPasswordRequired = self.credentials.username != ""               
        if isPasswordRequired: 
            response = requests.get(downloadUrl,
                                    verify=False, 
                                    auth=(self.credentials.username, self.credentials.password))
                                    
            if  response.status_code != 200:
                message = "   \nEROARE: Parola si/sau utilizatorul nu sunt valide, status: " + str(response.status_code)
                PrintExeptionAndQuit(message, None)
            
            feedData = response.text 
            
            with open(savePath, 'wb') as textfile:
                textfile.write(bytes(feedData, 'UTF-8'))
                textfile.close()
        else:
            response = urllib.request.urlopen(downloadUrl)
                          
            feedData = response.read().decode("utf-8-sig").encode("raw_unicode_escape")
            feedData = feedData.decode('unicode_escape').encode('ascii','ignore')
         
            with open(savePath, "wb") as textfile:
                textfile.write(feedData)
                textfile.close()
            
        print("    Feed " + savePath + " descarcat.")        
    
    def DownloadAndSaveImage(self, imgUrl, imgSavePath1, imgSavePath2=""):
        try:
            imgUrl = imgUrl.replace(" ", "%20")
            imgUrl = self.RepairBrokenUrl(imgUrl)
            
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) ' + \
                         'Ubuntu/12.04 Chromium/18.0.1025.168 Chrome/18.0.1025.168 Safari/535.19'
            
            if self.credentials.username != "":
                                                        
                response = requests.get(imgUrl,
                                        verify=False, 
                                        auth=(self.credentials.username, self.credentials.password),
                                        headers={'user-agent': user_agent})
                                
                if response.status_code == 200:
                    with open(imgSavePath1, 'wb') as file:
                        file.write(response.content)
                    
                    # If a second save path location has been given, save the image in this location
                    if imgSavePath2!="":
                        with open(imgSavePath2, 'wb') as file:
                            file.write(response.content)
            
            else:
                req = urllib.request.Request(imgUrl, headers={'User-Agent': user_agent})
                response = urllib.request.urlopen(req)
                data = response.read()                
                
                # Save image
                with open(imgSavePath1, 'wb') as file:
                    file.write(data)
                
                # If a second save path location has been given, save the image in this location
                if imgSavePath2!="":
                    with open(imgSavePath2, 'wb') as file:
                        file.write(data)
                #print("#path" + imgSavePath1 + " #orig path:" + imgUrl)
            
        
        except OSError as ex:
            print("Eroare salvare fisier: " + imgSavePath1 + " si/sau " + imgSavePath2 +"\n   motiv:"+ ex.reason)  
            logging.error("DownloadAndSaveImage : eroare salvare fisier: " + imgSavePath1 + " si/sau " + imgSavePath2 +"\n   motiv:"+ ex.reason)   
            
        except urllib.error.HTTPError as ex:
            print ("Unexpected error:",  ex.reason)
            logging.error("DownloadAndSaveImage : " + ex.reason)
      
        except urllib.error.URLError as ex:
            print("Eroare download: " + imgUrl + "\n  motiv: " + ex.reason + " ++" + str(sys.exc_info()[0]))
            logging.error("DownloadAndSaveImage : nu se poate downloada <" + imgUrl + "> motiv: " + ex.reason + " ++" + str(sys.exc_info()[0]))   
            raise
    
    def RepairBrokenUrl(self, url):
        repaired = url.replace(":www", "://www")
        return repaired
    
    def DownloadImages(self, articleList):
        '''
        Downloads the customer images
        '''
         
        ''' Images urls are stored in articlesList.images and new image names in articlesList.imagesNew.
            On the first position of articlesList.imagesNew the small image name is stored. '''
        
        print("    Folder descarcare: " + self.paths.allImagesFolder)
        print("                       " + self.paths.mainImagesFolder + "\n")
        
        for art in articleList:       
            # Download all images for current article
            for i, imgUrl in enumerate(art.imagesUrl):
             
                if imgUrl!="":  
                    try:
                        # If the main image is downloaded, save it also to a separate folder - later used
                        # for generating the small image
                        isMainImage = (i==0)
                        if isMainImage:
                            self.DownloadAndSaveImage(imgUrl,
                                                      imgSavePath1 = os.path.join(self.paths.allImagesFolder, art.imagesNames[i]),
                                                      imgSavePath2 = os.path.join(self.paths.mainImagesFolder,art.imagesNames[i])) 
                        else:
                            self.DownloadAndSaveImage(imgUrl, 
                                                      imgSavePath1 = os.path.join(self.paths.allImagesFolder,art.imagesNames[i])) 
                    except:
                        e = sys.exc_info()[0]
                        print ("\nEROARE descarcare imagine pentru articolul: ", art.title, ' @ ', art.imagesNames[i], "@", imgUrl, " eroare:", e)
                        logging.error('articles: articol <' + art.title + '> : eroare descarcare imagine <' + imgUrl + '> : mesaj eroare : ' + e)
                    
                    
                    sys.stdout.write(".")
                    sys.stdout.flush()
            
            sys.stdout.write("/")
            sys.stdout.flush()
        print("\n") 
    
    
    
    


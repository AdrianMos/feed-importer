

class Article(object):
    """Holds article information"""
    
            
    def __init__(self, id, title, price, available, initialCategory, category, supplier, subcategory="",
                 imagesUrl=[""]*13, description="", weight=0, quantity=1, pricePromo=0):  
        self.id = id.strip()
        self.title = title.strip()
        self.price = float(str(price).strip())
        self.pricePromo = float(str(pricePromo).strip())
        self.description = description.strip()
        self.quantity = str(quantity).strip()
        self.weight = str(weight).strip()
        self.available = available.strip()
        self.initialCategory = initialCategory.strip()
        self.category = category.strip()
        self.subcategory = subcategory.strip()
        self.supplier = supplier.strip()
        self.imagesUrl = [img.strip() for img in imagesUrl]
        self.imageSmallName = ""
        self.imageSmallPath = ""
        self.images = [""]*12
        self.imagesNames = [""]*12
        self.imagesPaths = [""]*12
        
        # prepare the image names as we use them
        #for i, url in enumerate(self.imagesUrl):
        #    customName = url
        #    customName = customName.replace("\\", "/")
        #    # extract only the filename from whole path
        #    customName = customName[customName.rfind("/")+1:]
        #    # replace spaces by dash "-"
        #    customName = customName.replace(" ", "-")
        #    customName = customName.replace("%20", "-")
        #    self.images[i] = customName
        #    #print("image " + str(i) + " name: " + self.images[i])

        #self.imageSmall = GetSmallImageName(self.images[0])
        
        # Extend the images list to the maximum elelemnts
        for i in range(len(self.imagesUrl), 12):
            self.imagesUrl.append("")
     
     
    def IsSameArticle(self, articleToCompare):
        if self.id == articleToCompare.id:
            return True
        return False
    
    def ComparePriceAndAvailability(self, articleToCompare):
        '''
        Compares the price and availability of the articles. If they are different False is returned and a message which
        describes the diferences.
        :param articleToCompare:
        '''
        msg = ""
        isDifferent = False
        if self.price!=articleToCompare.price:
            msg = msg + " pret " + str(self.price) + "=/=" + str(articleToCompare.price) 
            isDifferent = True
        
        if self.available!=articleToCompare.available:
            msg = msg + " stoc " + str(self.available) + "=/=" + str(articleToCompare.available)
            isDifferent = True
            
        return isDifferent, msg
                
                
    def __str__(self):
        '''
        Overwrites str function for this object.
        '''
      
        
        toString =  ("\n------------------------------------" + 
                "\nTitle: *" + self.title + "*" + 
                "\nID: *" + self.id + "*" + "  Price: *" + str(self.price) + "*  Quantity: *" + str(self.quantity) + "*" + 
                "\nWeight: *" + str(self.weight) + "*" + "  Available: *" + self.available + "*  Category: *" + self.category + "*" +               
                "\nDescription: *" + self.description + "*")   
       
        counter = 0
        for imageUrl in self.imagesUrl:
            if image!="":
                toString = toString +  "\nImage" + str(counter) + ": *" + imageUrl + "*"
            counter = counter+1
    
        return toString

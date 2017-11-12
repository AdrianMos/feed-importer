

class Article(object):
    """Holds article information"""
    
            
    def __init__(self, id, title, price, available, initialCategory, category, supplier, subcategory="", images=[""]*13, description="", weight=0, quantity=1, pricePromo=0):  
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
        self.images = [img.strip() for img in images]
        
        # Extend the images list to the maximum elelemnts
        for i in range(len(self.images), 13):
            self.images.append("")
        

    
       
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
        for image in self.images:
            if image!="":
                toString = toString +  "\nImage" + str(counter) + ": *" + image + "*"
            counter = counter+1
    
        return toString

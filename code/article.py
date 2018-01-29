

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
        self.imagesNames = [""]*12
        self.imagesPaths = [""]*12
             
     
    def IsSameArticle(self, articleToCompare):
        if self.id == articleToCompare.id:
            return True
        return False
               
                
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

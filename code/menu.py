import sys
class MenuItem:
    def __init__(self, name, function, arguments):
        self.name = name
        self.function = function
        self.arguments = arguments
        
class Menu:
    title = ""
    items = []
    def __init__(self, title, userMessage):
        self.title = title
        self.userMessage = userMessage
    
    def printMenu(self):
        print(str("*"*len(self.title)))
        print(self.title)
        for index, item in enumerate(self.items):
            print("  " + str(index) + ". " + item.name)
            
    def isValidOption(self, option):
        if 0 <= option <= len(self.items)-1:
            return True
        else:
            return False
            
    def getUserOption(self):
        option=None
        while True:
            try:
                option = int(input('\n' + self.userMessage + ' >> '))
                if not self.isValidOption(option):
                    raise RuntimeError()
                else:
                    break
            except:
                print("    invalid option")             
        return option
    
    def openMenu(self):
        self.printMenu()
        
        option=None
        hasOptions = len(self.items)>0
        if hasOptions:
            option = self.getUserOption()
            print(str(self.items[option].function))
            print(str(self.items[option].arguments))
            callbackAnswer = self.items[option].function(self.items[option].arguments)
        return callbackAnswer
    
    def addMenuItem(self, name, callback, arguments):
        self.items.append(MenuItem(name, callback, arguments))
    

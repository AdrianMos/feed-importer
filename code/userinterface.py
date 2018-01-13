
class UserInterface(object):
    """User interface functionality"""
    
    TITLE_LENGTH = 79
    FILL_CHARACTER = '-'
    HORIZONTAL_LINE = FILL_CHARACTER * TITLE_LENGTH + '\n'
    
    titleCounter = 1;
    
    def DisplayHeader(self):
        
        separator = '\n' + '*' * self.TITLE_LENGTH
        print(separator + '\n')
        print(' Actualizare date Haiducel '.center(self.TITLE_LENGTH ,' ')) 
        print(separator)
        print("V 5.1, 06.01.2018\n")
    
    def DisplayOptions(self):
        
        print("Optiuni disponibile:")
        print("  1. Iesire\n"
              "  2. Actualizare Nancy (NAN) ok\n"
              "  3. Actualizare BabyDreams (HDRE)\n" 
              "  4. Actualizare Bebex (BEB)\n"
              "  5. Actualizare BebeBrands (HBBA) ok\n"
              "  6. Actualizare BabyShops (HMER)\n"
              "  7. Actualizare KidsDecor (HDEC)\n"  
              "  8. Actualizare Hubners (HHUB) ok\n"
              )

    def GetCodeForOption(self, option):
                
        if option=="2":
            code = "NAN"
        elif option=="3":
            code = "HDRE"
        elif option=="4":
            code = "BEB"
        elif option=="5":
            code = "HBBA"
        elif option=="6":
            code = "HMER"
        elif option=="7":
            code = "HDEC"
        elif option=="8":
            code = "HHUB"
        else:
            code =  None
            
        return code
    
    
    def Title(self, title):
        
        titleCountStr = '(' + str(self.titleCounter) + ')'
        
        if len(title) <= self.TITLE_LENGTH - 2:
            
            formatedTitle = title.upper().center(self.TITLE_LENGTH \
                                                 - len(titleCountStr),
                                                 self.FILL_CHARACTER)
            
            print('\n' + titleCountStr + formatedTitle + '\n')
        else:
            print(self.HORIZONTAL_LINE +
                  titleCountStr + ' ' +
                  title.upper() + '\n' +
                  self.HORIZONTAL_LINE)
        
        self.titleCounter += 1
    
    def HorizontalLine(self):
        print (self.HORIZONTAL_LINE)
    

    def AskYesOrNo(self, question):
        '''
        Displays the question and waits for a yes or no answer (y/n).
        '''
        userInput=""
        print('')
        while (userInput!="da" and userInput!="nu"):
            userInput = input(question + ' da/nu: >> ').lower()
        return userInput
    
    def AskInput(self, question):
        return input(question)


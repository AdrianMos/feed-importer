
class UserInterface(object):
    """User interface functionality"""
    
    def DisplayHeader(self):
        
        print("*******************************************")
        print("*** Actualizare date magazinul Haiducel ***")
        print("*******************************************")
        print("Adrian Mos, V 3.3, 04.06.2016\n")
    
    def DisplayOptions(self):
        
        print("Optiuni disponibile:")
        print("  1. Iesire\n"
              "  2. Actualizare Nancy (NAN)\n"
              "  3. Actualizare BabyDreams (HDRE)\n" 
              "  4. Actualizare Bebex (BEB)\n"
              "  5. Actualizare BebeBrands (HBBA)\n"
              "  6. Actualizare BabyShops (HMER)\n"
              "  7. Actualizare KidsDecor (HDEC) - nu merge, caractere"  
                               " ilegale in feed, feed-nu se descarca\n"
              "  8. Actualizare Hubners (HHUB)\n"
              )
    
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


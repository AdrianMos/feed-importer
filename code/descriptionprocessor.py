import bleach
import re
   
class DescriptionProcessor(object):
    '''
    Cleans the article descriptions to a format handled well by the on-line platform.
    '''

    @staticmethod 
    def CleanDescription(inData):
        
        text = inData.replace("MyKids","").replace("BABY MIX","")


        text = DescriptionProcessor._InsertSpaceBetweenSentences(text)
        text = DescriptionProcessor._InsertSpaceAfterComma(text)
        text = DescriptionProcessor._ReplaceUnknownRomanianCharacters(text)
        
        text = DescriptionProcessor._RemovedUnallowedTagsAndChars(text)      
        text = DescriptionProcessor._ConvertBreaksToOurFormat(text)
        text = DescriptionProcessor._ReplaceDoubleBreaksWithOneBreak(text)
        text = DescriptionProcessor._RemoveEmptyParagraphs(text)
    
        text = DescriptionProcessor._MoveDashedLinesOnNewRow(text)
        
        text = DescriptionProcessor._MakeSubtitlesDistinct(text)
        text = DescriptionProcessor._ReplaceDoubleBreaksWithOneBreak(text)
        text = DescriptionProcessor._RemoveBreakAfterParagraphStart(text)
     
        return text
    
    @staticmethod   
    def _MoveDashedLinesOnNewRow(inData):
            
            zeroOrMoreSpaceChars = r" *" 
            wordNoNumbersAtLeastOneChar = r"[^\W\d_]+"
            wordNoNumbers = r"[^\W\d_]*"
            
            findPattern =  wordNoNumbers + zeroOrMoreSpaceChars + "-" + zeroOrMoreSpaceChars + wordNoNumbersAtLeastOneChar
            processed = re.sub(findPattern, DescriptionProcessor._InsertBreakBeforeDashIfNotWithinWord, inData)
            
            #find patters of chars excepting numbers, followed by dashed and number, e.g. "it includes: - 4 pillows -2 blankets"
            number = r"[0-9]"
            anyCharExceptNumber = r"[^0-9]"
            findPattern =  anyCharExceptNumber + zeroOrMoreSpaceChars + "-" + zeroOrMoreSpaceChars + number
            processed = re.sub(findPattern, DescriptionProcessor._InsertBreakBeforeDashIfNotWithinWord, processed)

            return processed
    
    
    @staticmethod
    def _MakeSubtitlesDistinct(inData):
        '''
        Finds the headings and makes them pretty.
        A heading is identified as: First word starts with uppercase, then max 2 more words, whole phrase ending in ":"
        '''
        # Regular expression patterns used for finding the heading
        wordWithCapital = r"\b[A-Z]\w*"
        zeroOrMoreSpaceChars = r" *"  
        zeroOrMoreWordChars  = r"\w*" 
        
        groupStart = r"("
        groupEnd = r")"
        group = r"\1"  # refers to data extracted from a match, located between first pair of groupStart and groupEnd.
        
        searchPattern = groupStart + \
                           wordWithCapital + \
                           zeroOrMoreSpaceChars + zeroOrMoreWordChars + \
                           zeroOrMoreSpaceChars + zeroOrMoreWordChars + \
                        groupEnd + \
                           zeroOrMoreSpaceChars + ":"
        
        prettyHead = "<br /><br /><strong>"
        prettyTail   = "</strong>"
        replacePattern = prettyHead + group + r":" + prettyTail
        
        return re.sub(searchPattern, replacePattern, inData)
    
    @staticmethod
    def _InsertBreakBeforeDashIfNotWithinWord(matchObj):
        '''
        Used by a regex function. Called when a specific string pattern is found.
        '''
        match = matchObj.group(0)
        #print(" " + match)
        
        knownDashWords = ["a-si", "a-l", "ce-i", "intr-un", "intr-unul", "intr-o", "l-am", "i-am",  "sa-si", "sa-l", "a-ti", "si-a",
                         "dintr-o", "dintr-un", "non-toxic", "non-toxice", "ultra-compact", "anti-rasturnare",
                          "mini-geam", "full-option", "crescandu-l", "nou-nascuti", "nou-nascut", "non-alergic",
                          "dandu-i", "anti-umezeala", "anti-alergic", "anti-alergica", "asigurandu-i", "dreapta-stanga",
                          "oferindu-i", "de-a", "Oeko-Tex", "anti-alunecare", "auto-oprire", "pastrandu-si", "stanga-dreapta",
                          "pernita-suport", "mentinandu-i", "ajustandu-se", "transformandu-se", "cauza-efect",
                          "mega-rampa", "ajutandu-l", "oferindu-le", "ne-am", "care-l", "high-resolution",
                          "display-ul", "de-congelarii", "de-congelare", "printr-o", "U-shape", "fata-spate",
                          "printr-un", "anti-UV", "pop-up", "anti-insecte", "evitandu-se", "a-i",
                          "dispay-ul", "Rasfatati-va", "nedeformandu-se", "integrandu-se", "phtalate-free",
                          "OEKO-TEX", "Marie-Sofie", "re-testate", "facandu-se", "click-uri",
                          "nou-nascutului", "anti-rotire", "re-gandite", "PVC-ul", "non-toxica",
                          "nu-l", "ce-l"];

        #TODO: implement logic for "anti-" words
        #TODO: mega-, non- ...
        #TODO: addd logic to replace english words with romanian "display-ul" -> "ecranul", "high-resolution"
        
        isDashWithinWord = match in knownDashWords    
        if (isDashWithinWord):
            return match
        else:
            index = str(match).find('-')
            return match[:index] + "<br />" + match[index:]
    
    @staticmethod
    def _ReplaceTripleBreaksWithTwoBreaks(inData):
        return re.sub(r"< ?br ?/> ?< ?br ?/> ?< ?br ?/>", r"<br /><br />", inData)
    
    @staticmethod
    def _InsertSpaceBetweenSentences(inData):
        # searches patterns lowerLetter/number/point followed by largeLetter
        return re.sub(r"([a-z0-9\.])([A-Z])", r"\1 \2", inData)
    
    @staticmethod
    def _InsertSpaceAfterComma(inData):
        return re.sub(r"(\w),(\w)", r"\1, \2", inData)
    
    @staticmethod   
    def _ReplaceDoubleBreaksWithOneBreak(inData):
        return re.sub(r"< ?br ?/> ?< ?br ?/>", r"<br />", inData)
        
    @staticmethod   
    def _RemoveBreakAfterParagraphStart(inData):
        processed = re.sub(r"<p> *< ?br ?/ ?>", r"<p>", inData)
        processed = re.sub(r"<p ?> *< ?/ ?br ?>", r"<p>", processed)
        return processed
    
    @staticmethod
    def _ReplaceUnknownRomanianCharacters(inData):
        return inData.replace("&#259;","a").replace("&#351;", "s").replace("&#355;", "t").replace("&icirc ", "i")
   
    @staticmethod
    def _RemovedUnallowedTagsAndChars(inData):   
        text = inData.replace("<div", "<p").replace("&lsquo", "\"").replace("&rsquo", "\"")
        text = text.replace("&ldquo", "\"").replace("&rdquo", "\"")
        text = text.replace("&ndash", "-").replace("&bull;", "-")
        
        # Remove invalid tags but keep their content.
        allowedTags = ['p', 'i', 'b', 'strong', 'br', 'span']
        text = bleach.clean(text, allowedTags, strip=True)

        text = text.replace("<span>", " ").replace("</span>", " ")

        oneOrMoreSpaceChars = r"\s+"
        text = re.sub(oneOrMoreSpaceChars, ' ', text)
        
        return text
    
    @staticmethod
    def _ConvertBreaksToOurFormat(inData):     
        return inData.replace("<br>", "<br />")

    @staticmethod
    def _RemoveEmptyParagraphs(inData):
        zeroOrMoreSpaceChars = r" *"
        findPattern = r"<p>" + zeroOrMoreSpaceChars + r"</p>"
        return re.sub(findPattern, "", inData)
    
        

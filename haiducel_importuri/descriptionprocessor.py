'''
Created on 26.12.2015

@author: adrian mos
'''
# from bs4 import BeautifulSoup, NavigableString
import bleach
import re

    
def _InsertBreakBeforeDashIfNotWithinWord(matchObj):
    '''
    Used by a regex function. Called when a specific string pattern is found.
    '''
    match = matchObj.group(0)
    isDashWithinWord = match in ["sa-s", "ce-i", "tr-u", "tr-o", "l-am", "i-am", "a-si", "sa-si", "sa-l", "a-ti", "si-a", "non-toxic", "ultra-compact", "mini-geam", "full-option", "anti-rasturnare", "3-10", "0-10"]; #from word: sa-si, ce-i, dintr-un, dintr-o
    
    if (isDashWithinWord):
        return match
    else:
        index = str(match).find('-')
        return match[:index] + "<br />" + match[index:]


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
        
        text = DescriptionProcessor._RemovedUnallowedTags(text)      
        text = DescriptionProcessor._ConvertBreaksToOurFormat(text)
        text = DescriptionProcessor._ReplaceDoubleBreaksWithOneBreak(text)
    
        text = DescriptionProcessor._MoveDashedLinesOnSeparateLine(text)
        
        text = DescriptionProcessor._MakeSubtitlesDistinct(text)
        text = DescriptionProcessor._ReplaceDoubleBreaksWithOneBreak(text)
     
        return text
    
    @staticmethod   
    def _MoveDashedLinesOnSeparateLine(inData):
        
            zeroOrMoreSpaceChars = r" *" 
            zeroOrOneChar = r".?"
            wordChar = r"\w"
            
            findPattern = zeroOrOneChar + zeroOrOneChar + "-" + zeroOrMoreSpaceChars + wordChar
    #       findPattern = r".?.?- *\w" 
            return re.sub(findPattern, _InsertBreakBeforeDashIfNotWithinWord, inData)
    
    
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
    def _ReplaceUnknownRomanianCharacters(inData):
        return inData.replace("&#259;","a").replace("&#351;", "s").replace("&#355;", "t")
   
    @staticmethod
    def _RemovedUnallowedTags(inData):   
        text = inData.replace("<span", "<p").replace("<div", "<p")
        
        # Remove invalid tags but keep their content.
        allowedTags = ['p', 'i', 'b', 'strong', 'br']
        text = bleach.clean(text, allowedTags, strip=True)  
        return text
    
    @staticmethod
    def _ConvertBreaksToOurFormat(inData):     
        return inData.replace("<br>", "<br />")
       
    def __init__(self, params):
        '''
        Constructor
        '''
        
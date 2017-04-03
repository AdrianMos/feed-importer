'''
Created on 27.04.2014

@author: adrian
'''
import collections
from articles import Articles

class Operations(object):
    '''
    Includes operations that can be performed on articles.
    '''

    @staticmethod
    def ExtractUpdatedArticles(articlesReference, articlesToCompare):
        '''
        Compares all articles from articlesReference with the articlesToCompare and
        returns an Articles() object with all updated articles.
        
        It also returns a dictionary including pairs of (id, comparison message).
        '''
        compareStatus=collections.OrderedDict()
        articlesUpdated = Articles(articlesReference.code)
     
        for art1 in articlesReference.articleList:
            for art2 in articlesToCompare.articleList:
                
                if art1.IsSameArticle(art2):
                    #article found, compare price and availability (for now), later on all fields should be compared
                    
                    different, msg = art1.ComparePriceAndAvailability(art2)
                                       
                    #add the article to the list of updated articles; add the comparison message
                    if different:
                        articlesUpdated.articleList.append(art2)
                        compareStatus.update([(str(art1.id), msg)])
                    break
                
        return articlesUpdated, compareStatus

    @staticmethod
    def SubstractArticles(articlesToSubstractFrom, articlesToBeSubstracted):
        '''
        Substracts articlesToBeSubstracted from articlesToSubstractFrom and
        returns an Articles() object with all updated articles.
        '''
               
        result = Articles("")
     
        for art1 in articlesToSubstractFrom.articleList:
            
            articleFound = False
            
            for art2 in articlesToBeSubstracted.articleList:
                
                #If the article exists in both lists
                if art1.IsSameArticle(art2):
                    articleFound = True
            
            #If the article was not found in the second list, we add it to the result list
            if articleFound == False:
                result.Add1(art1)
                
        return result
    
    @staticmethod
    def RemoveUnavailableArticles(articles):
        '''
        Removes the unavailable articles.
        Returns an Articles() object containing only available articles.
        '''     
        result = Articles("")
     
        for art1 in articles.articleList:
            
            if art1.available == "Active":
                result.Add1(art1)
                
        return result

    @staticmethod
    def CopyArticlesAndSetStatus(articles, status):
        '''
        Creates a copy of the articles but sets the status as required.  
        Returns an Articles() object with all updated articles.
        '''
               
        result = Articles("")
     
        position=0
        for art1 in articles.articleList:
            result.Add1(art1)
            result.articleList[position].status=""
            
            
                
        return result

    def __init__(self, params):
        '''
        Constructor
        '''
        
'''
Created on 27.04.2014

@author: Adrian Mos
'''
import collections
from code.suppliers.articles import Articles
import copy

class Operations(object):
    '''
    Includes operations that can be performed on articles.
    '''

##    @staticmethod
##    def ExtractUpdatedArticles(articlesReference, articlesToCompare):
##        '''
##        Compares all articles from articlesReference with the articlesToCompare and
##        returns an Articles() object with all updated articles.
##        
##        It also returns a dictionary including pairs of (id, comparison message).
##        '''
##        compareStatus=collections.OrderedDict()
##        articlesUpdated = Articles(articlesReference.code, None, None, None)
##     
##        for art1 in articlesReference.articleList:
##            for art2 in articlesToCompare.articleList:
##                
##                if art1.IsSameArticle(art2):
##                    #article found, compare price and availability (for now), later on al l fields should be compared
##                    
##                    different, msg = art1.ComparePriceAndAvailability(art2)
##                                       
##                    #add the article to the list of updated articles; add the comparison message
##                    if different:
##                        articlesUpdated.articleList.append(art2)
##                        compareStatus.update([(str(art1.id), msg)])
##                    break
##                
##        return articlesUpdated, compareStatus



##    @staticmethod
##    def IntersectArticles(articles1, articles2):
##        '''
##        Intersect the two sets of articles
##        '''     
##        result = copy.deepcopy(articles1)
##               
##        #we check elements backwards, from last element to first one
##        #in this way, if we remove an element, the indexes for the
##        #unchecked ones (which have a lower index) are not affected
##        for i, art1 in reversed(list(enumerate(result.articleList))):
##            found = False
##            for art2 in articles2.articleList:
##                print('comparing: ' + str(art1.id) + " with " + str(art2.id))
##                if art1.IsSameArticle(art2):
##                    found = True
##                    break
##            if found == False:
##                print("removing art " + str(art1.id))
##                result.articleList.pop(i)
##                
##
##        return result


    @staticmethod
    def SubstractArticles(articlesToSubstractFrom, articlesToBeSubstracted):
        '''
        Substracts articlesToBeSubstracted from articlesToSubstractFrom and
        returns the difference
        '''     
        #print("length art to substract from: " + str(len(articlesToSubstractFrom.articleList)))
        #print("length art to be substracted: " + str(len(articlesToBeSubstracted.articleList)))
        result = copy.deepcopy(articlesToSubstractFrom)
        #print("length art to substract from deepcopy: " + str(len(result.articleList)))

        #print("art to substract from deepcopy: " + str(len(result.articleList)))
        #for art1 in result.articleList:
        #    print(" " + str(art1.id))

        #print("art to be substracted: " + str(len(result.articleList)))
        #for art1 in articlesToBeSubstracted.articleList:
        #    print(" " + str(art1.id))

               
        #we check elements backwards, from last element to first one
        #in this way, if we remove an element, the indexes for the
        #unchecked ones (which have a lower index) are not affected
        for i, art1 in reversed(list(enumerate(result.articleList))):
            for art2 in articlesToBeSubstracted.articleList:
                #print('comparing: ' + str(art1.id) + " with " + str(art2.id))
                if art1.IsSameArticle(art2):
                    #print("removing art " + str(art1.id))
                    result.articleList.pop(i)
                    break

        return result
    
##    @staticmethod
##    def RemoveUnavailableArticles(articles):
##        '''
##        Removes the unavailable articles.
##        Returns an Articles() object containing only available articles.
##        '''     
##        result = Articles("", None, None, None)
##     
##        for art1 in articles.articleList:
##            
##            if art1.available == "Active":
##                result.Add1(art1)
##                
##        return result

##    @staticmethod
##    def CopyArticlesAndSetStatus(articles, status):
##        '''
##        Creates a copy of the articles but sets the status as required.  
##        Returns an Articles() object with all updated articles.
##        '''
##               
##        result = Articles("", None, None, None)
##     
##        position=0
##        for art1 in articles.articleList:
##            result.Add1(art1)
##            result.articleList[position].status=""
##            
##            
##                
##        return result

    def __init__(self, params):
        '''
        Constructor
        '''
        

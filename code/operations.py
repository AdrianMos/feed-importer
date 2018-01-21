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
    

    def __init__(self, params):
        '''
        Constructor
        '''
        

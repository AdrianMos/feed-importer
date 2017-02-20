'''
Created on 26.04.2014

@author: Adrian Raul Mos
'''
import os.path
import sys
import logging
#add the current folder to the python paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from userinterface import UserInterface
from factory import Factory
from export import Export
from operations import Operations
import time


import tkinter as tk
from tkinter.ttk import *
from tkinter import Tk, StringVar, ttk

export = Export()

MSG_WARNING_LESS_50_ARTICLES = 'ATENTIE: Posibila eroare in datele '  + \
                               'furnizorului. Exista mai putin de 50 ' + \
                               'de articole.'

MSG_FEED_ERRORS = '\n\n***    Au fost gasite ERORI in feed. Exista ' + \
                  'articole neimportate. ANUNTATI distribuitorul. ' + \
                  'Detalii in log. Erori gasite:'



class Observable:
    def __init__(self, initialValue=None):
        self.data = initialValue
        self.callbacks = {}

    def addCallback(self, func):
        self.callbacks[func] = 1

    def delCallback(self, func):
        del self.callback[func]

    def _docallbacks(self):
        for func in self.callbacks:
             func(self.data)

    def set(self, data):
        self.data = data
        self._docallbacks()

    def get(self):
        return self.data

    def unset(self):
        self.data = None


class Model:
    def __init__(self):
        self.myMoney = Observable(0)
        self.canDownloadImages = Observable(False)
        #self.suppliersList = Observable('')
        #self.selectedSupplier
    
    def addMoney(self, value):
        self.myMoney.set(self.myMoney.get() + value)
        self.canDownloadImages.set(True)

    def removeMoney(self, value):
        self.myMoney.set(self.myMoney.get() - value)
        self.canDownloadImages.set(False)


class View(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        
        self.editDummy = tk.Entry(self, width=8)
        
        self.btnDownloadFeed = tk.Button(self, text='Descarca', width=10)
        self.btnProcess = tk.Button(self, text='Proceseaza')

        self.btnDownloadImages = tk.Button(self, text='Descarca imagini', state='disabled')

        self.editPathHaiducel = tk.Entry(self, state='readonly')
        self.editPathSupplier = tk.Entry(self, state='readonly')
        
        OPTIONS = [
            'Nancy (NAN)',
            'BabyDreams (HDRE)',
            'Bebex (BEB)',
            'BebeBrands (HBBA)',
            'BabyShops (HMER)',
            'KidsDecor (HDEC) - nu merge,',
            'Hubners (HHUB' ]
        
        self.selectedSupplier = StringVar()
        self.comboSupplier = tk.ttk.Combobox(self, values=OPTIONS, state='readonly', textvariable=self.selectedSupplier)
        self.comboSupplier.bind("<<ComboboxSelected>>", lambda event : print(str(self.selectedSupplier.get())))
        
        self.columnconfigure(1, weight=1)
        
        tk.Label(self, text='Actualizare date Haiducel').grid(columnspan=3)
        tk.Label(self, text='V 3.5, 25.09.2016').grid(columnspan=3)
        tk.Label(self, text='Actualizare: ').grid(sticky='e')
        tk.Label(self, text='Feed haiducel: ').grid(sticky='e')
        tk.Label(self, text='Feed distribuitor: ').grid(sticky='e')

        self.comboSupplier.grid(row=2, column=1, sticky='ew')
        self.comboSupplier.current(0)
        self.editPathHaiducel.grid(row=3, column=1, sticky='ew')
        self.editPathSupplier.grid(row=4, column=1, sticky='ew')
        self.btnDownloadFeed.grid(row=4, column=3)
        self.btnProcess.grid(column=1, columnspan=3, sticky='ew')
        self.btnDownloadImages.grid(column=1, columnspan=3, sticky='ew')
        self.editDummy.grid()
        
    def SetMoney(self, money):
        self.editDummy.delete(0,'end')
        self.editDummy.insert('end', str(money))

    def ActivateBtnDownloadImages(self, state):
        self.stateString = 'normal' if (state is True) else 'disabled'
        self.btnDownloadImages.config(state=self.stateString)
        print(self.stateString)


class Controller:
    def __init__(self, root):
        self.model = Model()
        self.model.myMoney.addCallback(self.MoneyChanged)
        self.model.canDownloadImages.addCallback(self.ActivateDownloadImage)
        self.view1 = View(root)
        self.view1.btnDownloadFeed.config(command=self.AddMoney)
        self.view1.btnProcess.config(command=self.RemoveMoney)
        self.MoneyChanged(self.model.myMoney.get())
        
    def AddMoney(self):
        self.model.addMoney(10)

    def RemoveMoney(self):
        self.model.removeMoney(10)

    def MoneyChanged(self, money):
        self.view1.SetMoney(money)

    def ActivateDownloadImage(self, state):
        self.view1.ActivateBtnDownloadImages(state)
        

def main():

    root = tk.Tk()
    root.withdraw()
    app = Controller(root)
    root.mainloop()


    
    factory = Factory()
    user = UserInterface()


    user.DisplayHeader()
    
    try:
    
        
        user.DisplayOptions()
        userInput = user.AskInput('Introduceti numarul optiunii: >> ')
        if userInput == '1':
            sys.exit('Program terminat.')
        
        feed = factory.CreateSupplierFeedObject(userInput)
        if feed is None:
            sys.exit('Optiune invalida. Program terminat.')
        
        InitLogFile(feed.code)
        
        print('  Procesare articole de tipul ' +
              feed.__class__.__name__ + '.')

                  
        if user.AskYesOrNo('Descarc date noi pentru acest furnizor?') == 'da':
            feed.DownloadFeed()
        
        
        user.Title(' IMPORT DATE FEED ')
        print('\n    Feed de la distributor: ' + feed.code)
        errors = feed.Import()
        if errors > 0:
            print(MSG_FEED_ERRORS + str(errors))
        
        feed.ConvertToOurFormat()
        print('    Articole importate: ' + str(feed.ArticlesCount()) + '. ' +
              'Erori: ' + str(errors))
       
        if feed.ArticlesCount() < 50:
            logging.error(MSG_WARNING_LESS_50_ARTICLES)
            
            if user.AskYesOrNo(MSG_WARNING_LESS_50_ARTICLES +
                               ' Continuati?') == 'nu':
                sys.exit('Ati renuntat la procesare.')
        user.HorizontalLine()
        
        
        user.Title(' SALVARE FEED FORMAT STANDARD ')
        filename = GenerateOutputFilename('Onlineshop', feed.code)
        export.ExportDataForOnlineshop(feed, filename)
        user.HorizontalLine()
        
        
        user.Title(' CURATARE FEED ')
        feed.RemoveCrapArticles()
        print('    Articole importate, dupa eliminare: ' + 
               str(feed.ArticlesCount()))
        user.HorizontalLine()
        
        
        user.Title(' IMPORT DATE HAIDUCEL ')
        print('    Filtru distribuitor: ' + feed.code)
        haiducelAllArticles = factory.CreateHaiducelFeedObject()
        haiducelAllArticles.Import()
        haiducelFiltered = haiducelAllArticles.FilterBySupplier(feed.code)
        print('    Articole importate: ' + 
              str(haiducelFiltered.ArticlesCount()))
        user.HorizontalLine()
        
        
        user.Title(' COMPARARI ')
        print('\n\nARTICOLE MODIFICATE')
        ProcessUpdatedArticles(haiducelFiltered, feed)
        
        print('\n\nARTICOLE NOI')
        newArticles = ProcessNewArticles(haiducelFiltered, feed)

        print('\n\nARTICOLE STERSE')
        ProcessArticlesForDeletion(haiducelFiltered, feed)
        user.HorizontalLine()
        
        
        user.Title(' DESCARCARE IMAGINI NOI ')
        if user.AskYesOrNo('Descarc imaginile pentru articolele noi?') == 'da':
            newArticles.DownloadImages();  
        user.HorizontalLine()
            
            
    except Exception as ex:
        print('\n\n Eroare: ' + repr(ex) + '\n')
        logging.error('main: ' + repr(ex))
      
   
    user.AskInput('\nApasati enter pentru iesire. >> ')
    print('\n*** Program terminat ***')


def ProcessUpdatedArticles (haiducelFeed, supplierFeed):
    
    updatedArticles, updateMessages = Operations.ExtractUpdatedArticles(
                                                     haiducelFeed,
                                                     supplierFeed)
    # Set the saving paths & code for the updated articles identical to 
    # the supplier's paths
    # The updated articles belong to the supplier.
    updatedArticles.paths = supplierFeed.paths    
    print('    Articole actualizate: '+ str(updateMessages.__len__())) 

    filename = GenerateOutputFilename('articole existente cu' + 
                                      ' pret sau status modificat',
                                      supplierFeed.code)
    export.ExportPriceAndAvailabilityAndMessages(updatedArticles, 
                                                  updateMessages, 
                                                  filename)
    return updatedArticles

def ProcessArticlesForDeletion (haiducelFeed, supplierFeed):
    
    removedArticles = Operations.SubstractArticles(haiducelFeed, supplierFeed)
    
    print('    Articole ce nu mai exista in feed: ' + 
          str(removedArticles.ArticlesCount()))
    export.ExportArticlesForDeletion(
                removedArticles,
                GenerateOutputFilename('articole de sters', supplierFeed.code))
    return removedArticles

def ProcessNewArticles (haiducelFeed, supplierFeed):
    
    newArticles = Operations.SubstractArticles(supplierFeed, haiducelFeed)
    newArticles = Operations.RemoveUnavailableArticles(newArticles)
    newArticles.paths = supplierFeed.paths
    print('    Articole noi in feed: ' + 
          str(newArticles.ArticlesCount()))
    export.ExportAllData(
                newArticles, 
                GenerateOutputFilename('articole noi', supplierFeed.code))
    return newArticles

def GenerateOutputFilename(name, code):
    return (code
            + '/out/' 
            + code 
            + ' ' + name + ' ' 
            + time.strftime('%Y-%m-%d')
            + '.csv')

def InitLogFile(code):
    filename = os.path.join(code, 'erori ' + code + '.log')
    logging.basicConfig(filename = filename,
                        level = logging.INFO, 
                        filemode = 'w',
                        format ='%(asctime)s     %(message)s')

if __name__ == '__main__':
    main()

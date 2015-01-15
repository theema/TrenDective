# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 19:39:45 2014

@author: Theema

12th January 2015 v5
"""
#import matplotlib
#matplotlib.use("TkAgg")

from matplotlib import pyplot as plt
from lxml import html
import requests
import numpy as np
import tkinter as tk
plt.style.use('bmh')
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
#from matplotlib.backend_bases import key_press_handler

def sectorGui(event):
    print("sectorGui")
    label = tk.Label(master, text="Which sector would you like to analize?")
    v = tk.StringVar() 
    #choices = ['AGRI', 'FOOD', 'FASHION', 'HOME', 'PERSON', 'BANK', 'FIN', 'INSUR', 'AUTO', 'IMM', 'PAPER', 'PETRO', 'PKG', 'STEEL', 'CONMAT', 'PROP', 'PF&REIT', 'CONS', 'ENERG', 'MINE', 'COMM', 'HELTH', 'MEDIA', 'PROF', 'TOURISM', 'TRANS', 'ETRON', 'ICT']
    entry =tk.OptionMenu(master, v, 'AGRI', 'FOOD', 'FASHION', 'HOME', 'PERSON', 'BANK', 'FIN', 'INSUR', 'AUTO', 'IMM', 'PAPER', 'PETRO', 'PKG', 'STEEL', 'CONMAT', 'PROP', 'PF&REIT', 'CONS', 'ENERG', 'MINE', 'COMM', 'HELTH', 'MEDIA', 'PROF', 'TOURISM', 'TRANS', 'ETRON', 'ICT' )     
    
    
    label.grid(row= 2)
    entry.grid(row =2, column = 1)
    global allEntry 
    allEntry = v
    return()
def fetch():
    print("fetch")
    print(allEntry.get())
    global entry 
    entry = allEntry.get()
    return(entry)
def scrape(url, struct):
    """scraping for data from the web
    takes url and xpath structure"""
    page = requests.get(url)
    tree = html.fromstring(page.text)
    values = tree.xpath(struct)# a list of strings
    return (values)
def reverse(alist):
    """reverse the order of a list and convert to float"""
    try:
        alist = [float(i) for i in alist]
    except ValueError:
        alist = [i for i in alist if i != '\xa0']
        alist = alist[::-1]#reverse order of list
    return(alist)
def plotline(stock, title, ROA, ROE, Prof, date):
    """plot ROA ROE Prof marginline graph"""
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    x=np.arange(len(ROA))
    plt.plot(x,ROA, label="ROA")
    plt.plot(x,ROE, label="ROE")
    plt.plot(x,Prof, label = "Prog Marg")
    ax.set_xticks(x)
    ax.set_xticklabels(date)
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    plt.axis('tight')
    plt.show()    
    return()
def multibar(stocklist, ROA, ROE, Prof, sector):
    """ creates multiple bar graph """        
    width= 0.3
    fig = plt.figure()
    x = np.arange(len(stocklist))
    ax = fig.add_subplot(1, 1, 1)
    rect1 = plt.bar(x, ROA, width, color ="c")
    rect2 = plt.bar(x+width, ROE, width, color= "m")
    rect3= plt.bar(x+width*2, Prof, width)
    ax.set_xticks(x+width*2)
    ax.set_xticklabels(stocklist)
    ax.legend( (rect1, rect2, rect3), ('ROA', 'ROE', 'Prof Marg') )
    plt.xlabel("stocks")
    plt.ylabel(" Ratio %")
    plt.title("Stocks'ratio comparison in "+sector+" Sector")
    #setting ticks style
    for tick in ax.xaxis.get_ticklabels():
        tick.set_fontsize('small')
        #tick.set_fontname('Times New Roman')
        tick.set_color('black')
        tick.set_weight('bold')
        """
    canvas = FigureCanvasTkAgg(fig, master)
    canvas.show()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2TkAgg( canvas, master )
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)"""
    plt.show()
def strtofloat(new):
    try:
        new = [float(i) for i in new]#convert strings in list to float
    except ValueError:
        new = [0]
    if new ==[]:
        new =[0]
    return (new)
def create(event):
    #get stocklist
    sector = fetch()
    url = 'http://www.settrade.com/C13_MarketSummaryIndustry.jsp?sector='+sector+'&industry=&market=SET'
    struct = '/html/body/div[2]//div[position()>6]/div/div[1]/a/text()'
    stocklist = scrape(url, struct)
    print (stocklist)
    ROA = []
    ROE =[]
    prof =[]
    for symbol in stocklist:
        Url = 'http://www.settrade.com/C04_03_stock_companyhighlight_p1.jsp?txtSymbol='+symbol+'&selectPage=3'
        ROAstruct = '//*[@id="cnt"]/div[1]/div[1]/div[5]/div[13]/div[8]/div[2]/text()'
        ROEstruct = '//*[@id="cnt"]/div[1]/div[1]/div[5]/div[13]/div[9]/div[2]/text()'
        profstruct = '//*[@id="cnt"]/div[1]/div[1]/div[5]/div[13]/div[10]/div[2]/text()'
        a = scrape(Url, ROAstruct)
        b= scrape(Url, ROEstruct)
        c = scrape(Url, profstruct)
        a = strtofloat(a)
        b = strtofloat(b)
        c = strtofloat(c)        
        
        ROA.extend(a)
        ROE.extend(b)
        prof.extend(c)
    
    print (ROA)#test
    multibar(stocklist, ROA, ROE, prof, sector)
    
    
        
        
master = tk.Tk()
master.title("VisualImpress")
allEntry = ""
entry =""

graphL= tk.Label(master, text ="Which type of graph would you like to look at")
graphL.grid(columnspan =2)

showB = tk.Button(master, text="Show")
showB.bind("<Button-1>", create)

showB.grid(row =3)

sectorB = tk.Button(master, text ="Sector ratio comparison")
sectorB.bind("<Button-1>", sectorGui)
sectorB.grid(row =1, column = 0)

    
master.mainloop()

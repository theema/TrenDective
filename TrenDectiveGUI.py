# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 19:39:45 2014

@author: Theema
TrenDective with GUI
8th March 2015 changes: combine three aspect of TrendDective together;sector, pie, trend
"""
#import matplotlib
#matplotlib.use("TkAgg")

from matplotlib import pyplot as plt
from lxml import html
import requests
import numpy as np
import tkinter as tk
from collections import OrderedDict
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
    showB = tk.Button(master, text="Show")
    showB.bind("<Button-1>", create)
    showB.grid(row =3, columnspan = 3 )
    global allEntry 
    allEntry = v
    return()
def pieGui(event):
    label = tk.Label(master, text ="what stock would you like to be pie:")
    label.grid(row=2)
    global allEntry
    allEntry = tk.StringVar() 
    entry = tk.Entry(master, textvariable=allEntry)
    entry.grid(row=2, column = 1)
    showB = tk.Button(master, text = "Show")
    showB.bind("<Button-1>", pie)
    showB.grid(row=3, columnspan = 3)
    return()
def trendGui(event):
    stockL = tk.Label(master, text = "which stock would you like to analyze")
    stockL.grid(row= 2)
    stockE= tk.Entry(master)
    stockE.grid(row = 2, column= 1)
    supS = tk.Scale(master, from_=0, to = 1, orient = tk.HORIZONTAL, resolution = 0.1 , label = "support line threshold:", length = 200)
    supS.grid(row = 3, columnspan = 3)
    resS = tk.Scale(master, from_=1, to = 2, orient =tk.HORIZONTAL, resolution= 0.1, label = "resistant line threshold:", length = 200)
    resS.grid(row = 4, columnspan = 3)
    def trendline(event):
        supT = supS.get()#get sup's threshold
        resT = resS.get()
        symbol = stockE.get()
        url = 'http://www.settrade.com/C04_02_stock_historical_p1.jsp?txtSymbol='+symbol+'&selectPage=3&max=124'
        print(url)#test    
        page = requests.get(url)
        tree = html.fromstring(page.text)

        struct='//*[@id="cnt"]/div[1]/div[1]/div[5]/div[3]//div[position()>2]/div[6]/text()'
        price = tree.xpath(struct)
        print(price)        
        Ch= [float(i) for i in price]#change prices from string to float
        Ch=Ch[::-1]#reverse the order of the list
        print (Ch)
        print("check")
        index= {}
        bef={}
        aft={}
        low={}
        high={}
        cut = len(Ch)
        #create dict index, the main dictionary for the stock price
        for k, v in enumerate(Ch[1:(cut-1)]): #number the prices in the list excluded first and last item
            print( k, v)
            index.update({k: v})#add the new item into the dict
        
        print (index)
        
        #create dict aft
        La = Ch[2:]#create a list without first two items
        for k, v in enumerate(La):
            aft.update({k:v})
        
        #create dict LHbef
        Lb = Ch[0:(cut-2)]#create a list without last two items
        for k, v in enumerate (Lb):
            bef.update({k:v})
                     
        #compare three values
        for k, v in index.items():
            #compare values to determine low turning point for support line
            if index[k] < bef[k] and index[k]<= aft[k] or index[k] <= bef[k] and index[k]< aft[k] : 
                print("true low")
                print (k, v)#for testing
                low.update({k:v})
           
        for k, v in index.items():
            #compare values to determine high turning point for resistant line
            if index[k] > bef[k] and index[k] >= aft[k] or index[k] >= bef[k] and index[k] > aft[k]: 
                print("true high")
                print (k, v)
                high.update({k:v})
                            
        
        def trend(Dict, Type, thres):  
            """establish trendline for Dict
            Type is either "sup" or "res"
            """
            count = 0
            countF=0
            fLine={}#store flat trendlines
            Line={}#store other trendlines
            for x, y  in Dict.items():
                print("***************************************************")
                print("first base value is ",str(x), str( y))
                for k, v in Dict.items():
                    if k>x :#only do the calculation for the values after the base value
                        print("second base value",str(k),str( v))
                        m = (v-y)/(k-x) #m is gradient rise over run
                        c = v-(m*k)
                        #price = mk + c
                        if m ==0:#if line is flat
                            print("!!!!!flat "+Type+" line establish!!!!!")
                            countF+=1
                            try:
                                fLine[c].update({x:y, k:v})
                            except KeyError:#error occur if key(y-intercept) doesn't exist
                                fLine[c]={x:y,k:v}#flat SUP line is stored as y-intercept for key and the day:price for values
                        for a, b in Dict.items():
                            if a>k:
                                price =m*a+c#price is the predicted value on the line
                                if b ==price:#check if point 'b' is on the line 
                                    print("!!!!!found "+Type+ " !!!!",str(a),str( b))
                                    count+=1
                                    try:
                                        Line[m,c].update({a:b})#add the coordinate to existing SUP line
                                    except KeyError:
                                        Line[m,c]={x:y, k:v, a:b}
                                    try:
                                        for e, f in Dict.items():#checking whether there are point that exceeds the line's threshold
                                            if e>x:
                                                if Type =="sup":
                                                    if f < (e*m+c)*thres:# when price is less than the expected threshold's price 
                                                            Line.pop((m,c))#remove that key and value
                                                            print( Type+" line exceed threshold")
                                                else:#Type =="res"
                                                    if f > (e*m+c)*thres:# when price is less than the expected threshold's price 
                                                            Line.pop((m,c))#remove that key and value
                                                            print( Type+"line exceed threshold")
                                    except KeyError:#error can occur if there are more than one price that exceed the threshold
                                        pass
            return(fLine, Line)
        
        #checking support trend lines
        input("continue?")
        print (low)
        low=OrderedDict(sorted(low.items()))
        supF, sup =trend(low, "sup", supT)
        
        #check for resistant trend lines
        high=OrderedDict(sorted(high.items()))
        resF, res = trend(high, "res", resT)                                  
                                        
        print("done, detecting resistant line finished  ")
        #showing the graph of the 'index' and plotting trend lines
        x =[]
        y=[]
        for k,  v in index.items():
            x.append(k)
            y.append(v)
        #defining a function for plotting a line from dict that has ={title:{x:y,x:y}}
        def plotDict(dict, color):
            
            for title, dataDict in dict.items():
                a= [ keys for keys, values in dataDict.items()]
                b= [ values for keys, values in dataDict.items()]
                plt.plot(a,b,color)
            return
        #plotting trendlines    
        plotDict(sup, color = 'g')
        plotDict(res, 'r')
        plotDict(supF, 'c--')
        plotDict(resF, 'm--')
          
        plt.plot(x, y,'b')#also checking whether low has detect correct values or not
        #graph label and title 
        plt.title(str(cut-2)+ " days graph for "+symbol)
        plt.xlabel("days")
        plt.ylabel("price in Baht")
        plt.show()
        return()
    showB = tk.Button(master, text = "Show")
    showB.bind("<Button-1>", trendline)
    showB.grid(row=5, columnspan = 3)
def pie(event):
    symbol = fetch(allEntry)

    url = 'http://www.settrade.com/C04_06_stock_financial_p1.jsp?txtSymbol='+symbol+'&selectPage=6'
    
    
    lis = '//*[@id="cnt"]/div[1]/div[1]/div[5]/div[2]/div[position()>0]/div[1]/text()'
    netdebt = '\xa0ÃÇÁË¹ÕéÊÔ¹'#code for total liabilities
    equi= '\xa0ÃÇÁÊèÇ¹¢Í§¼Ùé¶×ÍËØé¹'#total equity
    
    listly = scrape(url, lis )
    indL = listly.index(netdebt)#return index of the netdebt
    indE= listly.index(equi)#return index of equi
    postL = str(indL+5)
    postE = str(indE+5)
    
    lstruct = '//*[@id="cnt"]/div[1]/div[1]/div[5]/div[2]/div['+postL+']/div[2]/text()'
    liab= scrape(url, lstruct )
    estruct = '//*[@id="cnt"]/div[1]/div[1]/div[5]/div[2]/div['+postE+']/div[2]/text()'
    equity = scrape(url, estruct)
            
    e = float(equity[0].replace(',',''))#removing comma and convert to float
    print(e)
    l = float(liab[0].replace(',',''))
    #asset = e+l
    global frac
    frac = [e, l]
    labels = 'Equity', 'Liabilities'
    explode = (0, 0.1)
    colors = [ 'yellowgreen', 'lightcoral']
    def myAutopct(pct):#displaying both pct and values
        total=sum(frac)
        val=pct*total/100.0
        return '{p:.2f}%  ({v:,.2f})'.format(p=pct,v=val)
    
    plt.pie(frac, labels = labels, colors= colors, explode=explode, shadow = True, startangle = 90, autopct = myAutopct  )
    plt.axis('equal')
    plt.show()

def create(event):
    #get stocklist
    sector = fetch(allEntry)
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
def fetch(ent):
    print("fetch")
    print(ent.get())
    global entry 
    entry = ent.get()
    return(entry)
def scrape(url, struct):
    """scraping for data from the web
    takes url and xpath structure"""
    page = requests.get(url)
    tree = html.fromstring(page.text)
    values = tree.xpath(struct)# a list of strings
    return (values)

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

master = tk.Tk()
master.title("VisualImpress")
allEntry = ""
entry =""

graphL= tk.Label(master, text ="Which type of graph would you like to look at")
graphL.grid(columnspan =3)

sectorB = tk.Button(master, text ="Ratio comparison")
sectorB.bind("<Button-1>", sectorGui)
sectorB.grid(row =1, column = 0)

pieB = tk.Button(master, text= "FnSt Pie")
pieB.bind("<Button-1>", pieGui)
pieB.grid(row = 1, column = 1)

trendB = tk.Button(master, text = "Trendline")
trendB.bind("<Button-1>", trendGui)
trendB.grid(row = 1, column = 2)
   
master.mainloop()

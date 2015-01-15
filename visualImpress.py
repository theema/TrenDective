# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 21:31:55 2014

@author: Theema

program that display graphs for stock comparison
27th December 2014 v7
"""
from matplotlib import pyplot as plt
from lxml import html
import requests
import numpy as np
plt.style.use('bmh')
def ratioValues(ratio):
    """get the list of ratio values of stock in the list
    """
    count= 0
    value = []
    while count < len(stockList):
        symbol= stockList[count]
        url1= 'http://www.settrade.com/C04_03_stock_companyhighlight_p1.jsp?txtSymbol='+symbol+'&selectPage=3'
        page1 = requests.get(url1)
        tree1= html.fromstring(page1.text)
        if ratio == "ROA":
            struct1 = '//*[@id="cnt"]/div[1]/div[1]/div[5]/div[13]/div[8]/div[2]/text()'
        elif ratio == "ROE":
            struct1= '//*[@id="cnt"]/div[1]/div[1]/div[5]/div[13]/div[9]/div[2]/text()'
        elif ratio =="Prof Marg":
            struct1= '//*[@id="cnt"]/div[1]/div[1]/div[5]/div[13]/div[10]/div[2]/text()'
        new = tree1.xpath(struct1)
        try:
            new = [float(i) for i in new]#convert strings in list to float
        except ValueError:
            new = [0]
        if new ==[]:
            new =[0]
        value.extend(new)
        #print(value, symbol)
        count +=1

    return(value)

def growthPath(number):
    """number 8 =ROA 9=ROE 10 = prof marg """
    path ='//*[@id="cnt"]/div[1]/div[1]/div[5]/div[13]/div['+number+']/div[position()<7 and position()>1]/text()'
    values=tree.xpath(path)
    print(values)
    try:
        values = [float(i) for i in values]
    except ValueError:
        values = [i for i in values if i != '\xa0']
    values = values[::-1]#reverse order of list
    return(values)

graph= ""
while graph== "":
    graph = input("which type of graph would you like to see? sector, year, ratio comparison")
if graph == "sector" or graph=="ratio comparison":
    #grabing the stock symbols list in the sector
    sector= ""
    while sector == "":
        sector=input("which sector?")
    url = 'http://www.settrade.com/C13_MarketSummaryIndustry.jsp?sector='+sector+'&industry=&market=SET'
        
    page = requests.get(url)
    tree = html.fromstring(page.text)

    struct='/html/body/div[2]//div[position()>6]/div/div[1]/a/text()'
    stockList = tree.xpath(struct)
    print (stockList)
    x=np.arange(len(stockList))#number of stocks/bars
    print(x)
   
    #get the ratio% of each stock
    if graph == "sector":
        ratio = "" 
        while ratio =="":
            ratio=input("What ratio would you like to be graph?") 
        values= ratioValues(ratio)
        
        width= 0.4
        #plotting
        fig = plt.figure() # create a figure object
        ax = fig.add_subplot(1, 1, 1)# create an axes object in the figure
        plt.bar(x, values,width, color="c", align = "center")#plotting the graph
        ax.set_xticks(x)
        ax.set_xticklabels(stockList)#how many bar, label
    else:
        ratio = ""        
        ROA = ratioValues("ROA")
        ROE = ratioValues("ROE")
        Marg = ratioValues("Prof Marg")
        width= 0.3
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        rect1 = plt.bar(x, ROA, width, color ="c")
        rect2 = plt.bar(x+width, ROE, width, color= "m")
        rect3= plt.bar(x+width*2, Marg, width)
        ax.set_xticks(x+width*2)
        ax.set_xticklabels(stockList)
        ax.legend( (rect1, rect2, rect3), ('ROA', 'ROE', 'Prof Marg') )
    plt.xlabel("stocks")
    plt.ylabel(ratio+ "%")
    plt.title("Stocks'"+ratio+" in "+sector+" Sector")

elif graph == "yearly":
    symbol = ""
    while symbol =="":
        symbol = input("what symbol would you like to analize?")
    url= 'http://www.settrade.com/C04_03_stock_companyhighlight_p1.jsp?txtSymbol='+symbol+'&selectPage=3'
    page = requests.get(url)
    tree= html.fromstring(page.text)
    ROAgrowth = growthPath('8')
    ROEgrowth = growthPath('9')
    Profgrowth= growthPath('10')
    path= '//*[@id="cnt"]/div[1]/div[1]/div[5]/div[13]/div[1]/div[position()<7 and position()>1]/text()'
    tick=tree.xpath(path)
    tick = tick[:(len(ROAgrowth))]#cutting the date list to the same length as the values
    tick = tick[::-1]#reverse order
    #plotting
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    x=np.arange(len(ROAgrowth))
    ROA =plt.plot(x,ROAgrowth, label="ROA")
    ROE=plt.plot(x,ROEgrowth, label="ROE")
    Prof=plt.plot(x,Profgrowth, label = "Prog Marg")
    ax.set_xticks(x)
    ax.set_xticklabels(tick)
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
elif graph == "yearly prof":
    symbol1 = input("First symbol you would like to compare")
    symbol2 = input("Second symbol")
    url = 'http://www.settrade.com/C04_03_stock_companyhighlight_p1.jsp?txtSymbol='+symbol1+'&selectPage=3'
    
    #ax.legend((ROA, ROE, Prof),('ROA', 'ROE', 'Prof Marg') )

#prof marg 5 years comparison
#5-10 years commodity to transport and energy sector line graph
#def yearly(symbol, ratio):
 #   url = 'http://www.settrade.com/C04_03_stock_companyhighlight_p1.jsp?txtSymbol='+symbol1+'&selectPage=3'
    
#setting font properties for xticks
for tick in ax.xaxis.get_ticklabels():
    tick.set_fontsize('small')
    #tick.set_fontname('Times New Roman')
    tick.set_color('black')
    tick.set_weight('bold')
plt.axis('tight')
plt.show()    

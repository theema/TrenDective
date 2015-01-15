#Program to identify trend lines for stocks
#Created by Theema 16th August 2014
#9th December 2014 v18

from collections import OrderedDict
from lxml import html
import requests
import matplotlib.pyplot as plt
#stock = None
while True:
    try:
        #get the price list for the stock
        symbol = input("which stock would you like to analize?")
        url = 'http://www.settrade.com/C04_02_stock_historical_p1.jsp?txtSymbol='+symbol+'&selectPage=3&max=124'
        print(url)#test    
        page = requests.get(url)
        tree = html.fromstring(page.text)

        struct='//*[@id="cnt"]/div[1]/div[1]/div[5]/div[3]//div[position()>2]/div[6]/text()'
        price = tree.xpath(struct)
        date1 = tree.xpath('//*[@id="cnt"]/div[1]/div[1]/div[5]/div[3]/div[2]/div[1]/text()')#latest date
        date2 = tree.xpath('//*[@id="cnt"]/div[1]/div[1]/div[5]/div[3]/div[125]/div[1]/text()')#oldest date
        Ch= [float(i) for i in price]#change prices from string to float
        Ch=Ch[::-1]#reverse the order of the list
        print (Ch)
        print("check")
        
    
        break
    except:#catch all error
        print("No matching stock symbol was found.")

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
                    
#checking support trend lines
count = 0
countF=0

input("continue?")
print (low)
low=OrderedDict(sorted(low.items()))

supF ={}
sup={}

while True : 
    try:
                
        thres=float(input("please input desired values for support line's threshold(needs to be less than 1)"))
        while thres > 1:#keeps looping until user input thres that is less than 1
            thres=float(input("Value was greater than 1 \n please enter threshold value again"))
        break#break the loop
    
    except ValueError:#error raise when user hits enter with no value, or string 
        print("Did not accept a valid value")    
        

for x, y  in low.items():
    print("***************************************************")
    print("first base value is ",str(x), str( y))
    
    for k, v in low.items():
        if k>x :#only do the calculation for the values after the base value
            print("second base value",str(k),str( v))
            
            m = (v-y)/(k-x) #m is gradient rise over run
           # print ("gradient is " ,m)
            c = v-(m*k)
            #print ("y intercept is ",c)#price = mk + c
            
        
            if m ==0:#if line is flat
                print("!!!!!flat SUP line establish!!!!!")
                countF+=1
                try:
                    supF[c].update({x:y, k:v})
                except KeyError:
                    supF[c]={x:y,k:v}#flat SUP line is stored as count for key and the day:price for values
            for a, b in low.items():
                if a>k:
                    price =m*a+c#price is the predicted value on the line
                    #print(a, b)
                    if b ==price:#check if point 'b' is on the line 
                        #count+=1
                        print("!!!!!found SUP!!!!",str(a),str( b))
                       # input("third confirmed point")  
                        count+=1
                        try:
                            sup[m,c].update({a:b})#add the coordinate to existing SUP line
                        except KeyError:
                            
                            sup[m,c]={x:y, k:v, a:b}
                        #    input(str(sup[m,c])+"that didn't exist")
                        try:
                            
                            for e, f in low.items():#checking whether there are point that exceeds the line's threshold
                                if e>x:
                                    if f < (e*m+c)*thres:# when price is less than the expected threshold's price 
                                        
                                            sup.pop((m,c))#remove that key and value
                                            print("SUP line exceed threshold")
                        except KeyError:#error can occur if there are more than one price that exceed the threshold
                         #   print(KeyError)
                            pass
                    
print("done, Support line finished ",)
#sup ={k:v for k, v in sup.items() if len(v) > 2}
input("continue?")

#check for resistant trend lines
high=OrderedDict(sorted(high.items()))

resF ={}
res={}
while True : 
    try:
                
        thres=float(input("please input desired values for support line's threshold(needs to be greater than 1)"))
        while thres < 1:#keeps looping until user input thres that is greater than 1 
            thres=float(input("Value was less than 1\n please enter threshold value again"))
        break#break the loop
    
    except ValueError:#error raise when user hits enter with no value or string
        print("Did not accept a valid value") 
for x,y  in high.items():
    print("***************************************************")
    print("first base value is ",str(x), str( y))
    #print(x, y)#test if items is sorted    
    for k, v in high.items():
        if k>x :#only do the calculation for the day after the first base day
            print("second base value",str(k),str( v))
            m = (v-y)/(k-x) #m is gradient rise over run
            #print ("gradient is " ,m)
            c = v-(m*k)
            #print ("y intercept is ",c)#price = mk + c
            
            if m ==0:
                print("!!!!!flat RES line establish!!!!!")
                countF+=1
                try:
                    resF[c].update({x:y, k:v})
                except KeyError:
                    resF[c]={x:y,k:v}#flat RES line is stored as y-intercept for key and the day:price for values
            for a, b in high.items():
                if a>k:
                    price =m*a+c#price is the predicted value on the line
                    #print(a, b)
                    if b ==price:#check if point 'b' is on the line 
                        #count+=1
                        print("!!!!!found SUP!!!!",str(a),str( b))
                    #    input("third confirmed point")  
                        count+=1
                        try:
                            res[m,c].update({a:b})#add the coordinate to existing RES line
                        except KeyError:
                            
                            res[m,c]={x:y, k:v, a:b}
                     #       input(str(res[m,c])+"that didn't exist")
                        try:
                            
                            for e, f in high.items():#checking whether there are point that exceeds the line's threshold
                                if e>x:
                                    if f > (e*m+c)*thres:# when price is greater than the expected threshold's price 
                                        res.pop((m,c))#remove that key and value
                                        print("RES line exceed threshold")
                        except KeyError:#error can occur if there are more than one price that exceed the threshold
                      #      print(KeyError)
                            pass    
           
                                    
                                
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
#k=[e for e,f in high.items()]
#v =[f for e,f in high.items()]
  
plt.plot(x, y,'b')#also checking whether low has detect correct values or not
#graph label and title 
plt.title(str(cut-2)+ " days graph for "+symbol)
plt.xlabel("days")
plt.ylabel("price in Baht")
plt.show()

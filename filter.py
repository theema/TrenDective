#Program for filtering stocks base on user's criteria Part1
#Created by Theema 24th August 2014
#9th October 2014 v2
#Data retrieved 24th August 2014

valDict = {"ADVANC":823938.32, "BCP":572740.59, "BJC":72286.86, "CPF":679814.49,"GLOBAL":431847.34, "IVL":100837.94, "LH":363310.27, "PTTEP":281374.40, "SCC":854166.91, "TOP": 92786.79, "VGI":88900.76}
PEDict = {"ADVANC":17.7, "BCP":9.68, "BJC":38.96, "CPF":22.84, "GLOBAL":56.94, "IVL":51.61, "LH":17.75, "PTTEP":11.87, "SCC":15.07, "TOP":8.72, "VGI":40.42}
ROADict = {"ADVANC":38.45, "BCP":8.87, "BJC":7.37, "CPF":6.44, "GLOBAL": 6.05, "IVL":4.42, "LH":11.38, "PTTEP":15.37, "SCC":11.71, "TOP":8.99, "VGI":53.42}
ROEDict = {"ADVANC":74.53, "BCP":13.9, "BJC":13.57, "CPF":9.21, "GLOBAL":6.41, "IVL":4.20, "LH":18.87, "PTTEP":14.29, "SCC":21.55, "TOP":13.79, "VGI":60.82}

valFilt={}
PEFilt={}
ROAFilt={}
ROEFilt={}
#print ("{:,}".format(100000000))
#filtering stock base on value 
while valFilt == {}:#keep looping if no items fits the criteria
    minVal= input("Enter the minimum value for trading value NOTE:values are in mil baht")
    maxVal= input("Enter the maximum value for trading value NOTE: values are mil baht")
    #filter the valDict down to keys with values that are greater than minVal and less than maxVal
    valFilt = {k: v for k, v in valDict.items() if v > int(minVal) and v < int(maxVal)}

print ("stocks that met the trading value criteria" +str(valFilt))

#remove keys PEDict that doesnt exist in valFilt
PEDict = {k: v for k, v in PEDict.items() if k in set(valFilt.keys())}
print (PEDict)
while PEFilt =={}:
    minPE = input("Enter the minimum value for PE ratio")
    maxPE = input("Enter the maximum value for PE ratio")
    PEFilt = {k: v for k, v in PEDict.items() if v > int(minPE) and v < int(maxPE)}
print ("stocks that met the PE ratio criteria" + str(PEFilt))

ROADict = {k: v for k, v in ROADict.items() if k in set(PEFilt.keys())}
while ROAFilt=={}:
    minROA = input("Enter the minimum value for ROA percentage")
    ROAFilt = {k: v for k, v in ROADict.items() if v > int(minROA)}
print ("stocks that met the ROA criteria" + str(ROAFilt))

ROEDict = {k: v for k, v in ROEDict.items() if k in set(ROAFilt.keys())}
while ROEFilt=={}:
    minROE = input("Enter the minimum value for ROe percentage")
    ROEFilt = {k: v for k, v in ROEDict.items() if v > int(minROE)}
print ("stocks that met all the criterias" + str(ROEFilt))
    

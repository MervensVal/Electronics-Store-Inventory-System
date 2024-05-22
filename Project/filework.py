import secret
import os
import Product as p
import json

DIRECTORY = secret.rootPath

def Create_Reports_Folder():
    path = DIRECTORY + '/Reports'
    isExist = os.path.exists(path)
    if not isExist:
        os.mkdir(path)

#returns list or dictionary of [products objects]
def Extract_Products():
    path = DIRECTORY+'Products/'+'MOCK_DATA Products.json'
    f = open(path)
    data = json.load(f)
    for i in data:
       CategoryID = (str(data[i]['CategoryID']).replace("['","")).replace("']","")
       LocationID = (str(data[i]['LocationID']).replace("['","")).replace("']","")
       ProductName = (str(data[i]['ProductName']).replace("['","")).replace("']","")
       CPU_GHz = (str(data[i]['CPU_GHz']).replace("['","")).replace("']","")
       RAM_GB = (str(data[i]['RAM_GB']).replace("['","")).replace("']","")
       Storage_GB = (str(data[i]['Storage_GB']).replace("['","")).replace("']","")
       Price = (str(data[i]['Price']).replace("['","")).replace("']","")
       IsDefective = (str(data[i]['IsDefective']).replace("['","")).replace("']","")

       product = p.Product(CategoryID,LocationID,ProductName,CPU_GHz,RAM_GB,Storage_GB,Price,IsDefective)
       product.DisplayProduct()
    f.close()
def Create_Log_Folder():
    pass

def Save_Log_Data():
    pass

def Archive_File():
    pass

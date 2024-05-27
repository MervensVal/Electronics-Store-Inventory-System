import secret
import os
import Product as p
import json
import db

DIRECTORY = secret.rootPath

def Create_Reports_Folder():
    path = DIRECTORY + '/Reports'
    isExist = os.path.exists(path)
    if not isExist:
        os.mkdir(path)

#returns list of product objects
def Extract_Products():
    try:
        path = DIRECTORY+'Products/'+'MOCK_DATA Products.json'
        f = open(path)
        length  = len(f.readlines())
        f.close()
        f = open(path)
        data = json.load(f)
        
        products_list = []
        for i in range(length):
            CategoryID = data[i]['CategoryID']
            LocationID = data[i]['LocationID']
            ProductName = str(data[i]['ProductName']).replace("'","")
            CPU_GHz = data[i]['CPU_GHz']
            RAM_GB = data[i]['RAM_GB']
            Storage_GB = data[i]['Storage_GB']
            Price = data[i]['Price']
            IsDefective = data[i]['IsDefective']
            product = p.Product(CategoryID,LocationID,ProductName,CPU_GHz,RAM_GB,Storage_GB,Price,IsDefective)
            products_list.append(product)
        db.Insert_Products(products_list)
        f.close()
        return products_list
    except Exception as e:
        print(e)

def Create_Log_Folder():
    pass

def Save_Log_Data():
    pass

def Archive_File():
    pass

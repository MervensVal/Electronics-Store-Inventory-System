import queries as q
import pyodbc as odbc
import sys
import secret
import os
import Product as p
import json
from win32com import client 

DRIVER = 'SQL SERVER'
SERVER_NAME = '(local)'
DATABASE_NAME = 'Electronics_Store'

conn_string = f"""
Driver={DRIVER};
Server={SERVER_NAME};
Database={DATABASE_NAME};
Trusted_Connection=yes;
"""

DIRECTORY = secret.rootPath

def Create_Reports_Folder():
    try:
        path = DIRECTORY + '/Reports'
        isExist = os.path.exists(path)
        if not isExist:
            os.mkdir(path)
        print('Create_Reports_Folder created')
    except Exception as e:
        print('Error creating reports folder: ',e)
    
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
            product = p.Product(CategoryID,LocationID,ProductName,
                                CPU_GHz,RAM_GB,Storage_GB,Price,IsDefective)
            products_list.append(product)
        Insert_Products(products_list)
        f.close()
    except Exception as e:
        print('Error extracting products from file: ',e)

try:
    conn = odbc.connect(conn_string)
except Exception as e:
    print('DB Connection Error')
    print(e)
else:     
    def Create_Tables():
        cursor = conn.cursor()
        try:
            cursor.execute(q.Create_Category_Table)
            cursor.execute(q.Create_Contact_Table)
            cursor.execute(q.Create_Location_Table)
            cursor.execute(q.Create_Product_Table)
            cursor.execute(q.Create_Total_Inventory_Value_Table)
            cursor.commit()
            cursor.close()
            print('Create_Tables Done')
        except Exception as e:
            print('Error creating tables. Rollback Initiated: ',e)
            cursor.rollback()
            cursor.close()
            sys.exit()
            
    def Insert_Products(products_list):
        try:
            cursor = conn.cursor()
            temp = []
            for i in products_list:
                temp = [i.CategoryID,i.LocationID,i.ProductName,i.CPU_GHz,i.RAM_GB,i.Storage_GB,i.Price,i.IsDefective]
                cursor.execute(q.Insert_Poducts,temp)
            cursor.commit() 
            cursor.close()
            print('Extract_Products Done')
        except Exception as e:
            cursor.rollback()
            cursor.close()
            print('Error inserting products into SQL table. Rollback initiated: ',e)

    def Generate_Report1():
        try:
            cursor = conn.cursor()
            with open(DIRECTORY + '/Reports/' + 'Get_Products_Data.csv') as csvfile:
                cursor.execute(q.Get_Products_Data)
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([i[0] for i in cursor.description]) #write headers
                csv_writer.writerows(cursor)
                cursor.commit()
            cursor.close()
            print('Get_Products_Data report created')
        except Exception as e:
            cursor.close()
            print('Error creating "Get_Products_Data" report',e)

    def Generate_Report2():
        try:
            cursor = conn.cursor()
            filedir = DIRECTORY + '/Reports/' + 'Total_Price_Per_Location.csv'
            with open(filedir) as csvfile:
                cursor.execute(q.Refresh_Price_Per_Location)
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([i[0] for i in cursor.description]) #write headers
                csv_writer.writerows(cursor)
                cursor.commit()
            cursor.close()
            print('Total_Price_Per_Location report created')
           
            #Convert to PDF [pip install pywin32]
            excel = client.Dispatch("Excel.Application")
            sheets = excel.Workbooks.Open(filedir)
            work_sheets = sheets.Worksheets[0]
            work_sheets.ExportAsFixedFormat(0,'PDF File Path')
        except Exception as e:
            cursor.rollback()
            cursor.close()
            print('Error creating "Get_Products_Data" report',e)

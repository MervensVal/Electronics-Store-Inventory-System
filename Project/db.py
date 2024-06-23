import csv
import queries as q
import pyodbc as odbc
import sys
import secret
import os
import Product as p
import json
from win32com import client
import pandas as pd
import matplotlib.pyplot as plt

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
        print('Reports folder created')
    except Exception as e:
        print('Error creating reports folder: ',e)

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
            cursor.execute(q.Create_Index_Product_Table)
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
            print('Products extracted & inserted')
        except Exception as e:
            cursor.rollback()
            cursor.close()
            print('Error inserting products into SQL table. Rollback initiated: ',e)
            sys.exit()

    def Generate_Report1():
        try:
            filedir = DIRECTORY + 'Reports/' + 'Get_Products_Data.csv'
            cursor = conn.cursor()
            with open(filedir,'w') as csvfile:
                cursor.execute(q.Get_Products_Data)
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([i[0] for i in cursor.description]) #write headers
                csv_writer.writerows(cursor)
                cursor.commit()
            cursor.close()
            csvfile.close()
            print('Is csv file Get_Products_Data closed? : ',csvfile.closed)
            print('Get_Products_Data report created')
        except Exception as e:
            cursor.rollback()
            cursor.close()
            print('Error creating "Get_Products_Data" report',e)
            sys.exit()

    def Generate_Report2():
        try:
            filedir = DIRECTORY + 'Reports/' + 'Total_Price_Per_Location.csv'
            cursor = conn.cursor()
            cursor.execute(q.Refresh_Price_Per_Location)
            with open(filedir,'w') as csvfile:
                cursor.execute(q.Get_Price_Per_Location)
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([i[0] for i in cursor.description]) #write headers
                csv_writer.writerows(cursor)
                cursor.commit()
            cursor.close()
            csvfile.close()
            print('Is csv file Total_Price_Per_Location closed: ',csvfile.closed)
            print('Total_Price_Per_Location report created')
        except Exception as e:
            cursor.rollback()
            cursor.close()
            print('Error creating "Total_Price_Per_Location" report',e)
            sys.exit()

    def Excel_To_PDF():
        try:
            filedir = DIRECTORY + 'Reports/' + 'Total_Price_Per_Location.csv'
            excel_file_location = filedir.replace('/','\\')
            app = client.DispatchEx("Excel.Application")
            app.Interactive = False
            app.Visible = False
            workbook = app.Workbooks.Open(excel_file_location)
            output = os.path.splitext(excel_file_location)[0]
            workbook.ActiveSheet.ExportAsFixedFormat(0,output)
            workbook.Close()
            print('Total_Price_Per_Location PDF created')
        except Exception as e: 
            print('Error generating PDF from Total_Price_Per_Location Report: ', e)

    def Compare_Laptop_Desktop():
        try:
            filedir = DIRECTORY + 'Reports/' + 'Total_Price_Per_Location.csv'
            data = pd.read_csv(filedir)
            data_frame = pd.DataFrame(data)
            
            df_Desktop = data_frame[data_frame['CategoryName'] == 'Desktop']
            #print('\nDesktop - data frame is:\n',df_Desktop)
            sum = df_Desktop['TotalPrice'].sum()
            d_sum_round = round(sum)
            #print(d_sum_round)

            df_Laptop = data_frame[data_frame['CategoryName'] == 'Laptop']
            #print('\nLaptop - data frame is:\n',df_Laptop)
            sum = df_Laptop['TotalPrice'].sum()
            l_sum_round = round(sum)
            #print(l_sum_round)

            left = ['one','two']
            height = [d_sum_round,l_sum_round] #data
            tick_label = ['Desktop $'+str(d_sum_round),'Laptop $'+str(l_sum_round)]
            plt.bar(left,
                    height,
                    tick_label = tick_label,
                    width= 0.5,
                    color=['lightblue','deepskyblue']
                    )
            plt.xlabel('Devices')
            plt.ylabel('Total Price x $10,000')
            plt.title('Total Cost Per Device Type')
            plt.show()
        except Exception as e:
            print('Error creating Bar graph from Report 2',e)

def Extract_Products():
    try:
        path = DIRECTORY+'Project/Products/'+'MOCK_DATA Products.json'
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
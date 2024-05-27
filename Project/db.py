import queries as q
import pyodbc as odbc
import sys

DRIVER = 'SQL SERVER'
SERVER_NAME = '(local)'
DATABASE_NAME = 'Electronics_Store'

conn_string = f"""
Driver={DRIVER};
Server={SERVER_NAME};
Database={DATABASE_NAME};
Trusted_Connection=yes;
"""

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
        except Exception as e:
            print('Error creating tables. Rollback Initiated')
            cursor.rollback()
            cursor.close()
            sys.exit()
            
    #Pull data from fileWork
    def Insert_Products(products_list):
        cursor = conn.cursor()
        temp = []
        for i in products_list:
            temp = [i.CategoryID,i.LocationID,i.ProductName,i.CPU_GHz,i.RAM_GB,i.Storage_GB,i.Price,i.IsDefective]
            cursor.execute(q.Insert_Poducts,str(temp))
            #print(i.CategoryID,i.LocationID,i.ProductName,i.CPU_GHz,i.RAM_GB,i.Storage_GB,i.Price,i.IsDefective)
        cursor.close()

    def Generate_Report1():
        pass

    def Generate_Report2():
        pass
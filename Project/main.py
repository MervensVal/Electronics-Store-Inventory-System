import db
import time
import sys

try:
  start = time.time()
  db.Create_Reports_Folder()
  db.Create_Tables()
  db.Extract_Products()
  db.Generate_Report1()
  db.Generate_Report2()
  db.Excel_To_PDF()
  end = time.time()
  print('Total report generation execution time: ',
        round((end-start) * (10**3)), 'ms', ' || ',
        round((end-start)), 's')
  db.Compare_Laptop_Desktop()
  sys.exit()
except Exception as e:
  print("Error occured during program execution: ",e)
  sys.exit()
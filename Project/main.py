import db
import time

try:
  start = time.time()
  db.Create_Reports_Folder()
  db.Create_Tables()
  db.Extract_Products()
  db.Generate_Report1()
  db.Generate_Report2()
  db.Excel_To_PDF()
  end = time.time()
  print('Total report generation execution time: ',round((end-start) * (10**3)), 'ms')
  db.Compare_Laptop_Desktop()
except Exception as e:
  print("Error occured during program execution: ",e)
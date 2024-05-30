import db

try:
  db.Create_Reports_Folder()
  db.Create_Tables()
  db.Extract_Products()
except Exception as e:
  print("Error occured during program execution.")

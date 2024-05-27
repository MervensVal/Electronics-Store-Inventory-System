import filework as fw
import db

db.Create_Tables()
print('Create_Tables Done')
fw.Extract_Products()
print('Extract_Products Done')

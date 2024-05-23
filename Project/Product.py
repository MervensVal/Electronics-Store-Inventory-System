#Use OOP here.
from abc import ABC, abstractmethod

class FileData(ABC):
    @abstractmethod
    def Print_Data_Source(FileName,FileType):
        pass

class Product(FileData):
    try:
        def __init__(self,CategoryID,LocationID,ProductName,CPU_GHz,RAM_GB,Storage_GB,Price,IsDefective):
            self.CategoryID = CategoryID
            self.LocationID = LocationID
            self.ProductName = ProductName
            self.CPU_GHz = CPU_GHz
            self.RAM_GB = RAM_GB
            self.Storage_GB = Storage_GB
            self.Price = Price
            self.IsDefective = IsDefective
        
        def DisplayProduct(self,lineNumber):
            print(lineNumber,': ',self.CategoryID,' ',self.LocationID,' ',self.ProductName,' ',
                self.CPU_GHz,' ',self.RAM_GB,' ',self.Storage_GB,' ',self.Price,' ',self.IsDefective)
        
        def Print_Data_Source(self,FileName,FileType):
            print('Products data')
            print('FileName: ',  FileName)
            print('FileName: ',  FileType)
    except Exception as e:
        print(e)
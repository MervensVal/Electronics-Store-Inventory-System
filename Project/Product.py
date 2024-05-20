#Use OOP here.
from abc import ABC, abstractmethod

class FileData(ABC):
    @abstractmethod
    def Print_Data_Source(FileName,FileType):
        pass

class Product(FileData):
    def __init__(self,CategoryID,LocationID,ProductName,CPU_GHz,RAM_MB,Storage_GB,Price,IsDefective):
        self.CategoryID = CategoryID
        self.LocationID = LocationID
        self.ProductName = ProductName
        self.CPU_GHz = CPU_GHz
        self.RAM_MB = RAM_MB
        self.Storage_GB = Storage_GB
        self.Price = Price
        self.IsDefective = IsDefective
    
    def Print_Data_Source(self,FileName,FileType):
        print('Products data')
        print('FileName: ',  FileName)
        print('FileName: ',  FileType)

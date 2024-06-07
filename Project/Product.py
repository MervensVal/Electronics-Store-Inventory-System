class Product():
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
    except Exception as e:
        print(e)

"""Classes for Product System"""
class Product:
    def __init__(self,product_id: int, name: str, price: float):
        self.product_id = product_id
        self.name = name
        self.price = price
    def update_price(self, new_price: float):
        self.price = new_price
class Electronic(Product):
    def __init__(self, product_id: int, name: str, model : str, power: float ):
        super().__init__(product_id, name)
        self.model = model
        self.power = power
class Smartphone(Electronic):
    def __init__(self, product_id: int, name: str, model : str, power: float, memory:int, battery:int, os:str ):
        super().__init__(product_id,name,model,power)
        self.os = os
        self.battery = battery
        self.memory = memory
class Laptop(Electronic):
    def __init__(self, product_id: int, name: str, model : str, power: float, ram: int, processor:str,storage:int,screenSize:int):
        super().__init__(product_id,name,model,power)
        self.ram = ram
        self.processor = processor
        self.storage = storage

"""Classes for Storage system"""
class ShelfCell:
    def __init__(self,cell_id:int, max_quantity:int):
        self.cell_id = cell_id
        self.max_quantity = max_quantity
        self.quantity = 0
        self.product = None

    def store(self,product: Product,quantity: int) -> bool:
        if self.product is None:
            if quantity <= self.max_quantity:
                self.product = product
                self.quantity = quantity
                return True
            return False
        elif self.product.product_id==product.product_id:
            if self.quantity + quantity <= self.max_quantity:
                self.product = product
                return True
            return False
        else:
            return False

    def retrieve(self,quantity:int) -> bool:
        if self.quantity >= quantity:
            self.quantity -= quantity
            if self.quantity == 0:
                self.product = None
            return True
        return False

    def isAvailable(self) -> bool:
        return self.quantity < self.max_quantity

class Shelf:
    def __init__(self, shelf_id: int, num_cells: int, cell_capacity: int):
        self.shelf_id = shelf_id
        self.cells = [ShelfCell(i,cell_capacity) for i in range(num_cells)]

    def add_product(self,product: Product,quantity: int) -> int:
        for cell in self.cells:
            if cell.isAvailable() and (cell.product is None or cell.product.product_id == product.product_id):
                spaceAvailable = cell.max_quantity - cell.quantity
                spaceToStore = min(spaceAvailable,quantity)
                if spaceToStore > 0:
                    cell.store(product,spaceToStore)
                    quantity -= spaceToStore
                if quantity == 0:
                    return 0
        return quantity

    def get_product(self,product: Product,quantity:int) -> bool:
        for cell in self.cells:
            if cell.product and cell.product.product_id == product.product_id:
                if quantity == 0:
                    break
                take = min(cell.quantity,quantity)
                cell.retrieve(take)
                quantity -= take
        return quantity == 0

    def all_available(self,product: Product) -> int:
        totalAmount = 0
        for cell in self.cells:
            if cell.product and cell.product.product_id == product.product_id:
                totalAmount += cell.quantity
        return totalAmount

class Warehouse:
    def __init__(self,warehouse_id: int, name : str):
        self.warehouse_id = warehouse_id
        self.name = name
        self.shelves  = []

    def add_shelf(self,shelf: Shelf):
        self.shelves.append(shelf)
    def get_shelfnum(self,id: int) -> int:
        i = 0
        for shelf in self.shelves:
            if shelf.shelf_id == id:
                return i
            i+=1
        return 0

    def get_stock(self,product: Product) -> int:
        totalAmount = 0
        for shelf in self.shelves:
            if shelf.product and shelf.product.product_id == product.product_id:
                totalAmount += shelf.all_available(product)
        return totalAmount

    def find_product(self,product: Product):
        cellsOfProduct = []
        for shelf in self.shelves:
            for cell in shelf.cells:
                if cell.product and cell.product.product_id == product.product_id:
                    cellsOfProduct.append((shelf.shelf_id,cell.cell_id,cell.quantity))
        return cellsOfProduct

class StockManager:
    def __init__(self,warehouse: Warehouse):
        self.warehouse = warehouse

    def check_stock(self,product: Product) -> int:
        return self.warehouse.get_stock(product)

    def reserve (self,product: Product,quantity: int) -> bool:
        if self.check_stock(product) < quantity:
            return False
        for shelf in self.warehouse.shelves:
            if quantity == 0:
                break
            reserved = min(shelf.all_available(product),quantity)
            shelf.remove_product(product,reserved)
            quantity -= reserved
        return quantity == 0

    def replenish(self,product: Product,quantity: int) -> bool:
        if self.warehouse.get_stock(product) == 0:
            for shelf in self.warehouse.shelves:
                if quantity == 0:
                    break
                added = shelf.add_product(product,quantity)
                if added == 0:
                    return True
        else:
            shelfThatHave = self.warehouse.shelves[self.warehouse.find_product(product)[0]]
            if shelfThatHave.add_product(product,quantity) == 0:
                return True
            else:
                new_quantity = shelfThatHave.add_product(product, quantity)
                for shelf in self.warehouse.shelves:
                    if new_quantity == 0:
                        break
                    added = shelf.add_product(product,new_quantity)
                    if added == 0:
                        return True
        return quantity == 0


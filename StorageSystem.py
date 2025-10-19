#Address Class
class Address:
    def __init__(self, name: str, pos: float,spec: str):
        self.name = name
        self.pos = pos
        self.spec = spec
#Product Abstract Class
class Product:
    def __init__(self, product_id: int, name: str, price: float):
        self.product_id = product_id
        self.name = name
        self.price = price

    def update_price(self, new_price: float):
        self.price = new_price


class Electronic(Product):  #Абстрактный класс электроники
    def __init__(self, product_id: int, name: str, price: float, model: str, power: float):
        super().__init__(product_id, name, price)
        self.model = model
        self.power = power


class Smartphone(Electronic):  #Класс телефонов
    def __init__(self, product_id: int, name: str, price: float, model: str, power: float, memory: int, battery: int,
                 os: str):
        super().__init__(product_id, name, price, model, power)
        self.os = os
        self.battery = battery
        self.memory = memory


class Laptop(Electronic):  #Класс ноутбуков
    def __init__(self, product_id: int, name: str, price: float, model: str, power: float, ram: int, processor: str,
                 storage: int, screen_size: str):
        super().__init__(product_id, name, price, model, power)
        self.ram = ram
        self.processor = processor
        self.storage = storage
        self.screen_size = screen_size


"""Classes for Storage System"""


class ShelfCell:
    def __init__(self, cell_id: int, max_quantity: int):
        self.cell_id = cell_id
        self.max_quantity = max_quantity
        self.quantity = 0
        self.product = None

    def store(self, product: Product, quantity: int) -> bool:
        if self.product is None:
            if quantity <= self.max_quantity:
                self.product = product
                self.quantity = quantity
                return True
            return False
        elif self.product.product_id == product.product_id:
            if self.quantity + quantity <= self.max_quantity:
                self.quantity += quantity
                return True
            return False
        else:
            return False

    def retrieve(self, quantity: int) -> bool:
        if self.quantity >= quantity:
            self.quantity -= quantity
            if self.quantity == 0:
                self.product = None
            return True
        return False

    def is_available(self) -> bool:
        return self.quantity < self.max_quantity


class Shelf:
    def __init__(self, shelf_id: int, num_cells: int, cell_capacity: int):
        self.shelf_id = shelf_id
        self.cells = [ShelfCell(i + 1, cell_capacity) for i in range(num_cells)]

    def add_product(self, product: Product, quantity: int) -> int:
        for cell in self.cells:
            if cell.is_available() and (cell.product is None or cell.product.product_id == product.product_id):
                space_available = cell.max_quantity - cell.quantity
                space_to_store = min(space_available, quantity)
                if space_to_store > 0:
                    cell.store(product, space_to_store)
                    quantity -= space_to_store
                if quantity == 0:
                    return True
        return quantity == 0

    def get_product(self, product: Product, quantity: int) -> bool:
        for cell in self.cells:
            if cell.product and cell.product.product_id == product.product_id:
                if quantity == 0:
                    break
                take = min(cell.quantity, quantity)
                cell.retrieve(take)
                quantity -= take
        return quantity == 0

    def all_available(self, product: Product) -> int:
        total_amount = 0
        for cell in self.cells:
            if cell.product and cell.product.product_id == product.product_id:
                total_amount += cell.quantity
        return total_amount


class Warehouse:
    def __init__(self, warehouse_id: int, name: str,address_name:str):
        self.warehouse_id = warehouse_id
        self.name = name
        self.shelves = []
        self.address_name = address_name

    def add_shelf(self, shelf: Shelf):
        self.shelves.append(shelf)

    def get_stock(self, product: Product) -> int:
        total_amount = 0
        for shelf in self.shelves:
            total_amount += shelf.all_available(product)
        return total_amount

    def find_product(self, product: Product):
        cells_of_product = []
        for shelf in self.shelves:
            for cell in shelf.cells:
                if cell.product and cell.product.product_id == product.product_id:
                    cells_of_product.append((shelf.shelf_id, cell.cell_id, cell.quantity))
        return cells_of_product


class StockManager:
    def __init__(self, warehouse: Warehouse):
        self.warehouse = warehouse

    def check_stock(self, product: Product) -> int:
        return self.warehouse.get_stock(product)

    def reserve(self, product: Product, quantity: int) -> bool:
        if self.check_stock(product) < quantity:
            return False
        for shelf in self.warehouse.shelves:
            if quantity == 0:
                break
            reserved = min(shelf.all_available(product), quantity)
            shelf.get_product(product, reserved)
            quantity -= reserved
        return quantity == 0

    def replenish(self, product: Product, quantity: int) -> bool:
        remaining = quantity
        for shelf in self.warehouse.shelves:
            for cell in shelf.cells:
                if cell.product and cell.product.product_id == product.product_id:
                    space = cell.max_quantity - cell.quantity
                    to_add = min(space, remaining)
                    if to_add > 0:
                        cell.store(product, to_add)
                        remaining -= to_add
                        if remaining == 0:
                            return True
        for shelf in self.warehouse.shelves:
            for cell in shelf.cells:
                if cell.product is None and cell.is_available():
                    space = cell.max_quantity - cell.quantity
                    to_add = min(space, remaining)
                    if to_add > 0:
                        cell.store(product, to_add)
                        remaining -= to_add
                        if remaining == 0:
                            return True
        print(f"{product.name} не помещается на склад {self.warehouse.name}, оставшееся количество : {remaining}!!!!")
        return remaining == 0


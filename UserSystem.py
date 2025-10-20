from StorageSystem import Product, Warehouse, StockManager

"""Classes for Users System"""
class User:
    def __init__(self, user_id: int, name: str, surname: str, email: str, password: str,address_name: str):
        self.user_id = user_id
        self.name = name
        self.surname = surname
        self.address = address_name
        self.email = email
        self.password = password
        self.cart = Cart(self)
        self.orders = []

    def make_an_order(self, stock_manager): #stock_manager can be Warehouse or StockManager
        if self.cart.is_empty():
            print("Корзина пустая")
            return None
        if isinstance(stock_manager, Warehouse):
            stock_manager = StockManager(stock_manager)
        for product_id, quantity in self.cart.items.items():
            quantity_available = stock_manager.check_stock(product_id)
            if quantity_available == 0:
                print(f"Товара с айди {product_id} нет в наличии на складе {stock_manager.warehouse.name}")
                return False
            if quantity_available < quantity:
                print(f"Товара с айди {product_id} не достаточно на складе {stock_manager.warehouse.name}")
                return False
            if quantity_available >= quantity:
                if not stock_manager.reserve(product_id, quantity):
                    print(f"Товар с айди {product_id} не достаточно для резервации на складе {stock_manager.warehouse.name}")
                    stock_manager.release_reservation(product_id, quantity)
                    return False
                order = Order(self,stock_manager)
                self.orders.append(order)
                return True
        return False


    def add_product_to_cart(self, product: Product, quantity: int):
        self.cart.add_item(product, quantity)


class Cart:
    def __init__(self, user: User):
        self.user = user
        self.items = {}
        self.cost = 0

    def add_item(self, product: Product, quantity: int):
        self.items[product.product_id] = self.items.get(product.product_id, 0) + quantity
        self.cost += quantity * product.price

    def remove_item(self, product: Product):
        if product.product_id in self.items:
            quantity = self.items[product.product_id]
            self.cost -= quantity * product.price
            del self.items[product.product_id]

    def clear(self):
        self.cost = 0
        self.items = {}

    def is_empty(self):
        return self.items == {}

    def get_cost(self):
        return self.cost

class Order:
    def __init__(self, user: User, stock_manager: StockManager):
        self.user = user
        self.items = user.cart.items
        self.status = "Создан"
        self.cost = user.cart.cost
        self.stock_manager = stock_manager
        for item in self.items.keys():
            print(f"Товар c айди {item} в количестве {self.items[item]}шт. был зарезервирован "
                  f"для заказа пользователя {user.name}")

    def cancel_order(self):
        self.status = "Отменён"
        for item in self.items.keys():
            product_id = item
            quantity = self.items[item]
            self.stock_manager.release_reservation(product_id, quantity)

    def finish_order(self):
        self.status = "Получен"
        for item in self.items.keys():
            product_id = item
            quantity = self.items[item]
            self.stock_manager.finalize_reservation(product_id, quantity)


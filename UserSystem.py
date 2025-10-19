from StorageSystem import Product
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

    def make_an_order(self):
        if self.cart.is_empty():
            print("Корзина пустая")
            return None
        order = Order(self, self.cart)
        self.orders.append(order)
        self.cart.clear()
        return order

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
            self.cost -= self.items[product.product_id].items()[0] * product.price
            del self.items[product.product_id]

    def clear(self):
        self.cost = 0
        self.items = {}

    def is_empty(self):
        return self.items == {}

    def get_cost(self):
        return self.cost

class Order:
    def __init__(self, user: User, cart: Cart):
        self.user = user
        self.items = cart.items
        self.status = "Создан"
        self.cost = cart.cost
        for item in self.items.values():
            print(item)

    def update_status(self, new_status: str):
        self.status = new_status
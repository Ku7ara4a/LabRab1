from datetime import datetime
import logging

from StorageSystem import Product, Warehouse, StockManager
from CartsAndOrdersManager import OrderManager

logger = logging.getLogger(__name__)

"""Classes for Users System"""
class User:
    def __init__(self, user_id: int, name: str, surname: str, email: str, password: str,address_name: str):
        self.user_id = user_id
        self.name = name
        self.surname = surname
        self.address = address_name
        self.email = email
        self.password = password
        self.order_manager = OrderManager()
        self.cart = Cart(self)
        self.orders = []
        self._load_cart_from_file()
        self._load_orders_from_file()

    def _load_cart_from_file(self) -> None:
        cart_items = self.order_manager.load_cart(self.user_id)
        self.cart.items = cart_items.get('items',{}).copy()
        self.cart.cost = cart_items.get('cost',0)

    def _load_orders_from_file(self) -> None:
        self.orders = []
        orders_data = self.order_manager.get_orders_by_user_id(self.user_id)
        if orders_data:
            max_order_id = max(int(order_data['order_id']) for order_data in orders_data)
            if hasattr(Order,'_order_id_counter'):
                Order.set_order_id_counter(max(Order.get_order_id_counter(), max_order_id))
            else:
                Order.set_order_id_counter(max_order_id)
        for order_data in orders_data:
            order = Order.from_dict(self, order_data)
            self.orders.append(order)

    def make_an_order(self, stock_manager) -> bool:#stock_manager can be Warehouse or StockManager
        can_reserve_all = True
        if self.cart.is_empty():
            print("Корзина пустая")
            return False
        if isinstance(stock_manager, Warehouse):
            stock_manager = StockManager(stock_manager)
        for product_id, quantity in self.cart.items.items():
            quantity_available = stock_manager.check_stock(int(product_id))
            if quantity_available == 0:
                print(f"Товара с айди {product_id} нет в наличии на складе {stock_manager.warehouse.name}")
                can_reserve_all = False
                break
            if quantity_available < quantity:
                print(f"Товара с айди {product_id} не достаточно на складе {stock_manager.warehouse.name}")
                can_reserve_all = False
                break

        for product_id, quantity in self.cart.items.items():
            temp_available = 0
            for shelf in stock_manager.warehouse.shelves:
                for cell in shelf.cells:
                    if cell.product and cell.product.product_id == int(product_id):
                        temp_available += cell.quantity - cell.reserved

            if temp_available < quantity:
                print(f"Товар {product_id} нельзя зарезервировать: доступно {temp_available}, нужно {quantity}")
                can_reserve_all = False
                break

        if not can_reserve_all:
            print(f"Невозможно создать заказ: не все товары можно зарезервировать, "
                  f"корзина пользователя {self.name} была обнулена")
            self.cart.clear()
            return False

        try:
            order = Order(self, stock_manager)
            self.orders.append(order)
            order.save_to_file()
            self.cart.clear()
            self.order_manager.delete_cart(self.user_id)
            return True

        except Exception as e:
            logger.error(f"Exception occurred while making an order: {e}")
            return False

    def add_product_to_cart(self, product: Product, quantity: int) -> None:
        self.cart.add_item(product, quantity)
        self.cart.save_to_file()

class Cart:
    def __init__(self, user: User):
        self.user = user
        self.items = {} #{product_id : quantity}
        self.cost = 0

    def add_item(self, product: Product, quantity: int) -> None:
        product_id = str(product.product_id)
        file_quantity = self.items.get(product_id,0)
        self.items[product_id] = file_quantity + quantity
        self.cost += quantity * product.price
        self.save_to_file()

    def remove_item(self, product: Product) -> None:
        if product.product_id in self.items:
            quantity = self.items[product.product_id]
            self.cost -= quantity * product.price
            del self.items[product.product_id]
            self.save_to_file()

    def update_item_quantity(self, product: Product, new_quantity: int) -> None:
        product_id = str(product.product_id)
        if product_id in self.items.keys():
            old_quantity = self.items[product_id]
            self.cost -= old_quantity * product.price
            self.cost += new_quantity * product.price
            self.items[product_id] = new_quantity
            self.save_to_file()
        else:
            print(f"Товар {product.name} отсутствует в корзине {self.user.name}")

    def clear(self) -> None:
        self.cost = 0
        self.items = {}
        self.save_to_file()

    def is_empty(self) -> bool:
        return self.items == {}

    def get_cost(self) -> int:
        return self.cost

    def save_to_file(self) -> None:
        cart_items = {
            "items": self.items,
            "cost": self.cost
        }
        self.user.order_manager.save_cart(self.user.user_id, cart_items)

class Order:
    _order_id_counter = 0
    _initialized = False

    def __init__(self, user: User, stock_manager: StockManager):
        if not Order._initialized:
            Order._initialize_counter()

        Order._order_id_counter += 1
        self.order_id = Order._order_id_counter
        self.user = user
        self.items = user.cart.items
        self.status = "Создан"
        self.cost = user.cart.cost
        self.stock_manager = stock_manager
        self.stock_manager_id = stock_manager.stock_manager_id
        self.warehouse_id = stock_manager.warehouse.warehouse_id
        self.date = datetime.now().isoformat()
        for item in self.items.keys():
            stock_manager.reserve(int(item),self.items[item])
            logger.info(f"Товар c айди {item} в количестве {self.items[item]}шт. был зарезервирован "
                  f"со склада {self.warehouse_id} для заказа пользователя {user.name}")

    @classmethod
    def _initialize_counter(cls) -> None:
        try:
            order_manager = OrderManager()
            orders = order_manager.load_orders()
            if orders:
                max_id = max(int(order_id) for order_id in orders.keys())
                cls._order_id_counter = max_id
            else:
                cls._order_id_counter = 0
            cls._initialized = True
        except Exception as e:
            logging.error(f"Exception occurred while initializing counter: {e}")
            cls._initialized = True
            cls._order_id_counter = 0

    #I don't know how to annotate this one
    @classmethod
    def from_dict(cls, user:User, order_data:dict):
        order = cls.__new__(cls)
        order.order_id = int(order_data.get('order_id'))
        order.user = user
        order.items = order_data['items']
        order.status = order_data['status']
        order.cost = order_data['cost']
        order.date = order_data.get('date',datetime.now().isoformat())
        order.stock_manager_id = order_data.get('stock_manager_id')
        order.warehouse_id = order_data.get('warehouse_id')
        if order.order_id > Order._order_id_counter:
            Order._order_id_counter = order.order_id

        order._restore_stock_manager()

        return order #

    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "user_id": self.user.user_id,
            "status": self.status,
            "date": self.date,
            "items": self.items,
            "cost": self.cost,
            "stock_manager_id": self.stock_manager_id,
            "warehouse_id": self.warehouse_id
        }

    def save_to_file(self) -> None:
        self.user.order_manager.save_order(self.order_id,self.to_dict())

    def _restore_stock_manager(self) -> bool:
        from StorageSystem import StockManagerRegistry
        registry = StockManagerRegistry()
        if self.stock_manager_id:
            self.stock_manager = registry.get(self.stock_manager_id)
            return True
        if self.stock_manager is None and self.warehouse_id:
            self.stock_manager = registry.get_by_warehouse_id(self.warehouse_id)
            return True
        if self.stock_manager is None:
            logger.error(f"An error occurred while retrieving stock manager: {self.warehouse_id}")
            return False
        return True

    def cancel_order(self) -> None:
        if self.status == "Создан":
            self.status = "Отменён"
            for item in self.items.keys():
                product_id = int(item)
                quantity = int(self.items[item])
                self.stock_manager.release_reservation(product_id, quantity)
                self.save_to_file()
        else:
            print(f"Невозможно отменить заказ со статусом {self.status}")

    def finish_order(self) -> None:
        if self.status == "Создан":
            self.status = "Получен"
            for item in self.items.keys():
                product_id = int(item)
                quantity = int(self.items[item])
                self.stock_manager.finalize_reservation(product_id, quantity)
                self.save_to_file()
        else:
            print(f"Невозможно получить заказ со статусом {self.status}")

    @classmethod
    def get_order_id_counter(cls) -> int:
        return cls._order_id_counter

    @classmethod
    def set_order_id_counter(cls, count : int) -> None:
        cls._order_id_counter = count


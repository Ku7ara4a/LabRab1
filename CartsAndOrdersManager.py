import json
import os
from datetime import datetime

class OrderManager:
    def __init__(self, carts_file : str = "carts.json", orders_file : str = "orders.json"):
        self.carts_file = carts_file
        self.orders_file = orders_file
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        for file_path in [self.carts_file, self.orders_file]:
            if not os.path.exists(file_path):
                print(f"Файл {file_path} не существовал, создаю заново")
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump({}, file, ensure_ascii=False, indent=4)
            else:
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()
                        if not content.strip():
                            print(f"Файл {file_path} пустой, инициализирую")
                            with open(file_path, "w", encoding="utf-8") as f:
                                json.dump({}, f, ensure_ascii=False, indent=4)
                        else:
                            json.loads(content)
                except Exception as e:
                    print(f"Файл {file_path} поврежден, пересоздаю: {e}")
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump({}, f, ensure_ascii=False, indent=4)

    def save_cart(self, user_id: int, cart_items: dict) -> bool:
        try :
            with open(self.carts_file, "r", encoding="utf-8") as file:
                all_carts = json.load(file)
            all_carts[str(user_id)] = {
                'items': cart_items['items'],
                'cost': cart_items['cost'],
                'last_updated': datetime.now().isoformat()
            }

            with open(self.carts_file, "w", encoding="utf-8") as file:
                json.dump(all_carts, file,ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print("Ошибка сохранения корзины")
            return False

    def load_cart(self, user_id: int) -> dict:
        try :
            with open(self.carts_file, "r", encoding="utf-8") as file:
                all_carts = json.load(file)

            return all_carts.get(str(user_id), {'items': {}, 'cost': 0})
        except Exception as e:
            print("Ошибка загрузки корзины")
            return {'items': {}, 'cost': 0}

    def save_order(self, order_id: int, order_data: dict) -> bool:
        try :
            with open(self.orders_file, "r",encoding="utf-8") as file:
                all_orders = json.load(file)

            all_orders[str(order_id)] = order_data

            with open(self.orders_file, "w",encoding="utf-8") as file:
                json.dump(all_orders, file, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Ошибка сохранения заказов {e}")
            return False

    def load_orders(self) -> dict:
        try :
            with open(self.orders_file, "r",encoding="utf-8") as file:
                orders = json.load(file)
            return orders
        except Exception as e:
            print("Ошибка при загрузке заказов")
            return {}

    def get_orders_by_user_id(self, user_id: int) -> list:
        orders = self.load_orders()
        user_orders = []
        for order_id, order_data in orders.items():
            if order_data.get("user_id") == user_id:
                order_data['order_id'] = order_id
                user_orders.append(order_data)
        return user_orders

    def delete_cart(self, user_id: int) -> bool:
        try :
            with open(self.carts_file, "r", encoding="utf-8") as file:
                all_carts = json.load(file)

            if str(user_id) in all_carts:
                del all_carts[str(user_id)]

            with open(self.carts_file, "w", encoding="utf-8") as file:
                json.dump(all_carts, file)
            return True
        except Exception as e:
            print("Ошибка при удалении корзины")
            return False
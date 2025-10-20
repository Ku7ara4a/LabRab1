#Address Class
import json
import os
from itertools import product


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
        self.reserved = 0
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

    def reserve(self, quantity: int) -> bool:
        if self.quantity - self.reserved >= quantity:
            self.reserved += quantity
            return True
        return False

    def release(self,quantity: int) -> bool:
        self.reserved = max(0, self.reserved - quantity)

    def finalize(self,quantity: int) -> bool:
        if self.reserved >= quantity:
            self.quantity -= quantity
            self.reserved -= quantity

    def is_available(self) -> bool:
        return self.quantity < self.max_quantity


class Shelf:
    def __init__(self, shelf_id: int, num_cells: int, cell_capacity: int):
        self.shelf_id = shelf_id
        self.cells = [ShelfCell(i + 1, cell_capacity) for i in range(num_cells)]

    def add_product(self, product: Product, quantity: int) -> int:
        remaining = quantity
        for cell in self.cells:
            if cell.product and cell.product.product_id == product.product_id:
                if cell.quantity < cell.max_quantity:
                    space_available = cell.max_quantity - cell.quantity
                    to_store = min(space_available, remaining)
                    if cell.store(product, to_store):
                        remaining -= to_store
                        if remaining == 0:
                            return 0
        for cell in self.cells:
            if cell.product is None:
                to_store = min(cell.max_quantity, remaining)
                if cell.store(product, to_store):
                    remaining -= to_store
                    if remaining == 0:
                        return 0

        return remaining

    def get_product(self, product: Product, quantity: int) -> bool:
        for cell in self.cells:
            if cell.product and cell.product.product_id == product.product_id:
                if quantity == 0:
                    break
                take = min(cell.quantity, quantity)
                cell.retrieve(take)
                quantity -= take
        return quantity == 0

    def all_available(self, product_id: int) -> int:
        total_amount = 0
        for cell in self.cells:
            if cell.product and cell.product.product_id == product_id:
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

    def get_stock(self, product_id) -> int:
        total_amount = 0
        for shelf in self.shelves:
            total_amount += shelf.all_available(product_id)
        return total_amount

    def find_product(self, product: Product):
        cells_of_product = []
        for shelf in self.shelves:
            for cell in shelf.cells:
                if cell.product and cell.product.product_id == product.product_id:
                    cells_of_product.append((shelf.shelf_id, cell.cell_id, cell.quantity))
        return cells_of_product

    def to_dict(self):
        return {
            "warehouse_id": self.warehouse_id,
            "name": self.name,
            "address_name": self.address_name,
            "shelves": [
                {
                    "shelf_id": shelf.shelf_id,
                    "cells": [
                        {
                            "cell_id": cell.cell_id,
                            "product_id": cell.product.product_id if cell.product else None,
                            "product_name": cell.product.name if cell.product else None,
                            "quantity": cell.quantity,
                            "max_quantity": cell.max_quantity,
                            "reserved": cell.reserved
                        }
                        for cell in shelf.cells
                    ]
                }
                for shelf in self.shelves
            ]
        }


class StockManager:
    def __init__(self, warehouse: Warehouse):
        self.warehouse = warehouse
        self.data_file= "warehouses.json"

    def check_stock(self, product_id: int) -> int:
        return self.warehouse.get_stock(product_id)

    def reserve(self, product_id:int, quantity: int) -> bool:
        remaining = quantity
        for shelf in self.warehouse.shelves:
            for cell in shelf.cells:
                if cell.product and cell.product.product_id == product_id:
                    available = cell.quantity - cell.reserved
                    if available > 0:
                        to_reserve = min(available, remaining)
                        if cell.reserve(to_reserve):
                            remaining -= to_reserve
                            if remaining == 0:
                                self.save_to_json()
                                return True
        self.save_to_json()
        if remaining > 0:
            print(f"Не удалось зарезервировать товар с айди {product_id} не было зарезервировано {remaining}")
            return False
        return True

    def finalize_reservation(self,product: Product, quantity: int) -> bool:
        remaining = quantity
        product_id = product.product_id
        for shelf in self.warehouse.shelves:
            for cell in shelf.cells:
                if cell.product and cell.product.product_id == product_id:
                    if cell.reserved > 0:
                        to_finalize = min(cell.reserved, remaining)
                        if to_finalize > 0:
                            cell.quantity -= to_finalize
                            cell.reserved -= to_finalize
                            remaining -= to_finalize
                            if cell.quantity == 0:
                                cell.product = 0
                                cell.quantity = 0
                            if remaining == 0:
                                self.save_to_json()
                                return True
        self.save_to_json()
        if remaining > 0:
            print(f"Не удалось снять {product.name} в количестве {remaining} с резервации")
            return False
        return True

    def release_reservation(self, product_id, quantity) -> bool:
        remaining = quantity
        for shelf in self.warehouse.shelves:
            for cell in shelf.cells:
                if cell.product and cell.product.product_id == product_id:
                    to_release = min(remaining, cell.reserved)
                    cell.release(to_release)
                    remaining -= to_release
                    if remaining == 0:
                        print(f"Снято {quantity} шт. резерва товара {cell.product.name} на складе {self.warehouse.name}")
                        self.save_to_json()
                        return True
        self.save_to_json()
        return False

    def replenish(self, product: Product, quantity: int) -> bool:
        remaining = quantity
        for shelf in self.warehouse.shelves:
            for cell in shelf.cells:
                if cell.product and cell.product.product_id == product.product_id:
                    if cell.quantity < cell.max_quantity:
                        space = cell.max_quantity - cell.quantity
                        to_add = min(space, remaining)
                        if to_add > 0:
                            cell.quantity += to_add
                            remaining -= to_add
                            if remaining == 0:
                                self.save_to_json()
                                return True
        for shelf in self.warehouse.shelves:
            for cell in shelf.cells:
                if cell.product is None:
                    to_add = min(cell.max_quantity, remaining)
                    if to_add > 0:
                        if cell.store(product, to_add):
                            remaining -= to_add
                            if remaining == 0:
                                self.save_to_json()
                                return True
        self.save_to_json()
        if remaining > 0:
            print(f"Не удалось поместить товар {product.name} в количестве {remaining} на склад {self.warehouse.name}")
            return False
        return True

    def save_to_json(self):
        from FileManager import save_storage_data, load_storage_data
        data = load_storage_data()
        warehouse_dict = self.warehouse.to_dict()
        for i, wh in enumerate(data["warehouses"]):
            if wh["warehouse_id"] == self.warehouse.warehouse_id:
                data["warehouses"][i] = warehouse_dict
                save_storage_data(data)
                return
        data["warehouses"].append(warehouse_dict)
        save_storage_data(data)


class GlobalStockManager:
    def __init__(self, warehouses):
        self.warehouses = warehouses

    def reserve_product(self, product: Product, quantity) -> bool:
        remaining = quantity
        total_reserved = 0
        for wh in self.warehouses:
            if remaining <= 0:
                break
            manager = StockManager(wh)
            available = sum(
                (cell.quantity - cell.reserved)
                for shelf in wh.shelves
                for cell in shelf.cells
                if cell.product and cell.product.product_id == product.product_id
            )
            if available > 0:
                to_reserve = min(available, remaining)
                if manager.reserve(product, to_reserve):
                    reserved_here = sum(
                        cell.reserved
                        for shelf in wh.shelves
                        for cell in shelf.cells
                        if cell.product and cell.product.product_id == product.product_id
                    )
                    total_reserved += reserved_here
                    remaining = quantity - total_reserved
        if total_reserved == quantity:
            return True
        else:
            return False

    def release_reservation(self, product : Product, quantity):
        product_id = product.product_id
        remaining = quantity
        for wh in self.warehouses:
            manager = StockManager(wh)
            to_release = min(remaining, sum(cell.reserved for shelf in wh.shelves for cell in shelf.cells if cell.product and cell.product.product_id == product_id))
            manager.release_reservation(product, to_release)
            remaining -= to_release
            if remaining == 0:
                return True
        return False

    def finalize_reservation(self, product:Product, quantity):
        remaining = quantity
        total_finalized = 0
        for wh in self.warehouses:
            if remaining <= 0:
                break
            manager = StockManager(wh)
            reserved_here = 0
            for shelf in wh.shelves:
                for cell in shelf.cells:
                    if cell.product and cell.product.product_id == product.product_id:
                        reserved_here += cell.reserved
            if reserved_here > 0:
                to_finalized = min(reserved_here,remaining)
                if manager.finalize_reservation(product, to_finalized):
                    actual_finalized = to_finalized
                    total_finalized += actual_finalized
                    remaining = quantity - total_finalized
        if total_finalized == quantity:
            return True
        print(f"Недостаточно {product.name} на всех складах для снятия с резерва")
        return False
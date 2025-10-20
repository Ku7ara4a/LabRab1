from StorageSystem import *
from UserSystem import *
import xml.etree.ElementTree as ET
import json
import os

'''Working with users
Saving users to XML'''
def save_users_to_xml(users:list, filename:str):
    root = ET.Element("users")
    for user in users:
        user_elem = ET.SubElement(root, "user")
        ET.SubElement(user_elem, "user_id").text = str(user.user_id)
        ET.SubElement(user_elem, "name").text = user.name
        ET.SubElement(user_elem, "surname").text = user.surname
        ET.SubElement(user_elem, "email").text = user.email
        ET.SubElement(user_elem, "password").text = user.password
        ET.SubElement(user_elem, "address_name").text = user.address
    tree = ET.ElementTree(root)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    print(f"Пользователи сохранены в файл {filename}")

'''Updating users'''
def update_users_from_xml(new_users:list, filename: str):
    users = load_users_from_xml(filename)
    users += new_users
    save_users_to_xml(users, filename)
    print(f'Список пользователей в {filename} обновлён')

'''Loading users from XML'''
def load_users_from_xml(filename:str):
    tree = ET.parse(filename)
    root = tree.getroot()
    users = []
    for user_elem in root.findall("user"):
        user_id = int(user_elem.find("user_id").text)
        name = user_elem.find("name").text
        surname = user_elem.find("surname").text
        email = user_elem.find("email").text
        password = user_elem.find("password").text
        address_name = user_elem.find("address_name").text
        user = User(user_id, name, surname, email, password, address_name)
        users.append(user)
    return users

"""Load single user from XML"""
def load_single_users_from_xml(filename:str,user_id: int):
    tree = ET.parse(filename)
    root = tree.getroot()
    user : User
    for user_elem in root.findall("user"):
        loaded_user_id = int(user_elem.find("user_id").text)
        if user_id == loaded_user_id:
            name = user_elem.find("name").text
            surname = user_elem.find("surname").text
            email = user_elem.find("email").text
            password = user_elem.find("password").text
            address_name = user_elem.find("address_name").text
            user = User(loaded_user_id, name, surname, email, password, address_name)
    if user:
        print(f"Пользователь с айди {user_id} найден")
        return user
    else:
        print(f"Пользователь с айди {user_id} не существует")
        return None

"""Delete user by ID"""
def delete_user_by_id(user_id:int, filename:str):
    users = load_users_from_xml(filename)
    root = ET.Element("users")
    for user in users:
        if user.user_id != user_id:
            user_elem = ET.SubElement(root, "user")
            ET.SubElement(user_elem, "user_id").text = str(user.user_id)
            ET.SubElement(user_elem, "name").text = user.name
            ET.SubElement(user_elem, "surname").text = user.surname
            ET.SubElement(user_elem, "email").text = user.email
            ET.SubElement(user_elem, "password").text = user.password
            ET.SubElement(user_elem, "address_name").text = user.address
    tree = ET.ElementTree(root)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    print(f"Пользователь с айди {user_id} удалён из {filename}")


"""Work with Addresses
Loading Addresses from XML"""
def load_addresses_from_xml(filename:str):
    tree = ET.parse(filename)
    root = tree.getroot()
    addresses = []
    for address_elem in root.findall("address"):
        adress_name = address_elem.find("name").text
        address_pos = float(address_elem.find("position").text)
        address_spec = address_elem.find("spec").text
        address = Address(adress_name, address_pos,address_spec)
        addresses.append(address)
    return addresses

"""Updating Addresses"""
def update_addresses_from_xml(new_addresses:list, filename:str):
    addresses = load_addresses_from_xml(filename)
    addresses += new_addresses
    saving_addresses_to_xml(addresses, filename)
    print(f"Список Адресов в {filename} обновлён")

"""Saving Addresses to XML"""
def saving_addresses_to_xml(addresses:list, filename:str):
    root = ET.Element("addresses")
    for address in addresses:
        address_elem = ET.SubElement(root, "address")
        ET.SubElement(address_elem, "name").text = address.name
        ET.SubElement(address_elem, "position").text = str(address.pos)
        ET.SubElement(address_elem, "spec").text = address.spec
    tree = ET.ElementTree(root)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    print(f"Адреса сохранены в файл {filename}")

"""Loading single Address from XML"""
def load_single_address_from_xml(filename:str, address_name : str):
    tree = ET.parse(filename)
    root = tree.getroot()
    address : Address = None
    for address_elem in root.findall("address"):
        loaded_address_name = address_elem.find("name").text
        if loaded_address_name == address_name:
            address_pos = float(address_elem.find("position").text)
            spec = address_elem.find("spec").text
            address = Address(loaded_address_name, address_pos,spec)
    if address:
        print(f"Искомый адресс с названием {address_name} найден")
        return address
    else:
        print(f"Искомый адресс с названием {address_name} не существует")
        return None

"""Deliting Address by name"""
def deleting_address_by_name(name:str, filename:str):
    addresses = load_addresses_from_xml(filename)
    root = ET.Element("addresses")
    for address in addresses:
        if address.name != name:
            address_elem = ET.SubElement(root, "address")
            ET.SubElement(address_elem, "name").text = address.name
            ET.SubElement(address_elem, "position").text = str(address.pos)
            ET.SubElement(address_elem, "spec").text = address.spec
    tree = ET.ElementTree(root)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    print(f"Адрес {name} удалён из {filename}")

"""Work with Product and Storage"""

storage_data = "warehouses.json"

def load_storage_data():
    if not os.path.exists(storage_data):
        print("Файл не существует, создаю заново")
        return {"warehouses": []}
    if os.path.getsize(storage_data) == 0:
        print("Файл пуст, создаю заново")
        return {"warehouses": []}
    try:
        with open(storage_data, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError as e:
        print(f"Ошибка чтения JSON: {e}")
        print("Файл повреждён, создаю пустой файл")
        return {"warehouses": []}

def save_storage_data(data : dict):
    with open(storage_data, "w",encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

"""Creating one warehouse in JSON"""
def create_warehouse(warehouse: Warehouse):
    warehouse_id = warehouse.warehouse_id
    name = warehouse.name
    address_name = warehouse.address_name
    data = load_storage_data()
    if any(wh["warehouse_id"] == warehouse_id for wh in data["warehouses"]):
        print("Склад существует, файл не перезаписан")
        return None
    data["warehouses"].append({"warehouse_id": warehouse_id, "name": name, "address_name":address_name, "shelves": [] })
    print(f"Склад с айди {warehouse_id} был создан")
    print(data)
    save_storage_data(data)

"""Creating one shelf in warehouse (JSON)"""
def create_shelf(warehouse_id: int, shelf: Shelf):
    data = load_storage_data()

    for wh in data["warehouses"]:
        if int(wh["warehouse_id"]) == warehouse_id:
            shelf_exists = False
            for i, existing_shelf in enumerate(wh["shelves"]):
                if existing_shelf["shelf_id"] == shelf.shelf_id:
                    for j, existing_cell in enumerate(existing_shelf["cells"]):
                        if existing_cell["product_id"] is None:
                            if j < len(shelf.cells):
                                cell = shelf.cells[j]
                                existing_shelf["cells"][j] = {
                                    "cell_id": cell.cell_id,
                                    "product_id": cell.product.product_id if cell.product else None,
                                    "product_name": cell.product.name if cell.product else None,
                                    "quantity": cell.quantity,
                                    "max_quantity": cell.max_quantity,
                                    "reserved": cell.reserved
                                }
                    shelf_exists = True
                    break
            if not shelf_exists:
                shelf_dict = {
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
                wh["shelves"].append(shelf_dict)

            save_storage_data(data)
            print(f"Полка {shelf.shelf_id} создана/обновлена на складе {warehouse_id}")
            return
    raise ValueError(f"Склад с айди {warehouse_id} не найден")

"""Searching in all of the warehouses"""
def search_product(product_id:int):
    data = load_storage_data()
    locations = []
    for wh in data["warehouses"]:
        for shelf in wh["shelves"]:
            for cell in shelf["cells"]:
                if cell["product_id"] == product_id:
                    locations.append({
                        "warehouse_id": wh["warehouse_id"],
                        "shelf_id": shelf["shelf_id"],
                        "cell_id": cell["cell_id"],
                        "quantity": cell["quantity"],
                        "reserved": cell["reserved"]
                    })
    return locations

"""Getting total stock"""
def get_total_stock(product_id:int):
    total_quantity = 0
    for location in search_product(product_id):
        total_quantity += location["quantity"]
    return total_quantity

"""Working with product system"""

PRODUCTS_FILE = "products.json"

class ProductManager:
    def __init__(self):
        self.products = {}
        self.load_products()

    def get_product_list(self):
        return self.products.values()

    def load_products(self):
        if not os.path.exists(PRODUCTS_FILE):
            with open(PRODUCTS_FILE, "w",encoding="utf-8") as f:
                json.dump({"products": []},f)
        with open(PRODUCTS_FILE,"r",encoding="utf-8") as f:
            data = json.load(f)
        self.products.clear()
        for p in data.get("products", []):
            obj = self.dict_to_product(p)
            self.products[obj.product_id] = obj

    def save_products(self):
        data = {"products": [self.product_to_dict(p) for p in self.products.values()]}
        with open(PRODUCTS_FILE,"w",encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False,indent=4)

    def add_product(self,product: Product):
        self.products[product.product_id] = product
        self.save_products()

    def get_product(self, product_id:int):
        return self.products.get(product_id)

    def delete_product(self, product_id:int):
        if product_id in self.products:
            del self.products[product_id]
            self.save_products()

    def update_price(self, product_id, new_price):
        product = self.get_product(product_id)
        if product:
            product.update_price(new_price)
            self.save_products()

    def dict_to_product(self, product):
        if product["specific"] == "Smartphone":
            return Smartphone(
                product["product_id"],product["name"],product["price"],product["model"],
                product["power"],product["memory"],product["battery"],product["os"]
            )
        elif product["specific"] == "Laptop":
            return Laptop(
                product["product_id"],product["name"],product["price"],product["model"],
                product["power"],product["ram"],product["processor"],product["storage"],
                product["screen_size"]
            )
        elif product["specific"] == "Electronic":
            return Electronic(
                product["product_id"],product["name"],product["price"],product["model"],
                product["power"]
            )
        else :
            return Product(
                product["product_id"],product["name"],product["price"]
            )
    def product_to_dict(self, product):
        base = {
            "product_id": product.product_id,
            "name": product.name,
            "price": product.price,
            "specific": product.__class__.__name__
        }
        if isinstance(product, Electronic):
            base.update({
                "model": product.model,
                "power": product.power,
            })
        if isinstance(product, Smartphone):
            base.update({
                "battery": product.battery,
                "memory": product.memory,
                "os": product.os,

            })
        if isinstance(product, Laptop):
            base.update({
                "processor": product.processor,
                "ram": product.ram,
                "storage": product.storage,
                "screen_size": product.screen_size,
            })
        return base
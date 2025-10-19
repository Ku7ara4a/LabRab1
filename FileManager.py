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
            address_name = user_elem.find("addresses").text
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
        print("Файл повреждён — возвращаю пустую структуру")
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
        """raise ValueError(f"Склад с айди {warehouse_id} уже существует, пересоздайте файл warehouses " # если убрать Return, то будет выдавать преднаписанную ошибку
                         f"или уберите часть кода с созданием складов")"""
    data["warehouses"].append({"warehouse_id": warehouse_id, "name": name, "address_name":address_name, "shelves": [] })
    print(f"Склад с айди {warehouse_id} был создан")
    print(data)
    save_storage_data(data)

"""Creating one shelf in warehouse (JSON)"""
def create_shelf(warehouse_id: int, shelf: Shelf):
    shelf_id = shelf.shelf_id
    num_cells = len(shelf.cells)
    cell_capacity = shelf.cells[0].max_quantity
    data = load_storage_data()
    for wh in data["warehouses"]:
        if int(wh["warehouse_id"]) == warehouse_id:
            if any(sh["shelf_id"] == shelf_id for sh in wh["shelves"]):
                print("Полка существует, файл не перезаписан")
                return None
                """raise ValueError(f"Полка с айди {shelf_id} уже существует") # если убрать break, то будет выдавать преднаписанную ошибку"""
            shelf = {
                "shelf_id": shelf_id,
                "cells" : [{"cell_id": i + 1, "product_id" : None , "quantity" : 0 , "max_quantity" : cell_capacity}
                           for i in range(num_cells)],
            }
            wh["shelves"].append(shelf)
            save_storage_data(data)
            return shelf
    raise ValueError(f"Склад с айди {warehouse_id} не найден")

"""Updating cell"""
def update_cell(warehouse_id:int, shelf_id:int, cell_id:int, product_id = None , quantity = 0):
    data = load_storage_data()
    for wh in data["warehouses"]:
        if wh["warehouse_id"] == warehouse_id:
            for shelf in wh["shelves"]:
                if shelf["shelf_id"] == shelf_id:
                    for cell in shelf["cells"]:
                        if cell["cell_id"] == cell_id:
                            if product_id is not None:
                                cell["product_id"] = product_id
                            if quantity > 0:
                                cell["quantity"] = min(cell["max_quantity"], quantity)
                            save_storage_data(data)
                            return cell
    print("Не удалось обновить ячейку")
    return None

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
                    })
    return locations

"""Getting total stock"""
def get_total_stock(product_id:int):
    total_quantity = 0
    for location in search_product(product_id):
        total_quantity += location["quantity"]
    return total_quantity
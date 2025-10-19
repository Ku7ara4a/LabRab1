from StorageSystem import *
from UserSystem import *
import xml.etree.ElementTree as ET

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

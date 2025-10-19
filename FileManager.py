from main import *
import xml.etree.ElementTree as ET

'''Saving users to XML'''
def save_users_to_xml(users, filename):
    root = ET.Element("users")
    for user in users:
        user_elem = ET.SubElement(root, "user")
        ET.SubElement(user_elem, "user_id").text = str(user.user_id)
        ET.SubElement(user_elem, "name").text = user.name
        ET.SubElement(user_elem, "surname").text = user.surname
        ET.SubElement(user_elem, "email").text = user.email
        ET.SubElement(user_elem, "password").text = user.password
        addresses_elem = ET.SubElement(user_elem, "addresses")
        for address in user.addresses:
            ET.SubElement(addresses_elem, "address").text = address
    tree = ET.ElementTree(root)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    print(f"Пользователи сохранены в файл {filename}")

'''Loading users from XML'''
def load_users_from_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    users = []
    for user_elem in root.findall("user"):
        user_id = int(user_elem.find("user_id").text)
        name = user_elem.find("name").text
        surname = user_elem.find("surname").text
        email = user_elem.find("email").text
        password = user_elem.find("password").text
        user = User(user_id, name, surname, email, password)
        addresses_elem = user_elem.find("addresses")
        if addresses_elem is not None:
            for addr_elem in addresses_elem.findall("address"):
                user.addresses.append(addr_elem.text)
        users.append(user)
    return users




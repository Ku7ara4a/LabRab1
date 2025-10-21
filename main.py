from FileManager import *

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler() # Turn if Test, Off if user
    ]
)

'''Creating address list and saving it to file'''
addresses = [Address("H1",10,"Living"),
             Address("H2",20,"Living"),
             Address("H3",30,"Living"),
             Address("WH1",0,"Warehouse"),
             Address("WH2",40,"Warehouse"),]
saving_addresses_to_xml(addresses, "addresses.xml")

"""Creating warehouse list and saving them to file"""
warehouses = [Warehouse(1,"Warehouse1","WH1"),
              Warehouse(2,"Warehouse2","WH2")]

for wh in warehouses:
    create_warehouse(wh)

"""Creating managers for warehouses"""
manager1 = StockManager(warehouses[0])
manager2 = StockManager(warehouses[1])

"""User list and saving them to file"""
users = [User(1,"Denis","Chaban","arxwoodj@gmail.com","notgonnasay","H1"),
         User(2,"Ivan","Ivanov","IvanovIvanIvanovich@ivan.ru","Vanya","H2"),
         User(3,"IDK","IDKOVICH","ILostMyCreativity@sad.com","Smth","H3")]
save_users_to_xml(users, "users.xml")

"""Shelves needs to go after warehouses"""
shelves = [Shelf(1,3,10),
           Shelf(2,5,4),
           Shelf(3,5,3),
           Shelf(4,2,5)]

for i in range(len(shelves)):
    if i % 2 == 0:
        warehouses[0].add_shelf(shelves[i])
    else:
        warehouses[1].add_shelf(shelves[i])

for i in range(len(shelves)):
    if i % 2 == 0:
        create_shelf(1, shelves[i])
    else:
        create_shelf(2, shelves[i])

#Working with products
product_manager = ProductManager()

product1 = Laptop(1,"Ноутбук Леново",100240,"LapTop-001",220,16,"Intel-CoreI5",512,"1920x1024")
product2 = Smartphone(2,"Телефон Крутофон",36000,"VeryCleverPhone",20,256,6000,"MOC")
product3 = Electronic(3,"Видеокарта",55000,"RTX-5090",575)

#Adding product to manager
product_manager.add_product(product1)
product_manager.add_product(product2)
product_manager.add_product(product3)

"""global_manager = GlobalStockManager(warehouses) #May delete this
"""

#Replanishing Products to warehouses (there is some more than it can fit)
manager1.replenish(product1, 15)
manager2.replenish(product1, 10)
manager2.replenish(product2, 6)
manager1.replenish(product2, 30)
manager1.replenish(product1, 20)

#Playing with carts
"""print("Работа функции изменения количества товара в корзине")
Ivan = users[1]
Ivan.add_product_to_cart(product1, 3)
print("Содержимое корзины")
print(Ivan.cart.items)
Ivan.cart.update_item_quantity(product1,10)
Ivan.add_product_to_cart(product2,3)
print("Содержимое корзины")
print(Ivan.cart.items)"""

#Playing with Orders
print("Работа системы заказов. Количество товара на складе можно посмотреть"
      " в файле warehouses.json")
Denis = users[0]
Denis.add_product_to_cart(product1, 20)
Denis.add_product_to_cart(product2, 3)
print("Содержимое корзины до создания заказа")
print(Denis.cart.items)

input("Enter any key to continue...")
Denis.make_an_order(warehouses[0])
print("Содержимое корзины после создания заказа")
print(Denis.cart.items)

input("Enter any key to continue...")
Denis.orders[-1].finish_order()

manager1.save_to_json()
manager2.save_to_json()
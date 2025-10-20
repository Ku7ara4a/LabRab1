from FileManager import *

'''Testing and uploading some random persons and houses from MiniHomeTown.png'''
addresses = [Address("H1",10,"Living"),
             Address("H2",20,"Living"),
             Address("H3",30,"Living"),
             Address("WH1",0,"Warehouse"),
             Address("WH2",40,"Warehouse"),]
saving_addresses_to_xml(addresses, "addresses.xml")

users = [User(1,"Denis","Chaban","arxwoodj@gmail.com","notgonnasay","H1"),
         User(2,"Ivan","Ivanov","IvanovIvanIvanovich@ivan.ru","Vanya","H2"),
         User(3,"IDK","IDKOVICH","ILostMyCreativity@sad.com","Smth","H3")]
save_users_to_xml(users, "users.xml")

'''Test of storage system'''
#Creating warehouses
warehouses = [Warehouse(1,"Warehouse1","WH1"),
              Warehouse(2,"Warehouse2","WH2")]

for wh in warehouses:
    create_warehouse(wh)

#Creating shelves and giving them to warehouses
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

#Adding product to manager
product_manager.add_product(product1)
product_manager.add_product(product2)

#Making manager to controll warehouses
manager1 = StockManager(warehouses[0])
manager2 = StockManager(warehouses[1])
global_manager = GlobalStockManager(warehouses)

#Replanishing Products to warehouses (there is some more than it can fit)
manager1.replenish(product1, 15)
manager2.replenish(product1, 10)
manager1.replenish(product2, 30)
manager1.replenish(product1, 20)

#Reserving in one warehouse
"""manager1.reserve(product1,35)
n = input()
manager1.release_reservation(product1,20)
"""

#Global reserving
"""global_manager.reserve_product(product1,25)
global_manager.finalize_reservation(product1,25)
"""

#Checking products
"""print("Проверка количества продуктов на всех складах:")
for wh in warehouses:
    print(f"Склад {wh.name}")
    for product in product_manager.get_product_list():
        print(f"{product.name} х {wh.get_stock(product)}")
"""

#Making an order
Denis = users[0]
Denis.add_product_to_cart(product1, 7)
Denis.make_an_order(manager1)


#Final saving
manager1.save_to_json()
manager2.save_to_json()

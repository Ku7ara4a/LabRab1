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


warehouses = [Warehouse(1,"Warehouse1","WH1"),
              Warehouse(2,"Warehouse2","WH2")]
shelves = [Shelf(1,3,10,),
           Shelf(2,5,4,),
           Shelf(3,5,3,),
           Shelf(4,2,5,),]

for wh in warehouses:
    create_warehouse(wh)

for i in range(len(shelves)):
    if i % 2 == 0:
        create_shelf(1,shelves[i])
        warehouses[0].add_shelf(shelves[i])
    else:
        create_shelf(2,shelves[i])
        warehouses[1].add_shelf(shelves[i])

manager1 = StockManager(warehouses[0])

product1 = Laptop(1,"Ноутбук Леново",100240,"LapTop-001",220,16,"Intel-CoreI5",512,"1920x1024")
product2 = Smartphone(2,"Телефон Крутофон",36000,"VeryCleverPhone",20,256,6000,"MOC")
manager1.replenish(product1,20)
manager1.replenish(product2,30)

"""
небольший отрывок для тестов
n = (input())
open("warehouses.json","w").close()"""
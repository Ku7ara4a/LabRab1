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


warehouse1 = Warehouse(1,"Warehouse1","WH1")
shelf1 = Shelf(1,3,10)
shelf2 = Shelf(2,5,3)
warehouse1.add_shelf(shelf1)
warehouse1.add_shelf(shelf2)
manager1 = StockManager(warehouse1)
product1 = Laptop(1,"Ноутбук Леново",100240,"LapTop-001",220,16,"Intel-CoreI5",512,"1920x1024")
product2 = Smartphone(2,"Телефон Крутофон",36000,"VeryCleverPhone",20,256,6000,"MOC")
manager1.replenish(product1,20)
manager1.replenish(product2,30)

users[0].cart.add_item(product1,10)
users[0].make_an_order()
print(users[0].orders[0].items)

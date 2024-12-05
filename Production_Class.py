from Bike_Class import Bike
from Customer_Class import *
from Order_Class import Order


class Production:
    def __init__(self, order: Order):
        self.__order = order
        self.__bike_components: list = order.get_bike().get_components()

    def get_components(self) -> list:
        return self.__bike_components

    def get_details(self) -> list:
        details = self.__order.get_details()
        return details


contact_info = ContactInformation("07774808256", "johndoe@gmail.com")
deli = DeliveryAddress("123", "Street", "County", "City", "ZH1DJF")
customer = Customer("Name", contact_info, deli)

bike = Bike("Big", "Blue", 12.4, "Standard", "Standard", "LED")

date = "12/12/2024"

order = Order(bike, customer, date)

production = Production(order)
print(production.get_components())
print(production.get_details())

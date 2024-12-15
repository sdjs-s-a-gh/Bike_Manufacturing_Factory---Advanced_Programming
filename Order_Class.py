from Bike_Class import Bike
from Customer_Class import Customer


class Order:
    order_id = 0

    def __init__(self, bike: Bike, customer: Customer, date):
        self.__bike = bike
        self.__customer = customer
        self.__date = date
        self.__order_id = Order.order_id + 1

    def get_details(self) -> list:
        details = [self.order_id, self.__bike, self.__customer, self.__date]
        return details

    def get_bike(self) -> Bike:
        return self.__bike

    def get_order_id(self) -> int:
        return self.__order_id

    def __str__(self):
        return (f"Bike Details: \n {self.__bike} \n\n Customer Details: \n {self.__customer}\n\n"
                f"Date Details: \n\t Date Ordered: {self.__date}")

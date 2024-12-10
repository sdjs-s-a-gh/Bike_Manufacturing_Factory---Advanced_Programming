from Bike_Class import Bike
from Customer_Class import Customer


class Order:
    def __init__(self, bike: Bike, customer: Customer, date):
        self.__bike = bike
        self.__customer = customer
        self.__date = date

    def get_details(self) -> list:
        details = [self.__bike, self.__customer, self.__date]
        return details

    def get_bike(self) -> Bike:
        return self.__bike

    def __str__(self):
        return (f"Bike Details: \n {self.__bike} \n\n Customer Details: \n {self.__customer}\n\n"
                f"Date Details: \n\t Date Ordered: {self.__date}")

# The imports need to be listed like this for the test files to work. Otherwise, the
# test files will attempt to access a relative Bike_Class, for instance, which doesn't exist / isn't relative to them.
from Bike_Factory.Bike_Class import Bike
from Bike_Factory.Customer_Class import Customer


class Order:
    # a Class Variable that is incremented with each instantiation of this class, representing a unique order id
    order_id = 0

    def __init__(self, bike: Bike, customer: Customer, date: str):
        self.__bike = bike
        self.__customer = customer
        self.__date = date
        Order.order_id += 1     # increment the order_id by 1 for each new order
        self.__order_id = Order.order_id

    def get_details(self) -> list:
        """A getter function that returns the details of the order. This includes the order_id, bike details, customer
        details and the date of the order.

        Returns:
             list: A list containing the details of the order: order_id, bike details, customer details and
             the date of the order.
            """
        details = [self.order_id, self.__bike.get_details(), self.__customer.get_details(), self.__date]
        return details

    def get_bike(self) -> Bike:
        """A getter function that returns the instance of the bike class used in this order.

        Returns:
             Bike: An instance of the bike class - whether the parent or subsequent child classes.
            """
        return self.__bike

    def get_customer(self) -> Customer:
        """ A getter function that returns the instance of the customer class used in this order.

        Returns:
            Customer: An instance of the customer class, opening the ability for method chaining.
        """
        return self.__customer

    def get_date(self) -> str:
        """ A getter function that returns the date of the order.

        Returns:
            str: A string containing the date of the order in the format 'dd/MM/yyyy'.
            """
        return self.__date

    def get_order_id(self) -> int:
        """A getter function that returns the order ID given to this instance of the Order class.

        Returns:
             int: A integer representing the order ID given to this instance of the Order class.
            """
        return self.__order_id

    def __str__(self):
        return (f"Bike Details: \n {self.__bike} \n\n Customer Details: \n {self.__customer}\n\n"
                f"Date Details: \n\t Date Ordered: {self.__date}")

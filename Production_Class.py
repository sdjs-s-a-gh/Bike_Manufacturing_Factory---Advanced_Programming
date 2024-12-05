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

    def can_produce_bike(self) -> bool:
        count = 0
        output_bin_components = output_bin.get_components_dict()
        for component in self.__bike_components:
            if output_bin_components[component] >= 1:
                count += 1

        # If there is one of each component, and thus the bike can be made
        if count == len(self.__bike_components):
            output_bin.decrement_component_count(self.__bike_components)
            return True
        # else - if there are not enough components
        return False


class InputBin:
    def __init__(self):
        self.__frames: int = 0
        self.__forks: int = 0

    def get_details(self) -> list:
        items = [self.__frames, self.__forks]
        return items

    def set_frames(self, frames: int) -> None:
        self.__frames = frames

    def set_forks(self, forks: int) -> None:
        self.__forks = forks


class OutputBin:
    def __init__(self):
        self.__productions: list[Production] = []   # initially, there is nothing in the output bin
        self.__components: list = []  # the list of components
        self.__components_dict: dict = {}   # dictionary of components

    def get_components_list(self) -> list:
        return self.__components

    def get_components_dict(self) -> dict:
        return self.__components_dict

    def add_production(self, production: Production):
        self.__productions.append(production)

        #  Finding the production with the largest component count
        #  Used a lambda as it saves me writing a separate component length function
        largest_production = max(self.__productions, key=lambda produc: len(produc.get_components()))

        self.__components = largest_production.get_components()

        # Dictionary comprehension where each component is a key.
        self.__components_dict = {component: 0 for component in self.__components}


    def remove_production(self, production: Production):
        pass


    def increment_component_count(self, component) -> None:
        self.__components_dict[component] += 1

    # on production of a bike
    def decrement_component_count(self, components: list) -> None:
        for component in components:
            self.__components_dict[component] -= 1


contact_info = ContactInformation("07774808256", "johndoe@gmail.com")
deli = DeliveryAddress("123", "Street", "County", "City", "ZH1DJF")
customer = Customer("Name", contact_info, deli)

bike = Bike("Big", "Blue", 12.4, "Standard", "Standard", "LED")

date = "12/12/2024"

order = Order(bike, customer, date)

output_bin = OutputBin()

production = Production(order)
print(production.get_components())
print(production.get_details())

output_bin.add_production(production)
print(output_bin.get_components_list())
print(output_bin.get_components_dict())
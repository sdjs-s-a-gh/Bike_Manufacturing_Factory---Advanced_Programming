from Bike_Class import Bike, SportBike
from Customer_Class import *
from Order_Class import Order


class Production:
    def __init__(self, order: Order):
        self.__order = order
        self.__bike_components: list = order.get_bike().get_components()
        inventory.add_production(self)

    def get_components(self) -> list:
        return self.__bike_components

    def get_details(self) -> list:
        details = self.__order.get_details()
        return details

    def can_produce_bike(self) -> bool:
        count = 0
        output_bin_components = inventory.get_components_dict()
        for component in self.__bike_components:
            if output_bin_components[component] >= 1:
                count += 1

        # If there is one of each component, and thus the bike can be made
        if count == len(self.__bike_components):

            return True
        # else - if there are not enough components
        return False

    def produce_bike(self) -> None:
        for component in self.__bike_components:
            inventory.decrement_component_count(component)

    def __str__(self):
        return f"{self.__order}"


class Inventory:
    def __init__(self):
        self.__productions: list[Production] = []   # initially, there is nothing in the output bin
        # All possible components
        self.__components: list = [
            "Tabular Steel", "Forks", "Frames", "Front Fork", "Pedals", "Pairs of Wheels", "Gears", "Brakes",
            "Seats", "Lights", "Drink Holder"
        ]
        self.__components_dict: dict = {component: 0 for component in self.__components}   # dictionary of components

    def get_components_list(self) -> list:
        return self.__components

    def get_components_dict(self) -> dict:
        return self.__components_dict

    def add_production(self, production: Production):
        self.__productions.append(production)

    def remove_production(self, production: Production):
        self.__productions.remove(production)

    def increment_component_count(self, component) -> None:
        self.__components_dict[component] += 1
        # component.increment - polymorphism to change the stock of inputs

    def decrement_component_count(self, component, amount: int = 1) -> None:
        self.__components_dict[component] -= amount


# component.create on button in the production screen / assembly line
# In-house created Component. i.e. created from existing parts and not imported like lights or seats, etc.
class Component:

    def create(self, component):
        inventory.increment_component_count(component)


class Fork(Component):
    # annoyingly, can't do compile-time polymorphism/overloading in python to not have to write the component name
    def create(self, component="Fork"):
        super().create(component)
        inventory.decrement_component_count("Tabular Steel")


class Frame(Component):
    def create(self, component="Frame"):
        super().create(component)
        inventory.decrement_component_count("Tabular Steel", 2)


class FrontFork(Component):

    def create(self, component="Front Fork"):
        super().create(component)
        inventory.decrement_component_count("Frames")
        inventory.decrement_component_count("Forks")


inventory = Inventory()


# shared components
# for component in components
#   button is interactable at all

from Bike_Class import *
from Customer_Class import *
from Order_Class import Order


class Production:
    def __init__(self, order: Order):
        self.__order = order
        self.__bike_components: list = order.get_bike().get_components()
        history.add_current_production(self)

    def get_components(self) -> list:
        return self.__bike_components

    def get_details(self) -> list:
        details = self.__order.get_details()
        return details

    def get_order_id(self) -> int:
        return self.__order.get_order_id()

    def can_produce_bike(self) -> bool:
        count = 0
        production_bin_components = inventory.get_production_bin()
        for component in self.__bike_components:
            if production_bin_components[component] >= 1:
                count += 1

        # If there is one of each component, and thus the bike can be made
        if count == len(self.__bike_components):

            return True
        # else - if there are not enough components
        return False

    def produce_bike(self) -> None:
        for component in self.__bike_components:
            inventory.decrement_component_count(component)
            inventory.decrement_production_bin_component_count(component)
        # Remove this production from current and mark it as completed
        history.remove_production(self)
        history.add_completed_production(self)

    def __str__(self):
        return f"{self.__order}"


class Inventory:
    def __init__(self):
        # Components made by the assembly line
        self.__internal_components = ["Front Fork", "Painted Parts", "Frames", "Forks"]
        # All possible components without duplicates
        all_components = set(Bike.possible_components).union(
                SportBike.possible_components,
                TourBike.possible_components,
                CommuteBike.possible_components,
                self.__internal_components,
                ["Tubular Steel"]
            )
        # Sort the components Alphabetically, as sets display items randomly (the result of hashing)
        self.__components: list = sorted(all_components)

        self.__components_dict: dict = {component: 0 for component in self.__components}   # dictionary of components

        # Initialise the contents of the production_bin (the part transferred between each assembly station)
        self.__production_bin = {component: 0 for component in self.__components_dict.keys()}

    def get_components_list(self) -> list:
        return self.__components

    def get_components_dict(self) -> dict:
        return self.__components_dict

    def get_internal_components(self) -> list:
        return self.__internal_components

    def get_production_bin(self) -> dict:
        return self.__production_bin

    def increment_production_bin_component_count(self, component, amount=1) -> None:
        if amount > 0:
            self.__production_bin[component] += amount
        else:
            raise ValueError(f"Amount must be greater than zero")

    def decrement_production_bin_component_count(self, component, amount=1):
        temp = self.__production_bin[component] - amount
        if amount > 0:
            if temp >= 0:
                self.__production_bin[component] = temp
            else:
                raise ValueError(f"This is not possible. Deducting {amount} of {component} will cause the amount in"
                                 f" stock to reach subzero.")
        else:
            raise ValueError(f"Amount must be greater than zero")

    def increment_component_count(self, component, amount=1) -> None:
        if amount > 0:
            self.__components_dict[component] += amount
        else:
            raise ValueError(f"Amount must be greater than zero")

        # component.increment - polymorphism to change the stock of inputs

    def decrement_component_count(self, component, amount: int = 1) -> None:
        temp = self.__components_dict[component] - amount
        if amount > 0:
            if temp >= 0:
                self.__components_dict[component] -= amount
            else:
                raise ValueError(f"This is not possible. Deducting {amount} of {component} will cause the amount in"
                                 f" stock to reach subzero.")
        else:
            raise ValueError(f"Amount must be greater than zero")


class History:
    def __init__(self):
        self.__current_productions: list[Production] = []   # initially there are no bikes in production
        self.__completed_productions: list[Production] = []

    def get_current_productions(self) -> list[Production]:
        return self.__current_productions

    def get_completed_productions(self) -> list[Production]:
        return self.__completed_productions

    def add_current_production(self, production: Production) -> None:
        self.__current_productions.append(production)

    def add_completed_production(self, production: Production) -> None:
        self.__completed_productions.append(production)

    def remove_production(self, production: Production) -> None:
        self.__current_productions.remove(production)


# component.create on button in the production screen / assembly line
# In-house created Component. i.e. created from existing parts and not imported like lights or seats, etc.
# Abstract Class
class Component:
    def __init__(self, input_components: list[str], output_component: list[str], decrement_production_bin: bool=False):
        self._input = input_components
        self._output = output_component
        self.decrement_production_bin = decrement_production_bin

    def create(self) -> None:
        index = 0
        try:
            # Remove the input(s) from the inventory
            for component in self._input:
                inventory.decrement_component_count(component)
                index += 1
        except ValueError as x:
            # Rollback the change (there is at maximum two inputs, so if an error occurs on first one, nothing happens;
            # whereas if an error occurs on the second one, the first component needs to be reversed.
            if index == 1:
                inventory.increment_component_count(self._input[index - 1])
            raise x

        # Add the output to the inventory (to showcase amount in stock) and the production bin
        inventory.increment_component_count(self._output[0])
        inventory.increment_production_bin_component_count(self._output[0])
        # When the bike has been created, the amount in the inventory and the production bin will be removed.

        # Only used for the subclasses FrontFork and Frame, removing copy and pasted code between the two.
        if self.decrement_production_bin:
            for component in self._input:
                inventory.decrement_production_bin_component_count(component)

    def __str__(self):
        return f"{self._output[0]}"


class Fork(Component):
    def __init__(self):
        super().__init__(input_components=["Tubular Steel"], output_component=["Forks"])


class FrontFork(Component):
    def __init__(self):
        super().__init__(["Frames", "Forks"], ["Front Fork"], True)


class PaintedPart(Component):
    def __init__(self):
        super().__init__(
            input_components=["Frames", "Forks"], output_component=["Painted Parts"], decrement_production_bin=True
        )


class Frame(Component):
    def __init__(self, amount: int, model: str):
        super().__init__(input_components=["Tubular Steel"], output_component=["Frames"])
        # Adjusting the amount of tubular steel deducted also depends on the model of bike
        model_map = {"Standard": 1, "Sport": 2, "Tour": 3, "Commute": 4}
        self._amount = amount * model_map[model]
        # annoyingly, can't do compile-time polymorphism/overloading in python to not have to write the component name

    def create(self) -> None:
        inventory.decrement_component_count(self._input[0], self._amount)
        inventory.increment_component_count(self._output[0])
        inventory.increment_production_bin_component_count(self._output[0])


class SmallFrame(Frame):
    def __init__(self, model: str):
        super().__init__(1, model)


class MediumFrame(Frame):

    def __init__(self, model: str):
        super().__init__(2, model)


class LargeFrame(Frame):
    def __init__(self, model: str):
        super().__init__(3, model)


class ExtraLargeFrame(Frame):
    def __init__(self, model: str):
        super().__init__(4, model)


class ExternalComponent:
    def __init__(self, component: str):
        self.components = component

    def add(self) -> None:
        inventory.increment_production_bin_component_count(self.components)

    def __str__(self) -> str:
        return f"{self.components}"


inventory = Inventory()
history = History()


# shared components
# for component in components
#   button is interactable at all

#print(inventory.get_components_list())

#bike = CommuteBike("Big", "Red", "Flat", 26, "Standard", "Standard",
 #                  "LED", True, False, True, False, False)
#print(bike.get_components())

#smallstandard = SmallFrame("Standard")
#smallstandard.create()
#print(inventory.get_production_bin())
#medium = MediumFrame("Sport")
#medium.create()
#painted_part = PaintedPart()
#painted_part.create()
#ex = ExtraLargeFrame("Standard")
#ex.create()
#print(f"Inventory: {inventory.get_components_dict()} \nProduction Bin: {inventory.get_production_bin()}")
#inventory.decrement_production_bin_component_count("Painted Parts")
#inventory.decrement_component_count("Painted Parts")
#print(f"\nInventory: {inventory.get_components_dict()} \nProduction Bin: {inventory.get_production_bin()}")
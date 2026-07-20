# The imports need to be listed like this for the test files to work. Otherwise, the
# test files will attempt to access a relative Bike_Class, for instance, which doesn't exist / isn't relative to them.
from Bike_Factory.Bike_Class import *
from Bike_Factory.Customer_Class import *
from Bike_Factory.Order_Class import Order


class Production:
    def __init__(self, order: Order):
        self.__order = order
        self.__bike_components: list = order.get_bike().get_components()
        history.add_current_production(self)

    # Getters instead of having quite deep method chaining

    def get_components(self) -> list:
        """A getter function that returns the components needed to create a bike in this instance of the class.

        Returns:
            list: A list listing the components need to create the bike in this production.
            """
        return self.__bike_components

    def get_details(self) -> list:
        """A getter function that returns the details of the order. This includes the order id, the bike's details,
         customer details and the date of the order.

         Returns:
             list: A list containing the details of the order: order id, bike details, customer details and the order
             date.
             """
        details = self.__order.get_details()
        return details

    def get_bike_details(self) -> list:
        """A getter function that returns the details of the bike class's properties.

        Returns:
            list: A list detailing the status of the bike class's properties.
            """
        return self.__order.get_bike().get_details()

    def get_customer(self) -> Customer:
        """A getter function that returns the instance of the customer class used in this order.

        Returns:
            Customer: An instance of the customer class, opening the ability for method chaining."""
        return self.__order.get_customer()

    def get_customer_name(self) -> str:
        """A getter function that returns the name of the customer.

        Returns:
            str: The name of the customer."""
        return self.__order.get_customer().get_name()

    def get_customer_contact_information(self) -> list:
        """
        A getter function that returns the contact information of the customer: their phone number and email address.

        Returns:
            list: A list of all the contact details of the customer: phone number and email address.
        """
        return self.__order.get_customer().get_contact_information()

    def get_customer_address(self) -> list:
        """
        A getter function that returns the delivery address of the customer.

        Returns:
            list: A list of all the delivery address details of the customer.
        """
        return self.__order.get_customer().get_delivery_address()

    def get_order_id(self) -> int:
        """A getter function that returns the order ID given to this instance of the Order class.

        Returns:
             int: A integer representing the order ID given to this instance of the Order class."""
        return self.__order.get_order_id()

    def get_date_ordered(self) -> str:
        """A getter function that returns the date of the order.

        Returns:
            str: A string containing the date of the order in the format 'dd/MM/yyyy'."""
        return self.__order.get_date()

    def can_produce_bike(self) -> bool:
        """A function that returns whether there is a sufficient number of components to make this instance
        of the bike class.

        Returns:
            bool: A boolean that indicates whether this instance of the bike class can be made.
            """
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
        """A subroutine that produces this instance of the bike class, removing the components used from the production
        bin and stock. The history is also updated by removing this production from the current and moving it into the
        list of completed productions."""
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
        """A getter function that returns a sorted list of all components that may be used to produce a bike.

        Returns:
            list: A sorted list of all the components that may be used to produce a bike.
            """
        return self.__components

    def get_components_dict(self) -> dict:
        """A getter function that returns a dictionary representing the stock/inventory of all components.

        Returns:
            dictionary: a dictionary representing the stock of the components; the key = component and the
            values = quantity of stock.
            """
        return self.__components_dict

    def get_internal_components(self) -> list:
        """A getter function that returns all components that are produced in-house, meaning they do not need to be
        restocked.

        Returns:
            list: A list of all components that are produced internally (in-house); they do not need to be restocked.
            """
        return self.__internal_components

    def get_production_bin(self) -> dict:
        """A getter function that returns the production bin: essentially a mini-version of stock that is meant to
        simulate, how I have interpreted, a bin/tray that gets passed from workstation-to-workstation, wherein each
        workstation puts in the components they have produced. Each workstation that is located after where the tray is
        currently at cannot produce/add any more components. However, the ones behind the production bin can, but they
        will be notified when they produce an excess.

        Returns:
            dictionary: A dictionary of all the components in the production bin, pairing with their number of stock.
            """
        return self.__production_bin

    def increment_production_bin_component_count(self, component: str, quantity=1) -> None:
        """A setter function increments the component passed in, as an argument, by a default quantity of one. This
        change is only applied to the production bin - not the inventory."""
        if quantity > 0:
            self.__production_bin[component] += quantity
        else:
            raise ValueError(f"quantity must be greater than zero")

    def decrement_production_bin_component_count(self, component, quantity=1):
        """A setter function decreases the component passed in, as an argument, by a default quantity of one. This
        change is only applied to the production bin - not the inventory."""
        temp = self.__production_bin[component] - quantity
        if quantity > 0:
            if temp >= 0:
                self.__production_bin[component] = temp
            else:
                raise ValueError(f"This is not possible. Deducting {quantity} of {component} will cause the quantity in"
                                 f" stock to reach subzero.")
        else:
            raise ValueError(f"quantity must be greater than zero")

    def increment_component_count(self, component, quantity=1) -> None:
        """A setter function that increases the quantity of the component passed in, as an argument,
         by a default value of one."""
        if quantity > 0:
            self.__components_dict[component] += quantity
        else:
            raise ValueError(f"quantity must be greater than zero")

    def decrement_component_count(self, component, quantity: int = 1) -> None:
        """A setter function that decreases the quantity of the component passed in, as an argument,
                 by a default value of one."""
        temp = self.__components_dict[component] - quantity
        if quantity > 0:
            if temp >= 0:
                self.__components_dict[component] -= quantity
            else:
                raise ValueError(f"This is not possible. Deducting {quantity} of {component} will cause the quantity in"
                                 f" stock to reach subzero.")
        else:
            raise ValueError(f"quantity must be greater than zero")


class History:
    def __init__(self):
        self.__current_productions: list[Production] = []   # initially there are no bikes in production
        self.__completed_productions: list[Production] = []

    def get_current_productions(self) -> list[Production]:
        """A getter function that returns a list of productions (as objects) that are currently in being
        fulfilled/produced.

        Returns:
            list[Production]: A list of productions that are currently being produced / on the assembly line.
        """
        return self.__current_productions

    def get_completed_productions(self) -> list[Production]:
        """A getter function that returns a list of completed production as objects.

        Returns:
            list[Production]: A list of productions that have been produced.
            """
        return self.__completed_productions

    def add_current_production(self, production: Production) -> None:
        """A setter subroutine that adds the production object passed in to the list of current productions."""
        self.__current_productions.append(production)

    def add_completed_production(self, production: Production) -> None:
        """A setter subroutine that adds the production object passed in to the list of completed productions."""
        self.__completed_productions.append(production)

    def remove_production(self, production: Production) -> None:
        """A setter subroutine that removes the production object passed from the list of current productions, ready
        to be moved to the list of completed productions."""
        self.__current_productions.remove(production)


# In-house created Component. i.e. created from existing parts and not imported like lights or seats, etc.
# Abstract Class
class Component:
    def __init__(self, input_components: list[str], output_component: list[str], decrement_production_bin: bool=False):
        self._input = input_components
        self._output = output_component
        self.decrement_production_bin = decrement_production_bin

    def create(self) -> None:
        """A subroutine that creates the components, removing those from its input from the inventory
        (either a singular component or multiple) and producing an output."""
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

        # Add the output to the inventory (to showcase quantity in stock) and the production bin
        inventory.increment_component_count(self._output[0])
        inventory.increment_production_bin_component_count(self._output[0])
        # When the bike has been created, the quantity in the inventory and the production bin will be removed.

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
    def __init__(self, quantity: int, model: str):
        super().__init__(input_components=["Tubular Steel"], output_component=["Frames"])
        # Adjusting the quantity of tubular steel deducted also depends on the model of bike
        model_map = {"Standard": 1, "Sport": 2, "Tour": 3, "Commute": 4}
        self._quantity = quantity * model_map[model]
        # annoyingly, can't do compile-time polymorphism/overloading in python to not have to write the component name

    def create(self) -> None:
        inventory.decrement_component_count(self._input[0], self._quantity)
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
        """A subroutine that increments the production bin count of the external component this instance of the
         class is created on. As external components are not made in-house, they must be purchased and restocked when
         needed."""
        inventory.increment_production_bin_component_count(self.components)

    def __str__(self) -> str:
        return f"{self.components}"


inventory = Inventory()
history = History()





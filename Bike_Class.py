class Bike:
    # Class Variables (i.e. not instance-related), using a tuple to make them immutable
    possible_components: tuple = (
            "Front Fork", "Handlebar", "Pedals", "Pairs of Wheels", "Gears", "Brakes", "Lights", "Seats"
    )
    # A list of components that are fixed by class, and thus can not be changed by a user.
    # The first index of the inner list denotes the component; the second index informs what the setIndex of the combo
    # box should be.
    non_interactable_components: list[list] = [["Handlebar Type", 0]]

    def __init__(self, size: str, colour: str, wheel_size: float, gear_type: str, brake_type: str, light_option: str):
        self._model = "Standard"  # the attribute is Protected as it needs to be accessed in inherited subclasses
        self.__size = size
        self.__colour = colour
        self._handlebar_type = "Flat"
        self.__wheel_size = wheel_size
        # Component Combinations
        self.__gear_type = gear_type
        self.__brake_type = brake_type
        self.__light_option = light_option

    def get_components(self) -> list:
        """A function returning the components USED by this particular instance of the Bike class. A copy of the class
        variable 'components' is returned because the components used in child classes may differ to the list of
        available components specified in a class's variable. For instance, the SportBike class has the available
        component 'Drink Holder'. If this component is false, the component would originally still be used as the class
        is inheriting the method to check its own possible components rather than a separate list, such as the one
        below."""
        components_used = [
            "Front Fork", "Handlebar", "Pedals", "Pairs of Wheels", "Gears", "Brakes", "Lights", "Seats"
        ]
        return components_used

    def get_details(self) -> list:
        details = [
            self._model, self.__size, self.__colour, self._handlebar_type, self.__wheel_size, self.__gear_type,
            self.__brake_type, self.__light_option
        ]

        return details

    def __str__(self):
        return (f"\t Model: {self._model}, \n\t Size: {self.__size}, \n\t Colour: {self.__colour},"
                f"\n\t Handlebar Type: {self._handlebar_type}, \n\t Wheel Size: {self.__wheel_size},"
                f"\n\t Gear Type: {self.__gear_type}, \n\t Brake Type: {self.__brake_type},"
                f"\n\t Light Option: {self.__light_option}")


class SportBike(Bike):
    # Possible Additional components - these are not guaranteed
    possible_components: tuple = Bike.possible_components + ("Drink Holder",)

    non_interactable_components: list[list] = [
        ["Handlebar Type", 1],  # Handlebar Type = Aerodynamic
        ["Gear Type", 1],   # Gear Type = Premium
        ["Brake Type", 0]   # Brake Type = Disc
    ]

    def __init__(self, size: str, colour: str, wheel_size: float, light_option: str, drink_holder: bool):
        super().__init__(size, colour, wheel_size, "Premium", "Disc", light_option)
        self._model = "Sport"   # Inherit parent class's protected attributes
        self._handlebar_type = "Aerodynamic"
        self._drink_holder = drink_holder

    def get_components(self) -> list:
        """A function returning the list of components USED by this particular instance of the SportBike class."""
        components_used = super().get_components()
        if self._drink_holder:
            components_used.append("Drink Holder")
        return components_used

    def get_details(self) -> list:
        details = super().get_details()
        details.append(self._drink_holder)
        return details

    def __str__(self):
        return f"{super().__str__()}, \n\t Drink Holder: {self._drink_holder}"


class TourBike(Bike):
    # Possible components
    possible_components: tuple = Bike.possible_components + ("Drink Holder", "Rear Rack", "Mudflaps")

    non_interactable_components: list[list] = [["Rear Rack", 1]]    # Rear Rack = Yes

    # The rear rack is not optional for tour classes -- it is mandatory, thus there is no input for it in the
    # constructor. Whereas, the drink holder and mudflaps are optional.
    def __init__(
            self, size: str, colour: str, handlebar_type: str, wheel_size: float, gear_type: str, brake_type: str,
            light_option: str, drink_holder: bool, mudflaps: bool
    ):
        super().__init__(size, colour, wheel_size, gear_type, brake_type, light_option)
        self._model = "Tour"
        self._handlebar_type = handlebar_type
        self._drink_holder = drink_holder
        self._rear_rack = True
        self._mudflaps = mudflaps

    def get_components(self) -> list:
        components_used = super().get_components()

        # Rather than writing a lot of if statements, I have used list comprehension to get a list of the status of
        # the additional components.
        additional_components = [
            "Drink Holder" if self._drink_holder else None,
            "Mudflaps" if self._mudflaps else None
        ]

        # From this list, remove the components if they are not None (they do not exist). A functional programming
        # filter could also be used to achieve the desired result.
        additional_components = [component for component in additional_components if component]

        return components_used + additional_components

    def get_details(self) -> list:
        details = super().get_details()
        details.append([self._drink_holder, self._rear_rack, self._mudflaps])
        return details

    def __str__(self):
        return (f"{super().__str__()}, \n\t Drink Holder: {self._drink_holder}, \n\t Rear Rack: {self._rear_rack}, "
                f"\n\t Mudflaps: {self._mudflaps}")


class CommuteBike(TourBike):
    # Possible components
    possible_components: tuple = TourBike.possible_components + ("Front Rack", "Child Seat")

    # Overwrite the non-interactable components
    non_interactable_components = None

    def __init__(
            self, size: str, colour: str, handlebar_type: str, wheel_size: float, gear_type: str, brake_type: str,
            light_option: str, drink_holder: bool, mudflaps: bool, front_rack: bool, rear_rack: bool, child_seat: bool
                 ):
        super().__init__(
            size, colour, handlebar_type, wheel_size, gear_type, brake_type, light_option, drink_holder, mudflaps
                         )
        self._model = "Commute"
        self.__front_rack = front_rack
        self._rear_rack = rear_rack
        self.__child_seat = child_seat

    def get_components(self) -> list:
        components_used = super().get_components()

        # List comprehension to get a list of the status of the additional components.
        additional_components = [
            "Rear Rack" if self._rear_rack else None,
            "Front Rack" if self.__front_rack else None,
            "Child Seat" if self.__child_seat else None
        ]

        # From this list, remove the components if they are not None (they do not exist).
        additional_components = [component for component in additional_components if component]

        return components_used + additional_components

    def get_details(self) -> list:
        details = super().get_details()
        details.append([self.__front_rack, self.__child_seat])
        return details

    def __str__(self):
        return f"{super().__str__()}, \n\t Front Rack: {self.__front_rack}, \n\t Child Seat: {self.__child_seat}"

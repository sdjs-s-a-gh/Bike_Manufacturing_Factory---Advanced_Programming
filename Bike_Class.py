class Bike:
    def __init__(self, size: str, colour: str, wheel_size: float, gear_type: str, brake_type: str, light_option: str):
        self._model = "Standard"  # the attribute is Protected as it needs to be accessed in inherited subclasses
        self.__size = size
        self.__colour = colour
        self.__wheel_size = wheel_size
        # Component Combinations
        self.__gear_type = gear_type
        self.__brake_type = brake_type
        self.__light_option = light_option

    def get_components(self) -> list:
        components = [
            "Front Fork", "Pedals", "Pairs of Wheels", "Gears", "Brakes", "Lights", "Seats"
        ]

        return components

    def get_details(self) -> list:
        details = [
            self._model, self.__size, self.__colour, self.__wheel_size, self.__gear_type,
            self.__brake_type, self.__light_option
        ]

        return details

    def __str__(self):
        return (f"\t Model: {self._model}, \n\t Size: {self.__size}, \n\t Colour: {self.__colour},"
                f"\n\t Wheel Size: {self.__wheel_size}, \n\t Gear Type: {self.__gear_type},"
                f"\n\t Brake Type: {self.__brake_type}, \n\t Light Option: {self.__light_option}")


class SportBike(Bike):
    def __init__(self, size: str, colour: str, wheel_size: float, gear_type: str, light_option: str, drink_holder: bool):
        super().__init__(size, colour, wheel_size, gear_type, "Premium", light_option)
        self._model = "Sport"
        self.__drink_holder = drink_holder

    def get_components(self) -> list:
        components = super().get_components()
        if self.__drink_holder:
            components.append("Drink Holder")
        return components

    def get_details(self) -> list:
        details = super().get_details()
        details.append(self.__drink_holder)
        return details

    def __str__(self):
        og_string = super().__str__()
        return f"{og_string}, \n\t Drink Holder: {self.__drink_holder}"

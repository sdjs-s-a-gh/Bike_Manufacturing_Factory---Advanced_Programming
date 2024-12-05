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
            self.__colour, self.__wheel_size, self.__gear_type, self.__brake_type, self.__light_option
        ]

        return components

    def get_details(self) -> list:
        details = [
            self._model, self.__size, self.__colour, self.__wheel_size, self.__gear_type,
            self.__brake_type, self.__light_option
        ]

        return details


class SportBike(Bike):
    def __init__(self, size: str, colour: str, wheel_size: float, gear_type: str, light_option: str):
        super().__init__(size, colour, wheel_size, gear_type, "Brake", light_option)
        self._model = "Sport"



#sport = SportBike("Big", "Blue", 1.4, "Standard", "LED")
#print(sport.get_components())
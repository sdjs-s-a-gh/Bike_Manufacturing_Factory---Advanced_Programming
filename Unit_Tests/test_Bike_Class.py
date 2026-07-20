from unittest import TestCase
from Bike_Factory.Bike_Class import *


class TestBike(TestCase):
    def setUp(self):
        """Create a sample (standard) Bike instance before each test."""
        self.bike = Bike(
            size="Big", colour="Blue", wheel_size=26, gear_type="Standard", brake_type="Rim", light_option="Standard"
        )

    def test_initialisation(self):
        """Test if the Bike initialises with the correct attributes by using the get_details() method."""
        actual: list = self.bike.get_details()
        expected: list = ["Model: Standard", "Size: Big", "Colour: Blue", "Handlebar Type: Flat",
                          "Wheel Size: 26 inches", "Gear Type: Standard", "Brake Type: Rim", "Light Option: Standard"]
        self.assertEqual(expected, actual)

    def test_get_components(self):
        """Test if the Bike instance correctly displays the types of components."""
        # Normal Data - the list of components used should be equal to the class attribute for the standard bike.
        actual: list[str] = self.bike.get_components()
        expected: list[str] = list(Bike.possible_components)
        self.assertEqual(expected, actual)

        # Erroneous Data - the "Drink Holder" is not expected
        not_expected: list[str] = [
            "Front Fork", "Handlebar", "Pedals", "Pairs of Wheels", "Gears", "Brakes", "Lights", "Seats", "Drink Holder"
        ]
        self.assertNotEqual(not_expected, actual)


class TestSportBike(TestCase):
    def setUp(self):
        """
        Create two sample SportBike instances before each test. One sample has a drinks holder; the other does not.
        """
        # A SportBike with a drink holder
        self.bike_w_drink = SportBike(
            size="Small", colour="Red", wheel_size=26, light_option="LED", drink_holder=True
        )
        # A SportBike without a drink holder. The 'wo' signifies 'without'.
        self.bike_wo_drink = SportBike(
            size="Small", colour="Red", wheel_size=26,  light_option="LED", drink_holder=False
        )

    def test_initialisation(self):
        """Test if the SportBike initialises with the correct attributes by using the get_details() method."""
        # With a drinks holder
        actual: list = self.bike_w_drink.get_details()
        expected: list = [
            "Model: Sport", "Size: Small", "Colour: Red", "Handlebar Type: Aerodynamic", "Wheel Size: 26 inches",
            "Gear Type: Premium", "Brake Type: Disc", "Light Option: LED", "Drink Holder: True"
        ]
        self.assertEqual(expected, actual)

        # Without a drinks holder
        actual: list = self.bike_wo_drink.get_details()
        expected: list = [
            "Model: Sport", "Size: Small", "Colour: Red", "Handlebar Type: Aerodynamic", "Wheel Size: 26 inches",
            "Gear Type: Premium", "Brake Type: Disc", "Light Option: LED", "Drink Holder: False"
        ]
        self.assertEqual(expected, actual)

    def test_get_components(self):
        """Test if the SportBike instances correctly displays each component that is needed to create that bike."""
        # With a drinks holder
        actual: list[str] = self.bike_w_drink.get_components()
        expected: list[str] = [
            "Front Fork", "Painted Parts", "Handlebar", "Pedals", "Pairs of Wheels", "Gears", "Brakes", "Lights",
            "Seats", "Drink Holder"
        ]
        self.assertEqual(expected, actual)

        # Without a drinks holder
        actual: list[str] = self.bike_wo_drink.get_components()
        expected: list[str] = [
            "Front Fork", "Painted Parts", "Handlebar", "Pedals", "Pairs of Wheels", "Gears", "Brakes", "Lights",
            "Seats"
        ]
        self.assertEqual(expected, actual)


class TestTourBike(TestCase):
    def setUp(self):
        """Create two sample TourBike class before each test. One has a mudflap; the other does not."""
        self.bike_with_mudflap = TourBike(
            size="Small", colour="Blue", handlebar_type="Aerodynamic", wheel_size=27.5, gear_type="Premium",
            brake_type="Rim", light_option="LED", drink_holder=True, mudflaps=True
        )

        self.bike_without_mudflap = TourBike(
            size="Small", colour="Blue", handlebar_type="Aerodynamic", wheel_size=27.5, gear_type="Premium",
            brake_type="Rim", light_option="LED", drink_holder=True, mudflaps=False
        )

    def test_initialisation(self):
        """Test if the TourBike instances initialise with the correct attributes by using the get_details() method."""
        # With a mudflap
        actual: list = self.bike_with_mudflap.get_details()
        expected: list = [
            "Model: Tour", "Size: Small", "Colour: Blue", "Handlebar Type: Aerodynamic", "Wheel Size: 27.5 inches",
            "Gear Type: Premium", "Brake Type: Rim", "Light Option: LED", "Drink Holder: True", "Rear Rack: True",
            "Mudflaps: True"
        ]
        self.assertEqual(expected, actual)

        # Without a mudflap
        actual: list = self.bike_without_mudflap.get_details()
        expected: list = [
            "Model: Tour", "Size: Small", "Colour: Blue", "Handlebar Type: Aerodynamic", "Wheel Size: 27.5 inches",
            "Gear Type: Premium", "Brake Type: Rim", "Light Option: LED", "Drink Holder: True", "Rear Rack: True",
            "Mudflaps: False"
        ]
        self.assertEqual(expected, actual)

    def test_get_components(self):
        """Test if the TourBike instances correctly display each component that is needed to create that bike."""
        # With a drinks holder
        actual: list[str] = self.bike_with_mudflap.get_components()
        expected: list[str] = [
            "Front Fork", "Painted Parts", "Handlebar", "Pedals", "Pairs of Wheels", "Gears", "Brakes", "Lights",
            "Seats", "Drink Holder", "Mudflaps", "Rear Rack"
        ]
        self.assertEqual(expected, actual)

        # Without a drinks holder
        actual: list[str] = self.bike_without_mudflap.get_components()
        expected: list[str] = [
            "Front Fork", "Painted Parts", "Handlebar", "Pedals", "Pairs of Wheels", "Gears", "Brakes", "Lights",
            "Seats", "Drink Holder", "Rear Rack"
        ]
        self.assertEqual(expected, actual)


class TestCommuteBikeClass(TestCase):
    def setUp(self):
        """Create two sample TourBike class before each test. One has a mudflap; the other does not."""
        self.bike_with_additional = CommuteBike(
            size="Small", colour="Blue", handlebar_type="Aerodynamic", wheel_size=27.5, gear_type="Premium",
            brake_type="Rim", light_option="LED", drink_holder=True, mudflaps=True, front_rack=True, rear_rack=True,
            child_seat=True
        )

        self.bike_without_additional = CommuteBike(
            size="Small", colour="Blue", handlebar_type="Aerodynamic", wheel_size=27.5, gear_type="Premium",
            brake_type="Rim", light_option="LED", drink_holder=True, mudflaps=True, front_rack=False, rear_rack=False,
            child_seat=False
        )

    def test_initialisation(self):
        # With additional components
        actual: list = self.bike_with_additional.get_details()
        expected: list = [
            "Model: Commute", "Size: Small", "Colour: Blue", "Handlebar Type: Aerodynamic", "Wheel Size: 27.5 inches",
            "Gear Type: Premium", "Brake Type: Rim", "Light Option: LED", "Drink Holder: True", "Rear Rack: True",
            "Mudflaps: True", "Front Rack: True", "Child Seat: True"
        ]
        self.assertEqual(expected, actual)

        # Without additional components
        actual: list = self.bike_without_additional.get_details()
        expected: list = [
            "Model: Commute", "Size: Small", "Colour: Blue", "Handlebar Type: Aerodynamic", "Wheel Size: 27.5 inches",
            "Gear Type: Premium", "Brake Type: Rim", "Light Option: LED", "Drink Holder: True", "Rear Rack: False",
            "Mudflaps: True", "Front Rack: False", "Child Seat: False"
        ]
        self.assertEqual(expected, actual)

    def test_get_components(self):
        """Test if the CommuteBike instances correctly display each component that is needed to create that bike."""
        # With a drinks holder
        actual: list[str] = self.bike_with_additional.get_components()
        expected: list[str] = [
            "Front Fork", "Painted Parts", "Handlebar", "Pedals", "Pairs of Wheels", "Gears", "Brakes", "Lights",
            "Seats", "Drink Holder", "Mudflaps", "Rear Rack", "Front Rack", "Child Seat"
        ]
        self.assertEqual(expected, actual)

        # Without a drinks holder
        actual: list[str] = self.bike_without_additional.get_components()
        expected: list[str] = [
            "Front Fork", "Painted Parts", "Handlebar", "Pedals", "Pairs of Wheels", "Gears", "Brakes", "Lights",
            "Seats", "Drink Holder", "Mudflaps"
        ]
        self.assertEqual(expected, actual)





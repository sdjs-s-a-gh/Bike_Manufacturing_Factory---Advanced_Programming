from unittest import TestCase
from Bike_Class import *


class TestBike(TestCase):
    def setUp(self):
        """Create a sample (standard) Bike class before each test."""
        self.bike = Bike(
            size="Big", colour="Blue", wheel_size=26, gear_type="Standard", brake_type="Rim", light_option="Standard"
        )

    def test_initialisation_and_get_details(self):
        """Test if the Bike initialises with the correct attributes by using the get_details() method"""
        actual: list = self.bike.get_details()
        expected: list = ["Standard", "Big", "Blue", "Flat", 26, "Standard", "Rim", "Standard"]
        # [0] = Model; [3] = Handlebar Type
        self.assertEqual(expected, actual)

    def test_get_components(self):
        """Test if the Bike instance correctly displays the types of components"""
        # Normal Data
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

    def test_initialisation_and_get_details(self):
        """Test if the SportBike initialises with the correct attributes by using the get_() method. Both methods
        should return the exact same result - despite having a differing 'drink holder' attribute."""
        # With a drinks holder
        actual: list = self.bike_w_drink.get_details()
        expected: list = ["Sport", "Small", "Red", "Aerodynamic", 26, "Premium", "Disc", "LED", True]
        self.assertEqual(expected, actual)

        # Without a drinks holder
        actual: list = self.bike_wo_drink.get_details()
        expected: list = ["Sport", "Small", "Red", "Aerodynamic", 26, "Premium", "Disc", "LED", False]
        self.assertEqual(expected, actual)

    def test_get_components(self):
        # With a drinks holder
        actual: list[str] = self.bike_w_drink.get_components()
        expected: list[str] = [
            "Front Fork", "Handlebar", "Pedals", "Pairs of Wheels", "Gears", "Brakes", "Lights", "Seats", "Drink Holder"
        ]
        self.assertEqual(expected, actual)

        # Without a drinks holder
        actual: list[str] = self.bike_wo_drink.get_components()
        expected: list[str] = ["Front Fork", "Handlebar", "Pedals", "Pairs of Wheels", "Gears", "Brakes", "Lights", "Seats"]
        self.assertEqual(expected, actual)



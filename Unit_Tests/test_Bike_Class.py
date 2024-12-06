from unittest import TestCase
from Bike_Class import *

class TestBike(TestCase):
    def setUp(self):
        """Create a sample (standard) Bike class before each test."""
        self.bike = Bike(
            size="Big", colour="Blue", wheel_size=12.6, gear_type="Standard", brake_type="Rim", light_option="Standard"
        )

    def test_initialisation_and_get_details(self):
        """Test if the Bike initialises with the correct attributes by using the get_details() method"""
        actual: list = self.bike.get_details()
        expected: list = ["Standard", "Big", "Blue", 12.6 , "Standard", "Rim", "Standard"]    # [0] = Model
        self.assertEqual(expected, actual)

    def test_get_components(self):
        """Test if the Bike instance correctly displays the types of components"""
        # Normal Data
        actual: list[str] = self.bike.get_components()
        expected: list[str] = ["Bicycle Frame", "Pairs of Wheels", "Gears", "Brakes", "Lights"]
        self.assertEqual(expected, actual)

        # Erroneous Data
        not_expected: list[str] = ["Bicycle Frame", "Pairs of Wheels", "Gears", "Brakes", "Lights", "Drink Holder"]
        self.assertNotEqual(not_expected, actual)

class TestSportBike(TestCase):
    def setUp(self):
        """Create two sample SportBike instances before each test. One sample has a drinks holder; the other does not."""
        # A SportBike with a drink holder
        self.bike_w_drink = SportBike(
            size="Small", colour="Red", wheel_size=10.8, gear_type="Disc", light_option="LED", drink_holder=True
        )
        # A SportBike without a drink holder
        self.bike_wo_drink = SportBike(
            size="Small", colour="Red", wheel_size=10.8, gear_type="Disc", light_option="LED", drink_holder=False
        )

    def test_initialisation_and_get_details(self):
        """Test if the SportBike initialises with the correct attributes by using the get_details() method."""
        # With a drinks holder
        actual: list = self.bike_w_drink.get_details()
        expected: list = ["Sport", "Small", "Red", 10.8, "Disc", "Premium", "LED", True]  # [0] = Model; [5] = brake type
        self.assertEqual(expected, actual)

        # Without a drinks holder
        actual: list = self.bike_wo_drink.get_details()
        expected: list = ["Sport", "Small", "Red", 10.8, "Disc", "Premium", "LED", False]
        self.assertEqual(expected, actual)

    def test_get_components(self):
        # With a drinks holder
        actual: list[str] = self.bike_w_drink.get_components()
        expected: list[str] = ["Bicycle Frame", "Pairs of Wheels", "Gears", "Brakes", "Lights", "Drink Holder"]
        self.assertEqual(expected, actual)

        # Without a drinks holder
        actual: list[str] = self.bike_wo_drink.get_components()
        expected: list[str] = ["Bicycle Frame", "Pairs of Wheels", "Gears", "Brakes", "Lights"]
        self.assertEqual(expected, actual)



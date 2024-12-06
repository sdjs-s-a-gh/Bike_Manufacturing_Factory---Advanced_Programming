from unittest import TestCase

from Customer_Class import Customer, ContactInformation, DeliveryAddress
from Production_Class import Production, output_bin # I need a specific instance of OutputBin to test
from Bike_Class import *
from Order_Class import Order


class TestProduction(TestCase):
    def setUp(self):
        """Create a sample Production class and the OutputBin before each test."""

        bike = Bike(
            size="Big", colour="Blue", wheel_size=12.6, gear_type="Standard", brake_type="Rim", light_option="Standard"
        )
        contact_info = ContactInformation(phone_number="02345678911", email_address="johndoe@gmail.com")
        delivery_info = DeliveryAddress(
            house_number="12", street="A690", county="Greater London", town_city="London", postcode="ZH1DJF"
        )
        customer = Customer(
            name="John Doe", contact_information=contact_info, delivery_address=delivery_info
        )
        order = Order(bike=bike, customer=customer, date="06/12/2024")
        self.production = Production(order=order)

    # As the tests are seemingly executed in alphabetical order, the test initialisation method name contains
    # the number one because the method needs to be run before test_get_components_multiple
    def test_initialisation(self):
        # Test all the components in the production bike are in the output bin.
        for component in self.production.get_components():
            self.assertIn(component, output_bin.get_components_list())

        self.assertEqual(self.production.can_produce_bike(), False)

    def test_get_components(self):
        actual = self.production.get_components()
        expected = ["Bicycle Frame", "Pairs of Wheels", "Gears", "Brakes", "Lights"]
        self.assertEqual(actual, expected)

    def test_production(self):
        for component in self.production.get_components():
            output_bin.increment_component_count(component)
        self.assertEqual(self.production.can_produce_bike(), True)

        # Test the production successfully cleans up by decrementing each component used by 1.
        output_bin_dict = output_bin.get_components_dict()
        for component in self.production.get_components():
            self.assertEqual(output_bin_dict[component], 0)

from unittest import TestCase

from Customer_Class import Customer, ContactInformation, DeliveryAddress
from Production_Class import Production, inventory   # I need a specific instance of Inventory to test
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

    def test_initialisation(self):
        # Test all the components in the production bike are valid by being in the Inventory.
        for component in self.production.get_components():
            self.assertIn(component, inventory.get_components_list())

        self.assertEqual(self.production.can_produce_bike(), False)

    def test_get_components(self):
        actual = self.production.get_components()
        expected = ["Front Fork", "Pedals", "Pairs of Wheels", "Gears", "Brakes", "Lights", "Seats"]
        self.assertEqual(actual, expected)

    def test_production(self):
        """
        Testing that a bike can be produced by fulfilling its component requirements. Once produced, then checking
        that the inventory successfully cleans up by decrementing each component used by 1.
        """
        for component in self.production.get_components():
            inventory.increment_component_count(component)
        self.assertEqual(self.production.can_produce_bike(), True)

        # Produce the bike, decrementing each component used by 1
        self.production.produce_bike()

        # Test the production successfully cleans up
        inventory_dict = inventory.get_components_dict()
        for component in self.production.get_components():
            self.assertEqual(inventory_dict[component], 0)

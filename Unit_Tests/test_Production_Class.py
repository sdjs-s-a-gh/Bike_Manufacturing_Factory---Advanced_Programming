from unittest import TestCase

from Bike_Factory.Customer_Class import Customer, ContactInformation, DeliveryAddress
# I need a specific instance of Inventory and History because the Production code relies on their existence.
from Bike_Factory.Production_Class import Production, inventory, history
from Bike_Factory.Bike_Class import *
from Bike_Factory.Order_Class import Order


class TestProduction(TestCase):
    def setUp(self):
        """Create a sample instance of the Production class before each test."""

        self.bike = SportBike(
            size="Small", colour="Red", wheel_size=26, light_option="LED", drink_holder=True
        )
        self.contact_info = ContactInformation(phone_number="02345678911", email_address="johnsmith@gmail.com")
        self.delivery_info = DeliveryAddress(
            house_number="10", street="Belle Vue", county="County Durham", town_city="Durham", postcode="DH1 0NQ"
        )
        self.customer = Customer(
            name="John Smith", contact_information=self.contact_info, delivery_address=self.delivery_info
        )
        self.order_date = "06/12/2024"
        self.order = Order(bike=self.bike, customer=self.customer, date=self.order_date)
        self.production = Production(order=self.order)

        # a copy production to test if the order ids are correctly unique.
        self.order2 = Order(bike=self.bike, customer=self.customer, date=self.order_date)
        self.production2 = Production(order=self.order2)

    def test_initialisation(self):
        """Test if the instance correctly initialises."""
        self.assertEqual(self.production.get_customer(), self.customer)
        self.assertEqual(self.production.get_date_ordered(), self.order_date)
        self.assertEqual(self.production.get_bike_details(), self.bike.get_details())
        self.assertEqual(self.production.get_components(), self.bike.get_components())
        self.assertEqual(self.production.get_customer_name(), self.customer.get_name())
        self.assertNotEqual(self.production.get_order_id(), self.production2.get_order_id())

        # Test the bike has been added to the list of current productions.
        self.assertIn(self.production, history.get_current_productions())

    def test_production_of_bike(self):
        """
        Testing that a bike can be produced by fulfilling its component requirements. Once produced, then checking
        that the inventory successfully cleans up by decrementing each component used by 1.
        """
        # Restock Materials to be used for the production of the bike
        for component in inventory.get_components_list():
            inventory.increment_component_count(component, 2)

        # Get the material to make the bike and put them in the production bin
        for component in self.production.get_components():
            inventory.increment_production_bin_component_count(component)
        self.assertEqual(self.production.can_produce_bike(), True)

        # Produce the bike, decrementing each component used by 1
        self.production.produce_bike()

        # Test the production successfully cleans up
        for component in self.production.get_components():
            self.assertEqual(inventory.get_production_bin()[component], 0)

        # Test the production has been removed from the list of current productions
        self.assertNotIn(self.production, history.get_current_productions())

        # Test the production has been added to the list of completed productions
        self.assertIn(self.production, history.get_completed_productions())

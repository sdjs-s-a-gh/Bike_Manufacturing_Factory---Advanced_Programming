from unittest import TestCase

from Customer_Class import Customer, ContactInformation, DeliveryAddress
from Production_Class import Production, OutputBin
from Bike_Class import *
from Order_Class import Order

class TestProduction(TestCase):
    def setUp(self):
        """Create a sample Production class and the OutputBin before each test."""
        self.output_bin = OutputBin()

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
        self.production = Production(order)

    def test_initialisation(self):
        # As there is only this production bike, the output bin's components should match.
        self.assertEqual(self.output_bin.get_components_list(), self.production.get_components())
        self.assertEqual(self.production.can_produce_bike(), False)

    def test_get_components(self):
        actual = self.production.get_components()
        expected = ["Bicycle Frame", "Pairs of Wheels", "Gears", "Brakes", "Lights"]
        self.assertEqual(actual, expected)

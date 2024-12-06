from unittest import TestCase
from Customer_Class import *


class TestCustomer(TestCase):
    def setUp(self):
        pass
        self.customer = Customer()
        self.contact_info = ContactInformation()
        self.delivery_address = DeliveryAddress()

class TestContactInformation(TestCase):

    def test_validate_phone_number(self):
        """Testing the private validate_phone_number method through the first argument passed into the ContactInformation
        class"""

        # Normal - raises error
        self.assertRaises(ValueError, ContactInformation("77", "johndoe@gmail.com"))

        # Extreme
        self.assertRaises(ValueError, contact_info = ContactInformation("0234567891", "johndoe@gmail.com"))

    def test_validate_email_address(self):
        """
        Testing the private validate_phone_number method through the second argument passed into the ContactInformation
        class
        """

        # Normal - raises errors
        self.assertRaises(ValueError, ContactInformation("0234567891", "johndoe.com"))
        self.assertRaises(ValueError, ContactInformation("02345678911", "johndoe@gmail.co"))
        self.assertRaises(ValueError, ContactInformation("02345678911", ".com@gmail.co"))
        self.assertRaises(ValueError, ContactInformation("02345678911", ".uk@gmail.co"))

class TestDeliveryAddress(TestCase):
    def setUp(self):
        self.delivery_address = DeliveryAddress(
            house_number="123", street="A690", county="Greater London", town_city="London", postcode="DH1 0NQ"
        )

    def test_initialisation(self):
        pass

    def test_validate_postcode(self):

        # Normal - raises errors
        self.assertRaises(ValueError, DeliveryAddress,
            "123", "A690", "Greater London", "London", "DH1 0000"
        )



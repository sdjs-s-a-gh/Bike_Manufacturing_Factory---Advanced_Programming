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

        # Normal, using a 'with' statement as the class needs to be created inside a function in order to
        # pick up on the constructor raising the error.
        with self.assertRaises(ValueError):
            ContactInformation(phone_number="77", email_address="johndoe@gmail.com")

        # Extreme - there are 10 digits in the phone_number; not the required 11
        with self.assertRaises(ValueError):
            ContactInformation(phone_number="0234567891", email_address="johndoe@gmail.com"),
            # Too many digits (12)
            ContactInformation(phone_number="023456789112", email_address="johndoe@gmail.com")

    def test_validate_email_address(self):
        """
        Testing the private validate_phone_number method through the second argument passed into the ContactInformation
        class
        """

        # Normal - raises errors
        with self.assertRaises(ValueError):
            ContactInformation(phone_number="0234567891", email_address="johndoe.com"),
            ContactInformation(phone_number="02345678911", email_address="johndoe@gmail.co"),
            ContactInformation(phone_number="02345678911", email_address=".com@gmail.co"),
            ContactInformation(phone_number="02345678911", email_address=".uk@gmail.co")


class TestDeliveryAddress(TestCase):
    def setUp(self):
        self.delivery_address = DeliveryAddress(
            house_number="123", street="A690", county="Greater London", town_city="London", postcode="DH1 0NQ"
        )

    def test_initialisation(self):
        pass

    def test_validate_postcode(self):

        # Normal - raises errors
        with self.assertRaises(ValueError):
            # too many characters
            DeliveryAddress(
                house_number="123", street="A690", county="Greater London", town_city="London", postcode="DH1 00000"
            ),
            # too few characters
            DeliveryAddress(
                house_number="123", street="A690", county="Greater London", town_city="London", postcode="DH1 00"
            )



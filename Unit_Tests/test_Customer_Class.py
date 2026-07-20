from unittest import TestCase
from Bike_Factory.Customer_Class import *


class TestCustomer(TestCase):
    def setUp(self):
        """Test if the instance is correctly created by not raising an error."""
        self.contact_information = ContactInformation(phone_number="02345678911", email_address="johnsmith@gmail.com")
        self.delivery_address = DeliveryAddress(
            house_number="123", street="Belle Vue", county="County", town_city="Durham", postcode="DH1 0NQ"
        )
        self.name = "John Smith"
        self.customer = Customer(self.name, self.contact_information, self.delivery_address)

    def test_get_name(self):
        """Test if the name is correctly returned."""
        self.assertEqual(self.customer.get_name(), self.name)

    def test_get_details(self):
        self.assertEqual(self.customer.get_details(), [
            self.name, self.contact_information.get_details(), self.delivery_address.get_details()
        ])

class TestContactInformation(TestCase):
    def setUp(self):
        """Test if the instance correctly allows for contact information."""
        self.contact_info = ContactInformation(phone_number="02345678911", email_address="johnsmith@gmail.com")

    def test_validate_phone_number(self):
        """Test if the instance correctly raises errors for invalid phone numbers."""

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
        """Test if the instance correctly raises errors for invalid phone numbers."""

        # Normal - raises errors
        with self.assertRaises(ValueError):
            ContactInformation(phone_number="0234567891", email_address="johndoe.com"),
            ContactInformation(phone_number="02345678911", email_address="johndoe@gmail.co"),
            ContactInformation(phone_number="02345678911", email_address=".com@gmail.co"),
            ContactInformation(phone_number="02345678911", email_address=".uk@gmail.co")


class TestDeliveryAddress(TestCase):
    def setUp(self):
        """Test if the instance correctly allows for valid delivery details."""
        self.delivery_address = DeliveryAddress(
            house_number="123", street="A690", county="Greater London", town_city="London", postcode="DH1 0NQ"
        )

    def test_validate_postcode(self):
        """Test if the instance correctly raises errors for invalid postcodes."""

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



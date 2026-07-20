class Customer:
    def __init__(self, name: str, contact_information, delivery_address):
        self.__name = name
        self.__contact_information: ContactInformation = contact_information
        self.__delivery_address: DeliveryAddress = delivery_address

    def get_details(self) -> list:
        """
        A getter function that returns all details of the customer: their name, contact information and
        delivery address.

        Returns:
            list: A list of all details of the customer. The second [1] and third [2] indexes are both lists themselves.
        """
        details = [self.__name, self.__contact_information.get_details(), self.__delivery_address.get_details()]
        return details

    def get_name(self) -> str:
        """
        A getter function that returns the name of the customer.

        Returns:
            str: The name of the customer.
        """
        return self.__name

    def get_contact_information(self) -> list:
        """
        A getter function that returns the contact information of the customer: their phone number and email address.

        Returns:
            list: A list of all the contact details of the customer: phone number and email address.
            """
        return self.__contact_information.get_details()

    def get_delivery_address(self) -> list:
        """
        A getter function that returns the delivery address of the customer.

        Returns:
            list: A list of all the delivery address details of the customer.
        """
        return self.__delivery_address.get_details()

    # Allows me to hash the customers to put them in a set
    def __eq__(self, other):
        if not isinstance(other, Customer):
            return False
        return (
                self.__name == other.__name and
                self.__contact_information.get_details() == other.__contact_information.get_details()
                # No need to compare delivery address if the contact info is the same. Also a person may move house
                # or live at multiple anyways.
             )

    def __hash__(self):
        # Convert contact information to a tuple (to ensure it's immutable and hashable)
        return hash((self.__name, tuple(self.__contact_information.get_details())))

    def __str__(self):
        return (f"\t Full Name: {self.__name} \n\t Contact Information: {self.__contact_information}"
                f"\n\t Delivery Address: {self.__delivery_address}")


class ContactInformation:
    def __init__(self, phone_number: str, email_address: str):
        self.__phone_number: str = self.__validate_phone_number(phone_number)
        self.__email_address: str = self.__validate_email(email_address)

    @staticmethod   # as neither of these functions explicitly modify an attribute nor use one, making the self
    # argument redundant
    def __validate_phone_number(phone_number: str) -> str:
        """
        A private function used on instantiation to determine whether the phone number entered is valid. If the number
        is valid, the attribute __phone_number is updated. Otherwise, a ValueError is raised.

        Args:
            phone_number(str): The phone number entered for the contact information.

        Returns:
            str: The phone number entered for the contact information - should it be valid.

        Raises: ValueError: If the phone number entered is not equal to 11 digits long or if the first digit is not 0
        (zero).

        Example:
            02345678911
        """

        if len(phone_number) != 11 and phone_number[0] != 0:
            raise ValueError("The phone number must be at least 11 digits long")
        # else, the number is valid
        return phone_number

    @staticmethod
    def __validate_email(email_address: str) -> str:
        """
        A private function used on instantiation to determine whether the email address entered is valid. If the email
        is valid, the attribute __email_address is updated. Otherwise, a ValueError is raised.

        Args:
            email_address(str): The phone number entered for the contact information.

        Returns:
            str: The email address entered for the contact information - should it be valid.

        Raises: ValueError: If the email address entered does not contain an at sign (@) or a domain name (.com or .co.uk).
        Or, if a domain name is present but not located at the end of the email address.

        Examples:
            johndoe@gmail.com
            johndoe@gmail.co.uk
        """
        # Without importing regex

        # Remove all whitespaces (leading, trailing and internal) if there are any
        stripped_email = email_address.replace(" ", "")

        if "@" not in stripped_email or not (".com" in stripped_email or ".co.uk" in stripped_email):
            raise ValueError("The email address must contain an at sign (@) and a domain name (either .com or .co.uk).)")
        elif stripped_email[len(stripped_email)-4:] != ".com" and stripped_email[len(stripped_email)-6:] != ".co.uk":
            raise ValueError("The domain name must be at the very end of the email.")
        else:
            return stripped_email

    def get_details(self) -> list:
        """A getter function that returns a list of the customer's phone number and email address.

        Returns:
            list: A list of the customer's phone number and email address.
            """
        details = [self.__phone_number, self.__email_address]
        return details

    def __str__(self):
        return f"\n\t\t Phone Number: {self.__phone_number},\n\t\t Email Address: {self.__email_address}"


class DeliveryAddress:
    def __init__(self, house_number: str, street: str, county: str, town_city: str, postcode: str):
        self.__house_number: str = house_number  # they may live in an apartment; for example: 123a. Or a named house.
        self.__street: str = street
        self.__county: str = county
        self.__town_city: str = town_city
        self.__postcode: str = self.__validate_postcode(postcode)

    @staticmethod
    def __validate_postcode(postcode: str) -> str:
        """
        A private class used on instantiation to determine whether the postcode entered is valid. If the postcode
        is valid, the attribute __postcode is updated. Otherwise, a ValueError is raised.

        Args:
            postcode(str): The postcode entered for the delivery address.

        Returns:
            str: The postcode address entered for the delivery address - should it be valid.

        Raises: ValueError: If the postcode does not match the format LL09 0LL, where L = Letter, 0 = mandatory number,
                             9 = optional number

        Examples:
            ZH1 0FR - with or without the space inbetween
            ZH12 0GD
        """
        # remove middle space
        stripped_postcode = postcode.replace(" ", "")

        if len(stripped_postcode) != 6 and len(stripped_postcode) != 7:  # originally in the format ZH1 0FR or ZH12 0GD
            raise ValueError("The postcode must be in the format LL09 0LL, where L = Letter, 0 = mandatory number,"
                             "9 = optional number")
        # else
        return stripped_postcode

    def get_details(self) -> list:
        """A getter function that returns a list of information about the customer's delivery address.

        Returns:
            list: A list of all the delivery address details of the customer.
            """
        details = [self.__house_number, self.__street, self.__county, self.__town_city, self.__postcode]
        return details

    def __str__(self):
        return (f"\n\t\t House Number/Title: {self.__house_number}, \n\t\t Street: {self.__street},"
                f" \n\t\t County: {self.__county}, \n\t\t Town/City: {self.__town_city},"
                f" \n\t\t Postcode: {self.__postcode}")

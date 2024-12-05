class Customer:
    def __init__(self, name: str, contact_information, delivery_address):
        self.__name = name
        self.__contact_information: ContactInformation = contact_information
        self.__delivery_address: DeliveryAddress = delivery_address


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
        """

        if len(phone_number) != 11 and phone_number[0] != 0:
            raise ValueError("The phone number must be at 11 digits long and the fist digit must also be 0 (zero)")
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
        occurrence = {"@": 0, ".com": 0, ".co.uk": 0}  # "." may appear multiple times
        for char in email_address:
            if char in occurrence:
                occurrence[char] += 1

        # Remove all whitespaces (leading, trailing and internal) if there are any
        stripped_email = email_address.replace(" ", "")

        if occurrence["@"] != 1 and (occurrence[".com"] != 1 or occurrence[".co.uk"] != 1):
            raise ValueError("The email address must contain an at sign (@) and a domain name (either .com or .co.uk).)")
        elif stripped_email[len(stripped_email)-4:] != ".com" and stripped_email[len(stripped_email)-6:] != ".co.uk":
            raise ValueError("The domain name must be at the very end of the email.")
        else:
            return stripped_email


class DeliveryAddress:
    def __init__(self, house_number: str, street: str, county: str, town_city: str, postcode: str):
        self.__house_number: str = house_number  # they may live in an apartment; for example: 123a
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

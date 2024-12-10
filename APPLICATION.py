import sys

from Bike_Class import *
from Customer_Class import *
from Production_Class import *

from PySide6.QtCore import Qt, QRegularExpression, QDate, QAbstractTableModel, QModelIndex, QRect
from PySide6.QtGui import *
from PySide6.QtWidgets import (
    QApplication, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMenuBar, QPushButton, QVBoxLayout, QWidget, QComboBox,
    QMessageBox, QDateEdit, QTableView, QStyledItemDelegate, QAbstractItemView, QStyleOptionViewItem
)

from Order_Class import Order


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assembly Line")
        # self.setMenuBar(QMenuBar)
        self.resize(960, 540)
        self.order_entry = OrderEntryWindow()

        # Create Widgets
        btn_open_order_entry_window = QPushButton("Order Entry")

        # Connect widgets to methods
        btn_open_order_entry_window.clicked.connect(self.toggle_window)

        # Create Models for the Inventory table
        components_dict = inventory.get_components_dict()
        self.data = [[component, stock] for component, stock in components_dict.items()]

        self.inventory_model = CustomTableModel(self.data)
        self.table_view = QTableView(self)
        self.table_view.setModel(self.inventory_model)

        custom_delegate = CustomDelegate(self)
        self.table_view.setItemDelegateForColumn(1, custom_delegate)

        # Components that need to be restocked, which will be shown in a label
        self.restock_list = []

        # Layout Setup
        self.lbl_restock = QLabel("")
        # self.lbl_restock.hide()

        inventory_layout = QVBoxLayout()
        inventory_layout.addWidget(self.table_view)
        inventory_layout.addWidget(self.lbl_restock)

        main_layout = QHBoxLayout()
        main_layout.addLayout(inventory_layout)
        main_layout.addWidget(btn_open_order_entry_window, alignment=Qt.AlignmentFlag.AlignBottom)
        main_layout_widget = QWidget()
        main_layout_widget.setLayout(main_layout)
        self.setCentralWidget(main_layout_widget)

    def get_restock_list(self) -> list[str]:
        return self.restock_list

    def add_restock(self, component: str) -> None:
        self.restock_list.append(component)

    def remove_restock(self, component: str) -> None:
        self.restock_list.remove(component)

    def set_restock_message(self) -> None:
        if len(self.restock_list) > 0:
            self.lbl_restock.setText(f"The following components need to be restocked:"
                                     f" {str(self.restock_list).replace("'", "").replace("[", "").replace("]", "")}.")
            # The replace methods remove the list parentheses, making it more professional
            self.lbl_restock.show()
        else:
            self.lbl_restock.hide()


    def toggle_window(self):
        if self.order_entry.isVisible():
            self.order_entry.hide()
        else:
            self.order_entry.show()


class CustomTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.__data = data

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and index.isValid():
            return self.__data[index.row()][index.column()]

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return ["Component", "Stock"][section]
            elif orientation == Qt.Orientation.Vertical:
                return section + 1      # Row Numbers

    def rowCount(self, parent=QModelIndex()):
        return len(self.__data)

    def columnCount(self, parent=QModelIndex()):
        if self.__data:
            return len(self.__data[0])
        # else
        return 0


class CustomDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Checking if the stock falls below 3 on external components, prompting a restocking

        stock = index.data(Qt.ItemDataRole.DisplayRole)

        # Get the component associated with the current cell's stock
        component_name = index.siblingAtColumn(0).data()

        internal_components = ["Forks", "Frames", "Front Fork"]

        if component_name not in internal_components and stock < 3:
            painter.fillRect(option.rect, QColor(250, 0, 0))

            # Add component to the restock message
            if component_name not in window.get_restock_list():
                window.add_restock(component_name)
        else:
            # If the component is currently in restock message, remove it so it isn't shown
            if component_name in window.get_restock_list():
                window.remove_restock(component_name)

        painter.drawText(option.rect, str(stock))
        window.set_restock_message()



class OrderEntryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Order Entry")
        self.resize(960, 540)

        # Create Widgets
        lbl_order_date = QLabel("Order Date")
        self.order_date = QDateEdit()
        self.order_date.setDisplayFormat("dd/MM/yyyy")
        self.order_date.setDate(QDate.currentDate())
        btn_submit = QPushButton("Submit")

        # - Customer Entry

        lbl_customer_data_entry = QLabel("Customer Data Entry:")
        lbl_name = QLabel("Customer Full Name")
        self.txt_name = QLineEdit()
        self.txt_name.setMaximumWidth(100)
        self.txt_name.setMaxLength(25)
        self.txt_name.setPlaceholderText("John Doe")
        alphabet_only_validator = QRegularExpressionValidator(QRegularExpression("^[A-Za-z]+( [A-Za-z]+)*"))
        self.txt_name.setValidator(alphabet_only_validator)

        lbl_contact_information = QLabel("Contact Information:")
        self.lbl_phone_number = QLabel("Phone Number")
        self.txt_phone_number = QLineEdit()
        self.txt_phone_number.setMaximumWidth(100)
        self.txt_phone_number.setMaxLength(11)
        self.txt_phone_number.setPlaceholderText("01234567891")
        phone_validator = QRegularExpressionValidator(QRegularExpression("^0[0-9]*"))
        self.txt_phone_number.setValidator(phone_validator)

        lbl_email_address = QLabel("Email Address")
        self.txt_email_address = QLineEdit()
        self.txt_email_address.setMaximumWidth(140)
        self.txt_email_address.setMaxLength(40)
        self.txt_email_address.setPlaceholderText("example@gmail.com")
        # Validation in the DeliveryAddress class will catch exceptions

        lbl_delivery_address = QLabel("Delivery Address:")
        lbl_house_number = QLabel("House Number or Title")
        self.txt_house_number = QLineEdit()
        self.txt_house_number.setMaximumWidth(140)
        self.txt_house_number.setMaxLength(20)
        self.txt_house_number.setPlaceholderText("10, 123a, Village House")
        house_number_validator = QRegularExpressionValidator(QRegularExpression("([0-9]+[A-Za-z]?)|([A-Za-z]+ [A-Za-z]*)"))
        self.txt_house_number.setValidator(house_number_validator)

        lbl_street_name = QLabel("Street Name")
        self.txt_street_name = QLineEdit()
        self.txt_street_name.setMaximumWidth(100)
        self.txt_street_name.setMaxLength(25)
        self.txt_street_name.setPlaceholderText("Wood Drive")
        self.txt_street_name.setValidator(alphabet_only_validator)

        lbl_county = QLabel("County")
        self.txt_county = QLineEdit()
        self.txt_county.setMaximumWidth(100)
        self.txt_county.setMaxLength(25)
        self.txt_county.setPlaceholderText("Tyne and Wear")
        self.txt_county.setValidator(alphabet_only_validator)

        lbl_town_city = QLabel("Town or City")
        self.txt_town_city = QLineEdit()
        self.txt_town_city.setMaximumWidth(100)
        self.txt_county.setMaxLength(25)
        self.txt_town_city.setPlaceholderText("Sunderland")
        self.txt_town_city.setValidator(QRegularExpressionValidator("^[A-Za-z]+"))

        lbl_postcode = QLabel("Postcode")
        self.txt_postcode = QLineEdit()
        self.txt_postcode.setMaximumWidth(100)
        self.txt_postcode.setMaxLength(7)
        self.txt_postcode.setPlaceholderText("SR5 1SU")
        self.txt_postcode.setInputMask(">AA90 9AA")
        # formatting in the customer class/exception is different because that's what and I also think is more intuitive

        # - Order Entry
        lbl_bike_order_entry = QLabel("Bike Order Entry:")
        lbl_bike = QLabel("Type of Bike")
        self.cbo_bike = QComboBox()
        self.cbo_bike.addItems(["Standard", "Sport"])
        # Standard bike does not have the option for a drink holder
        self.cbo_bike.currentIndexChanged.connect(self.button_visibility)

        lbl_size = QLabel("Bike Size")
        self.cbo_size = QComboBox()
        self.cbo_size.addItems(["Small", "Medium", "Large", "Extra Large"])

        lbl_colour = QLabel("Bike Colour")
        self.cbo_colour = QComboBox()
        self.cbo_colour.addItems(["Red", "Blue", "Green", "Black", "White", "Yellow", "Pink"])

        lbl_wheel_size = QLabel("Wheel Size")
        self.cbo_wheel_size = QComboBox()
        self.wheel_sizes = {"26 inches": 26, "27.5 inches": 27.5, "29 inches": 29, "40 inches": 40}
        self.cbo_wheel_size.addItems([key for key in self.wheel_sizes])

        # Component Combinations
        lbl_gear_type = QLabel("Gear Type")
        self.cbo_gear_type = QComboBox()
        self.cbo_gear_type.addItems(["Standard", "Premium"])

        lbl_brake_type = QLabel("Brake Type")
        self.cbo_brake_type = QComboBox()
        self.cbo_brake_type.addItems(["Disc", "Rim"])

        lbl_light_type = QLabel("Light Type")
        self.cbo_light_type = QComboBox()
        self.cbo_light_type.addItems(["Standard", "LED"])

        self.lbl_drink_holder = QLabel("Drink Holder")
        self.cbo_drink_holder = QComboBox()
        self.drink_holder_option = {"Yes": True, "No": False}
        self.cbo_drink_holder.addItems([key for key in self.drink_holder_option])

        # Default status of the drink holder option
        self.lbl_drink_holder.hide()
        self.cbo_drink_holder.hide()

        # Layout Setup
        customer_layout = QVBoxLayout()
        customer_layout.addWidget(lbl_customer_data_entry)
        customer_layout.addWidget(lbl_name)
        customer_layout.addWidget(self.txt_name)
        customer_layout.addWidget(lbl_contact_information)
        customer_layout.addWidget(self.lbl_phone_number)
        customer_layout.addWidget(self.txt_phone_number)
        customer_layout.addWidget(lbl_email_address)
        customer_layout.addWidget(self.txt_email_address)
        customer_layout.addWidget(lbl_delivery_address)
        customer_layout.addWidget(lbl_house_number)
        customer_layout.addWidget(self.txt_house_number)
        customer_layout.addWidget(lbl_street_name)
        customer_layout.addWidget(self.txt_street_name)
        customer_layout.addWidget(lbl_county)
        customer_layout.addWidget(self.txt_county)
        customer_layout.addWidget(lbl_town_city)
        customer_layout.addWidget(self.txt_town_city)
        customer_layout.addWidget(lbl_postcode)
        customer_layout.addWidget(self.txt_postcode)

        order_layout = QVBoxLayout()
        order_layout.addWidget(lbl_bike_order_entry)
        order_layout.addWidget(lbl_bike)
        order_layout.addWidget(self.cbo_bike)
        order_layout.addWidget(lbl_size)
        order_layout.addWidget(self.cbo_size)
        order_layout.addWidget(lbl_colour)
        order_layout.addWidget(self.cbo_colour)
        order_layout.addWidget(lbl_wheel_size)
        order_layout.addWidget(self.cbo_wheel_size)
        order_layout.addWidget(lbl_gear_type)
        order_layout.addWidget(self.cbo_gear_type)
        order_layout.addWidget(lbl_brake_type)
        order_layout.addWidget(self.cbo_brake_type)
        order_layout.addWidget(lbl_light_type)
        order_layout.addWidget(self.cbo_light_type)
        order_layout.addWidget(self.lbl_drink_holder)
        order_layout.addWidget(self.cbo_drink_holder)

        date_layout = QVBoxLayout()
        date_layout.addWidget(lbl_order_date, alignment=Qt.AlignmentFlag.AlignVCenter)
        date_layout.addWidget(self.order_date, alignment=Qt.AlignmentFlag.AlignTop)

        main_layout = QHBoxLayout()
        main_layout.addLayout(customer_layout)
        main_layout.addLayout(order_layout)
        main_layout.addLayout(date_layout)

        main_layout.addWidget(btn_submit)

        self.setLayout(main_layout)

        # Connect widgets to methods
        btn_submit.clicked.connect(self.complete_order)

    def button_visibility(self) -> None:
        """A subroutine that dynamically changes the visibility of the specific labels and buttons on the screen; as
        opposed to hard-coding values. This is beneficial as the subroutine grants the platform to be more scalable,
        allowing more bike classes to be created without having to hardcode each and every label and button.
         """

        # All new components that are not included at standard
        component_lbl_btn_mapping = {"Drink Holder": [self.lbl_drink_holder, self.cbo_drink_holder]}

        # Initially, hide all labels/buttons
        for component in component_lbl_btn_mapping:
            lbl: QLabel = component_lbl_btn_mapping[component][0]
            btn: QPushButton = component_lbl_btn_mapping[component][1]
            lbl.hide()
            btn.hide()

        match self.cbo_bike.currentText():
            # Need to create temp instances to get components of specific classes
            case "Standard":
                bike = Bike("Big","Blue",26, "Standard", "Rim", "Standard")
            case "Sport":
                bike = SportBike("Small", "Red", 26, "Disc", "LED", True)
            case _:
                pass

        # Additional Components that may be shown
        bike_components: list[str] = bike.get_components()
        standard_bike_components: list[str] = [
            "Front Fork", "Pedals", "Pairs of Wheels", "Gears", "Brakes", "Lights", "Seats"]

        # Highlights additional components that the bike has, such as a drink holder
        components_to_show: list[str] = [
            component for component in bike_components if component not in standard_bike_components]

        for component in components_to_show:
            lbl: QLabel = component_lbl_btn_mapping[component][0]
            btn: QPushButton = component_lbl_btn_mapping[component][1]
            lbl.show()
            btn.show()

    def complete_order(self):
        # Check Nulls
        if self.check_nulls() is False:
            name = self.txt_name.text()
            phone_number = self.txt_phone_number.text()
            email_address = self.txt_email_address.text()
            house_number = self.txt_house_number.text()
            street_name = self.txt_street_name.text()
            county = self.txt_county.text()
            town_city = self.txt_town_city.text()
            postcode = self.txt_postcode.text()

            bike = self.cbo_bike.currentText()
            size = self.cbo_size.currentText()
            colour = self.cbo_colour.currentText()
            wheel_size = self.wheel_sizes[self.cbo_wheel_size.currentText()]    # convert str to float
            gear = self.cbo_gear_type.currentText()
            brake = self.cbo_brake_type.currentText()
            light = self.cbo_light_type.currentText()
            drink_holder = self.drink_holder_option[self.cbo_drink_holder.currentText()]
            order_date = self.order_date.text()

            # Rather than crash the program, the following code will present the error to the user.
            try:
                contact_info = ContactInformation(phone_number, email_address)
                delivery_info = DeliveryAddress(house_number, street_name, county, town_city, postcode)
                customer = Customer(name, contact_info, delivery_info)

                # Would be more efficient if Python had compile-time polymorphism, so I would not have to specify the
                # type of bike.
                match self.cbo_bike.currentText():
                    case "Standard":
                        bike = Bike(size, colour, wheel_size, gear, brake, light)
                    case "Sport":
                        bike = SportBike(size, colour, wheel_size, gear, light, drink_holder)

                order = Order(bike, customer, order_date)

                production = Production(order)

            except Exception as x:
                QMessageBox.critical(self, "Error", str(x))
            # If successful
            QMessageBox.information(self, "Order Submitted", str(production))
            # Clean up
            self.clear()
        else:
            QMessageBox.critical(self, "Null Error", "You have not entered information into every field.")

    def check_nulls(self) -> bool:
        return not (
                self.txt_name.text() and self.txt_phone_number.text() and self.txt_email_address.text() and
                self.txt_house_number.text() and self.txt_street_name.text() and self.txt_county.text() and
                self.txt_town_city.text() and self.txt_postcode.text())

    def clear(self) -> None:
        self.order_date.clear()

        self.txt_name.clear()
        self.txt_phone_number.clear()
        self.txt_email_address.clear()
        self.txt_house_number.clear()
        self.txt_street_name.clear()
        self.txt_county.clear()
        self.txt_town_city.clear()
        self.txt_postcode.clear()

        self.cbo_bike.setCurrentIndex(0)
        self.cbo_size.setCurrentIndex(0)
        self.cbo_colour.setCurrentIndex(0)
        self.cbo_wheel_size.setCurrentIndex(0)
        self.cbo_gear_type.setCurrentIndex(0)
        self.cbo_brake_type.setCurrentIndex(0)
        self.cbo_drink_holder.setCurrentIndex(0)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

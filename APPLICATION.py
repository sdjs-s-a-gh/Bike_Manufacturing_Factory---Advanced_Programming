import sys

from Bike_Class import *
from Customer_Class import *
from Production_Class import *

from PySide6.QtCore import Qt, QRegularExpression, QDate, QAbstractTableModel, QModelIndex, QRect
from PySide6.QtGui import *
from PySide6.QtWidgets import (
    QApplication, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMenuBar, QPushButton, QVBoxLayout, QWidget, QComboBox,
    QMessageBox, QDateEdit, QTableView, QStyledItemDelegate, QAbstractItemView, QStyleOptionViewItem, QInputDialog,
    QGridLayout
)

from Order_Class import Order


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assembly Line")
        # self.setMenuBar(QMenuBar)
        self.resize(960, 750)
        self.order_entry = OrderEntryWindow()

        # Create Widgets

        header_typography = QFont()
        header_typography.setBold(True)
        header_typography.setPointSize(12)
        sub_header_typography = QFont()
        sub_header_typography.setBold(True)
        sub_header_typography.setPointSize(9)

        # - Assembly Line
        btn_open_order_entry_window = QPushButton("Order Entry")
        lbl_assembly_line = QLabel("Assembly Line")
        lbl_assembly_line.setFont(header_typography)
        btn_frame_assembly = QPushButton("Frame Assembly")
        btn_fork_assembly = QPushButton("Fork Assembly")
        btn_front_fork_assembly = QPushButton("Front Fork Assembly")
        btn_painted_parts = QPushButton("Painted Parts")
        btn_pedal_addition = QPushButton("Pedal Addition")
        btn_wheel_addition = QPushButton("Wheel Addition")
        btn_gear_addition = QPushButton("Gear Addition")
        btn_brake_addition = QPushButton("Brake Addition")
        btn_light_addition = QPushButton("Light Addition")
        btn_seat_addition = QPushButton("Seat Addition")
        btn_drink_holder_addition = QPushButton("Drink Holder Addition")
        btn_front_rack_addition = QPushButton("Front Rack Addition")
        btn_rear_rack_addition = QPushButton("Rear Rack Addition")
        btn_mudflaps_addition = QPushButton("Mudflaps Addition")
        btn_child_seat_addition = QPushButton("Child Seat Addition")

        self.assembly_line_buttons = [
            btn_frame_assembly, btn_fork_assembly, btn_front_fork_assembly, btn_painted_parts, btn_pedal_addition,
            btn_wheel_addition, btn_gear_addition, btn_brake_addition, btn_light_addition, btn_seat_addition,
            btn_drink_holder_addition, btn_front_rack_addition, btn_rear_rack_addition, btn_mudflaps_addition,
            btn_child_seat_addition
        ]

        # -- Bike Status / Production Table
        lbl_bike_status = QLabel("Bike Status / Production Bin")
        lbl_bike_status.setFont(sub_header_typography)
        self.lbl_production = QLabel("There are no bikes currently in production.")

        # - Inventory
        lbl_inventory = QLabel("Inventory")
        lbl_inventory.setFont(header_typography)
        btn_auto_restock = QPushButton("Auto Restock")
        lbl_restock_hint = QLabel("To manually restock, please select a row from the table. Once presented with a"
                                  " dialog box, enter a specified number to restock.")
        lbl_restock_hint.setWordWrap(True)

        # - Create Models for the Production and Inventory table

        # -- Production
        self.production_table_view = None
        self.production_model = None
        self.check_production()

        # -- Inventory
        components_dict = inventory.get_components_dict()
        inventory_data = [[component, stock] for component, stock in components_dict.items()]

        self.inventory_model = CustomTableModel(inventory_data, ["Component", "Stock"])
        self.table_view = QTableView(self)
        self.table_view.setModel(self.inventory_model)
        # self.table_view.resizeColumnsToContents()
        self.table_view.setFixedWidth(225)
        # self.table_view.setFixedSize(225, 450)

        # -- Create custom delegate for the inventory model that will alter the appearance of cells depending on their
        # stock
        inventory_custom_delegate = InventoryCustomDelegate(self)
        self.table_view.setItemDelegateForColumn(1, inventory_custom_delegate)

        # - Components that need to be restocked, which will be shown in a label
        self.restock_list = []

        # Connect widgets to methods
        btn_open_order_entry_window.clicked.connect(self.toggle_window)
        self.table_view.clicked.connect(self.on_cell_click)     # specific cell that is clicked
        btn_auto_restock.clicked.connect(self.auto_restock)

        self.bike_frame = None  # assigned a value through the Order Entry Screen
        fork = Fork()
        front_fork = FrontFork()
        painted_part = PaintedPart()
        wheel = Component("Pairs of Wheels", )

        # Using a lambda function to stop the button from executing during setup (because the function contains an
        # argument rather than just the method name and so it tries to execute)
        btn_frame_assembly.clicked.connect(lambda: self.add_inhouse_component(self.bike_frame))
        btn_fork_assembly.clicked.connect(lambda: self.add_inhouse_component(fork))
        btn_front_fork_assembly.clicked.connect(lambda: self.add_inhouse_component(front_fork))
        btn_painted_parts.clicked.connect(lambda: self.add_inhouse_component(painted_part))
        btn_wheel_addition.clicked.connect(self.add_inhouse_component)
        btn_gear_addition.clicked.connect(self.add_inhouse_component)
        btn_brake_addition.clicked.connect(self.add_inhouse_component)
        btn_light_addition.clicked.connect(self.add_inhouse_component)
        btn_seat_addition.clicked.connect(self.add_inhouse_component)
        btn_drink_holder_addition.clicked.connect(self.add_inhouse_component)
        btn_front_rack_addition.clicked.connect(self.add_inhouse_component)
        btn_rear_rack_addition.clicked.connect(self.add_inhouse_component)
        btn_mudflaps_addition.clicked.connect(self.add_inhouse_component)
        btn_child_seat_addition.clicked.connect(self.add_inhouse_component)

        # Layout Setup

        # - Create Menubar at the top of the screen
        self.create_menubar()

        self.main_layout = QGridLayout()
        # - Assembly Line
        self.main_layout.addWidget(lbl_assembly_line, 0, 0)
        self.main_layout.addWidget(lbl_bike_status, 17, 0)   # change
        self.main_layout.addWidget(self.lbl_production, 18, 0)   # change
        self.main_layout.addWidget(btn_frame_assembly, 1, 0)
        self.main_layout.addWidget(btn_fork_assembly, 2, 0)
        self.main_layout.addWidget(btn_front_fork_assembly, 4, 0)
        self.main_layout.addWidget(btn_painted_parts, 5, 0)
        self.main_layout.addWidget(btn_pedal_addition, 6, 0)
        self.main_layout.addWidget(btn_wheel_addition, 7, 0)
        self.main_layout.addWidget(btn_gear_addition, 8, 0)
        self.main_layout.addWidget(btn_brake_addition, 9, 0)
        self.main_layout.addWidget(btn_light_addition, 10, 0)
        self.main_layout.addWidget(btn_seat_addition, 11, 0)
        self.main_layout.addWidget(btn_drink_holder_addition, 12, 0)
        self.main_layout.addWidget(btn_front_rack_addition, 13, 0)
        self.main_layout.addWidget(btn_rear_rack_addition, 14, 0)
        self.main_layout.addWidget(btn_mudflaps_addition, 15, 0)
        self.main_layout.addWidget(btn_child_seat_addition, 16, 0)

        #if self.production_table_view is not None:
         #   self.main_layout.addWidget(self.production_table_view, 1, 1, 8, 1)

        # - Inventory
        self.main_layout.addWidget(lbl_inventory, 0, 5)
        self.main_layout.addWidget(self.table_view, 1, 5, 18, 1)  # row 1-18, col 1
        self.main_layout.addWidget(btn_auto_restock, 1, 9)
        self.main_layout.addWidget(lbl_restock_hint, 2, 9)
        self.lbl_restock_message = QLabel("")
        self.lbl_restock_message.setWordWrap(True)
        self.main_layout.addWidget(self.lbl_restock_message, 5, 9)   # items that need restocking

        self.main_layout.addWidget(btn_open_order_entry_window, 0, 11)
        self.main_layout_widget = QWidget()
        self.main_layout_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_layout_widget)

    def get_restock_list(self) -> list[str]:
        return self.restock_list

    def add_restock(self, component: str) -> None:
        self.restock_list.append(component)

    def remove_restock(self, component: str) -> None:
        self.restock_list.remove(component)

    def set_restock_message(self) -> None:
        if len(self.restock_list) > 0:
            self.lbl_restock_message.setText(
                f"The following components need to be restocked:"
                f" {str(self.restock_list).replace("'", "").replace("[", "").replace("]", "")}."
            )
            # The replace methods remove the list parentheses, making it more readable
            self.lbl_restock_message.show()
        else:
            self.lbl_restock_message.hide()

    def on_cell_click(self, index) -> None:

        row = index.row()

        component = self.inventory_model.data(self.inventory_model.index(row, 0))

        # If the component is not made in-house
        if component not in inventory.get_internal_components():
            try:
                value, ok = QInputDialog.getInt(
                    self,
                    "Manual Restock",
                    f"How much would you like to restock the '{component}' component by?",
                    value=0,
                    minValue=0,
                    maxValue=30,
                    step=1
                )
                if ok and value > 0:
                    # Increment the stock in the inventory instance.
                    inventory.increment_component_count(component, value)

                    # As the model's data does not keep in sync with the inventory, tell the model to base its data of
                    # the inventory again - rather than have a synchronous method update the separate data in the
                    # current cell.
                    self.inventory_model.update_data(
                        [[component, stock] for component, stock in inventory.get_components_dict().items()]
                    )

                    new_stock = inventory.get_components_dict()[component]
                    QMessageBox.information(self, f"{component} successfully Restocked",
                                            f"There are now {new_stock} {component} in stock.")
            except ValueError as x:
                # If the input is <0, display an error message
                QMessageBox.critical(self, "Invalid Input", str(x))

        else:
            QMessageBox.information(self, "In-house Component",
                                    f"The {component} is made in-house and cannot be restocked.")

    def auto_restock(self) -> None:
        value, ok = QInputDialog.getInt(
            self,
            "Auto Restock",
            f"How much would you like to restock all the components by?",
            value=0,
            minValue=0,
            maxValue=30,
            step=1
        )
        if ok and value > 0:
            try:

                # Increment the stock of every component in the inventory instance.
                for component in inventory.get_components_list():

                    # Components that cannot be restocked as they are made in-house
                    if component not in inventory.get_internal_components():
                        inventory.increment_component_count(component, value)

                # Update the model to match the new stock
                self.inventory_model.update_data(
                    [[component, stock] for component, stock in inventory.get_components_dict().items()]
                )

                QMessageBox.information(self, f"Successfully Restocked",
                                        f"There is now {value} more of every component in stock.")
            except ValueError as x:
                # If the input is <0, display an error message
                QMessageBox.critical(self, "Invalid Input", str(x))

    def toggle_window(self) -> None:
        if self.order_entry.isVisible():
            self.order_entry.hide()
        else:
            self.order_entry.show()

    def create_menubar(self) -> None:
        """A subroutine that creates the menubar at the top of the main window. These menus have submenus, however they
        are not functional - as specified in the requirements: (1) "Not needed > Anything to do with saving/loading the
        current state > But menus providing this should be on the interface to do this." and (2) "User Interface
        Components > A menu Bar with at least the standard menu items." """
        menubar = self.menuBar()

        # Standard menu items
        file_menu = menubar.addMenu("File")
        save_submenu = file_menu.addMenu("Save")
        open_submenu = file_menu.addMenu("Open")

        view_menu = menubar.addMenu("View")
        edit_menu = menubar.addMenu("Edit")

    def set_bike_frame(self, frame: Frame) -> None:
        self.bike_frame = frame

    #def add_external_component(self, component: Component) -> None:

    def add_inhouse_component(self, component: Component) -> None:
        try:
            component.create()
        except ValueError as x:
            QMessageBox.critical(self, "Invalid", str(x))
        QMessageBox.information(self, "Component Added", f"1 {component} has been added to the Production Bin.")
        # Update the model views
        self.update_models_views()

    def hide_assembly_line(self) -> None:
        for button in self.assembly_line_buttons:
            button.hide()

    def show_assembly_line(self) -> None:
        for button in self.assembly_line_buttons:
            button.show()

    def check_production(self) -> None:

        bikes_in_production = history.get_current_productions()

        if len(bikes_in_production) > 0:
            self.lbl_production.hide()
            self.show_assembly_line()

            components_needed: list[list] = []
            all_components = [component for component in inventory.get_components_list()]
            column_headers = ["Order ID"] + all_components + ["Can Produce Bike?"]
            production_bin: dict = inventory.get_production_bin()

            # Each row in the table
            for bike in bikes_in_production:
                # Initialise each cell in the row with None
                row = [None] * len(all_components)

                # Overwrite cells with components that are present
                for component in bike.get_components():
                    row[all_components.index(component)] = production_bin[component]

                # Components that are strictly used to create other components or are created from existing components
                indirect_components = ["Frames", "Forks", "Tubular Steel", "Painted Parts"]

                # Add the indirect components to the row
                for component in indirect_components:
                    row[all_components.index(component)] = production_bin[component]

                components_needed.append([bike.get_order_id()] + row + [bike.can_produce_bike()])
            # If the production table view has not been initialised
            if self.production_table_view is None:
                self.production_table_view = QTableView(self)
                self.main_layout.addWidget(self.production_table_view, 18, 0, 8, 12)
                assemblyline_custom_delegate = AssemblyLineCustomDelegate(self)
                self.production_table_view.setItemDelegate(assemblyline_custom_delegate)

                font = QFont()
                font.setPointSize(8)
                self.production_table_view.setFont(font)
                self.production_table_view.resizeColumnsToContents()

            production_data = components_needed
            print(f"all_components: {all_components}; column_headers: {column_headers}")

            self.production_model = CustomTableModel(production_data, column_headers)
            self.production_table_view.setModel(self.production_model)
            self.production_table_view.show()

        else:
            self.lbl_production.show()
            self.hide_assembly_line()

            # Hide the table view if it exists
            if self.production_table_view is not None:
                self.production_table_view = QTableView(self)

    def update_models_views(self) -> None:
        self.check_production()
        # Update the model to match the new stock
        self.inventory_model.update_data(
            [[component, stock] for component, stock in inventory.get_components_dict().items()]
        )

    def closeEvent(self, event) -> None:
        user_input = QMessageBox.critical(
            self, "Confirm Exit", "Are you sure you want to exit the application?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if user_input == QMessageBox.StandardButton.Yes:
            QApplication.quit()
            event.accept()
        else:
            event.ignore()


class CustomTableModel(QAbstractTableModel):
    def __init__(self, data, column_headers: list[str]):
        super().__init__()
        self.__data = data
        self.__column_headers = column_headers

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and index.isValid():
            return self.__data[index.row()][index.column()]

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.__column_headers[section]
            elif orientation == Qt.Orientation.Vertical:
                return section + 1      # Row Numbers

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.__data)

    def columnCount(self, parent=QModelIndex()):
        if self.__data:
            return len(self.__data[0])
        # else
        return 0

    def update_data(self, new_data: list) -> None:
        self.__data = new_data


class InventoryCustomDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index) -> None:
        stock = index.data(Qt.ItemDataRole.DisplayRole)

        # Get the component associated with the current cell's stock
        component_name = index.siblingAtColumn(0).data()

        # Checking if the stock falls below 3 on external components, prompting a restocking
        if component_name not in inventory.get_internal_components() and stock < 3:
            painter.fillRect(option.rect, QColor(250, 0, 0))

            # Add component to the restocking message
            if component_name not in window.get_restock_list():
                window.add_restock(component_name)
        else:
            # If the component is currently in restock message, remove it so it isn't shown
            if component_name in window.get_restock_list():
                window.remove_restock(component_name)

        painter.drawText(option.rect, str(stock))
        window.set_restock_message()


class AssemblyLineCustomDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        stock = index.data(Qt.ItemDataRole.DisplayRole)

        if index.column() != 0:    # ignore the OrderID column
            # Change the colour of the cell depending on the quantity of stock
            if stock is None:
                # Fill black, indicating that component is not used
                painter.fillRect(option.rect, QColor(0, 0, 0))
            elif stock == 0 or stock is False:
                # Fill red, indicating not enough stock
                painter.fillRect(option.rect, QColor(255, 0, 0))
            else:   # stock > 0 or stock is True
                # Fill green, indicating a valid amount of stock.
                painter.fillRect(option.rect, QColor(0, 255, 0))

        # Paint text for the quantity of stock
        painter.drawText(option.rect, str(stock))


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
        self.cbo_bike.addItems(["Standard", "Sport", "Tour", "Commute"])
        # Standard bike does not have the option for a drink holder
        self.cbo_bike.currentIndexChanged.connect(self.set_disabled)

        lbl_size = QLabel("Bike Size")
        self.cbo_size = QComboBox()
        self.cbo_size.addItems(["Small", "Medium", "Large", "Extra Large"])

        lbl_colour = QLabel("Bike Colour")
        self.cbo_colour = QComboBox()
        self.cbo_colour.addItems(["Red", "Blue", "Green", "Black", "White", "Yellow", "Pink"])

        lbl_handlebar_type = QLabel("Handlebar Type")
        self.cbo_handlebar_type = QComboBox()
        self.cbo_handlebar_type.addItems(["Flat", "Aerodynamic"])

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

        lbl_drink_holder = QLabel("Drink Holder")
        self.cbo_drink_holder = QComboBox()
        self.boolean_dict = {"No": False, "Yes": True}
        cbo_boolean_option = [key for key in self.boolean_dict]

        self.cbo_drink_holder.addItems(cbo_boolean_option)

        lbl_front_rack = QLabel("Front Rack")
        self.cbo_front_rack = QComboBox()
        self.cbo_front_rack.addItems(cbo_boolean_option)

        lbl_rear_rack = QLabel("Rear Rack")
        self.cbo_rear_rack = QComboBox()
        self.cbo_rear_rack.addItems(cbo_boolean_option)

        lbl_mudflaps = QLabel("Mudflaps")
        self.cbo_mudflaps = QComboBox()
        self.cbo_mudflaps.addItems(cbo_boolean_option)

        lbl_child_seat = QLabel("Child Seat")
        self.cbo_child_seat = QComboBox()
        self.cbo_child_seat.addItems(cbo_boolean_option)

        # Set all combo boxes interactable to begin with
        self.set_all_interactable()

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
        order_layout.addWidget(lbl_handlebar_type)
        order_layout.addWidget(self.cbo_handlebar_type)
        order_layout.addWidget(lbl_wheel_size)
        order_layout.addWidget(self.cbo_wheel_size)
        order_layout.addWidget(lbl_gear_type)
        order_layout.addWidget(self.cbo_gear_type)
        order_layout.addWidget(lbl_brake_type)
        order_layout.addWidget(self.cbo_brake_type)
        order_layout.addWidget(lbl_light_type)
        order_layout.addWidget(self.cbo_light_type)
        order_layout.addWidget(lbl_drink_holder)
        order_layout.addWidget(self.cbo_drink_holder)
        order_layout.addWidget(lbl_front_rack)
        order_layout.addWidget(self.cbo_front_rack)
        order_layout.addWidget(lbl_rear_rack)
        order_layout.addWidget(self.cbo_rear_rack)
        order_layout.addWidget(lbl_mudflaps)
        order_layout.addWidget(self.cbo_mudflaps)
        order_layout.addWidget(lbl_child_seat)
        order_layout.addWidget(self.cbo_child_seat)

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

    def get_component_mapping(self) -> dict:
        # A dictionary containing all the combo boxes that can be disabled.
        component_cbo_mapping = self.get_additional_component_mapping()
        component_cbo_mapping.update({
            "Handlebar Type": self.cbo_handlebar_type,
            "Gear Type": self.cbo_gear_type,
            "Brake Type": self.cbo_brake_type
        })

        return component_cbo_mapping

    def get_additional_component_mapping(self) -> dict:
        additional_components = {
            "Drink Holder": self.cbo_drink_holder,
            "Front Rack": self.cbo_front_rack,
            "Rear Rack": self.cbo_rear_rack,
            "Mudflaps": self.cbo_mudflaps,
            "Child Seat": self.cbo_child_seat
        }
        return additional_components

    def set_all_interactable(self) -> None:
        """A subroutine used to set all combo boxes to be interactable. """
        components = self.get_component_mapping()
        for component in components.values():
            component: QComboBox = component
            component.setDisabled(False)
            component.setCurrentIndex(0)

    def set_disabled(self) -> None:
        """A subroutine that sets specific combo boxes to be read-only based on the class of bike chosen."""

        # Initially reset all combo boxes to be interactable
        self.set_all_interactable()

        match self.cbo_bike.currentText():
            case "Standard":
                bike = Bike
            case "Sport":
                bike = SportBike
            case "Tour":
                bike = TourBike
            case _:
                bike = CommuteBike

        # Disable specified components and set their index to the indicated value. For example, a SportBike will have
        # the Handlebar Type option disabled and the index will be set to 1, which will read "Aerodynamic".
        disable_combo_box = self.get_component_mapping()
        if self.cbo_bike.currentText() != "Commute":    # as Commute.non_interactable components = None
            for combo_box in bike.non_interactable_components:
                cbo: QComboBox = disable_combo_box[combo_box[0]]   # index 0 = combo box
                cbo.setDisabled(True)
                cbo.setCurrentIndex(combo_box[1])   # index 1 = set index

        # Disable additional components the bike chosen does not have access to. For instance, the standard bike does
        # not have a 'Drink Holder' option, and consequently this will be disabled.
        additional_components = self.get_additional_component_mapping()
        for component in additional_components:
            if component not in bike.possible_components:
                cbo: QComboBox = additional_components[component]
                cbo.setDisabled(True)

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

            model = self.cbo_bike.currentText()
            size = self.cbo_size.currentText()
            colour = self.cbo_colour.currentText()
            handlebar_type = self.cbo_handlebar_type.currentText()
            wheel_size = self.wheel_sizes[self.cbo_wheel_size.currentText()]    # convert str to float
            gear = self.cbo_gear_type.currentText()
            brake = self.cbo_brake_type.currentText()
            light = self.cbo_light_type.currentText()
            drink_holder = self.boolean_dict[self.cbo_drink_holder.currentText()]
            front_rack = self.boolean_dict[self.cbo_front_rack.currentText()]
            rear_rack = self.boolean_dict[self.cbo_rear_rack.currentText()]
            mudflaps = self.boolean_dict[self.cbo_mudflaps.currentText()]
            child_seat = self.boolean_dict[self.cbo_child_seat.currentText()]
            order_date = self.order_date.text()

            types_of_frames: dict = {
                "Small": SmallFrame(model),
                "Medium": MediumFrame(model),
                "Large": LargeFrame(model),
                "Extra Large": ExtraLargeFrame(model)
            }
            # Rather than crash the program, the following code will present the error to the user.
            try:
                contact_info = ContactInformation(phone_number, email_address)
                delivery_info = DeliveryAddress(house_number, street_name, county, town_city, postcode)
                customer = Customer(name, contact_info, delivery_info)

                # Would be more efficient if Python had compile-time polymorphism, so I would not have to specify the
                # type of bike.
                match model:
                    case "Standard":
                        bike = Bike(size, colour, wheel_size, gear, brake, light)
                    case "Sport":
                        bike = SportBike(size, colour, wheel_size, light, drink_holder)
                    case "Tour":
                        bike = TourBike(
                            size, colour, handlebar_type, wheel_size, gear, brake, light, drink_holder, mudflaps
                        )
                    case _:
                        bike = CommuteBike(
                            size=size, colour=colour, handlebar_type=handlebar_type, wheel_size=wheel_size,
                            gear_type=gear, brake_type=brake, light_option=light, drink_holder=drink_holder,
                            mudflaps=mudflaps, front_rack=front_rack, rear_rack=rear_rack, child_seat=child_seat
                        )

                order = Order(bike, customer, order_date)

                production = Production(order)

            except Exception as x:
                QMessageBox.critical(self, "Error", str(x))
            # If successful
            QMessageBox.information(self, "Order Submitted", str(production))

            # Reset the Production model view
            window.check_production()

            # Change the production bin's frame type
            window.set_bike_frame(types_of_frames[size])

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

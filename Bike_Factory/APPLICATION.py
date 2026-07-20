import sys
from functools import partial

from PySide6.QtCharts import QChart, QChartView

from Bike_Class import *
from Customer_Class import *
from Production_Class import *
from Order_Class import Order

from PySide6.QtCore import Qt, QRegularExpression, QDate, QAbstractTableModel, QModelIndex, QRect, QEvent, QPointF, \
    QDateTime
from PySide6.QtGui import *
from PySide6.QtWidgets import (
    QApplication, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMenuBar, QPushButton, QVBoxLayout, QWidget, QComboBox,
    QMessageBox, QDateEdit, QTableView, QStyledItemDelegate, QAbstractItemView, QStyleOptionViewItem, QInputDialog,
    QGridLayout, QStyle, QStyleOptionButton
)
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assembly Line")
        self.resize(960, 750)
        self.order_entry = OrderEntryWindow()
        self.reports = ReportsWindow()

        # Create Widgets

        header_typography = QFont()
        header_typography.setBold(True)
        header_typography.setPointSize(12)
        sub_header_typography = QFont()
        sub_header_typography.setBold(True)
        sub_header_typography.setPointSize(9)

        btn_open_order_entry_window = QPushButton("Order Entry")
        btn_open_report_window = QPushButton("Reports")

        # - Assembly Line
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
        btn_handlebar_addition = QPushButton("Handlebar Addition")
        btn_drink_holder_addition = QPushButton("Drink Holder Addition")
        btn_front_rack_addition = QPushButton("Front Rack Addition")
        btn_rear_rack_addition = QPushButton("Rear Rack Addition")
        btn_mudflaps_addition = QPushButton("Mudflaps Addition")
        btn_child_seat_addition = QPushButton("Child Seat Addition")
        btn_pass = QPushButton("Pass")

        self.assembly_line_buttons = [
            btn_frame_assembly, btn_fork_assembly, btn_pass, btn_front_fork_assembly, btn_painted_parts,
            btn_pedal_addition, btn_wheel_addition, btn_gear_addition, btn_brake_addition, btn_light_addition,
            btn_seat_addition, btn_handlebar_addition, btn_drink_holder_addition, btn_front_rack_addition,
            btn_rear_rack_addition, btn_mudflaps_addition, btn_child_seat_addition
        ]

        self.internal_component_mapping: dict[QPushButton, str] = {
            btn_frame_assembly: "Frames", btn_fork_assembly: "Forks",
            btn_front_fork_assembly: "Front Fork", btn_painted_parts: "Painted Parts"
        }

        # -- Bike Status / Production Table
        self.lbl_production_bin_component_status = QLabel("")
        self.lbl_production_bin_component_status.setWordWrap(True)
        self.lbl_pass_btn_hint = QLabel(
            "Please press the Pass button when the production bin reaches an additional component that the "
            "bike(s) do not contain."
        )
        self.lbl_pass_btn_hint.setWordWrap(True)
        lbl_bike_status = QLabel("Bike Status / Production Bin")
        lbl_bike_status.setFont(sub_header_typography)
        self.lbl_production = QLabel("There are no bikes currently in production.")

        # - Inventory
        lbl_inventory = QLabel("Inventory")
        lbl_inventory.setFont(header_typography)
        btn_auto_restock = QPushButton("Auto Restock")
        lbl_restock_hint = QLabel(
            "To manually restock a specific component, please select their associated row from the table."
            " Once presented with a dialog box, enter a specified number to restock."
        )
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
        btn_open_order_entry_window.clicked.connect(lambda: self.toggle_window(self.order_entry))
        btn_open_report_window.clicked.connect(lambda: self.toggle_window(self.reports))
        self.table_view.clicked.connect(self.on_cell_click)     # specific cell that is clicked
        btn_auto_restock.clicked.connect(self.auto_restock)

        self.bike_frame = None  # assigned a value through the Order Entry Screen
        fork = Fork()
        front_fork = FrontFork()
        painted_part = PaintedPart()
        pedals = ExternalComponent("Pedals")
        wheel = ExternalComponent("Pairs of Wheels")
        gear = ExternalComponent("Gears")
        brake = ExternalComponent("Brakes")
        lights = ExternalComponent("Lights")
        seats = ExternalComponent("Seats")
        handlebar = ExternalComponent("Handlebar")
        drink_holder = ExternalComponent("Drink Holder")
        front_rack = ExternalComponent("Front Rack")
        rear_rack = ExternalComponent("Rear Rack")
        mudflaps = ExternalComponent("Mudflaps")
        child_seat = ExternalComponent("Child Seat")

        # Using a lambda function to stop the button from executing during setup (because the function contains an
        # argument rather than just the method name and so it tries to execute)
        btn_frame_assembly.clicked.connect(lambda: self.add_internal_component(self.bike_frame, -1))
        btn_fork_assembly.clicked.connect(lambda: self.add_internal_component(fork, -1))
        btn_front_fork_assembly.clicked.connect(lambda: self.add_internal_component(front_fork, 0))
        btn_painted_parts.clicked.connect(lambda: self.add_internal_component(painted_part, 1))
        btn_pedal_addition.clicked.connect(lambda: self.add_external_component(pedals, 2))
        btn_wheel_addition.clicked.connect(lambda: self.add_external_component(wheel, 3))
        btn_gear_addition.clicked.connect(lambda: self.add_external_component(gear, 4))
        btn_brake_addition.clicked.connect(lambda: self.add_external_component(brake, 5))
        btn_light_addition.clicked.connect(lambda: self.add_external_component(lights, 6))
        btn_seat_addition.clicked.connect(lambda: self.add_external_component(seats, 7))
        btn_handlebar_addition.clicked.connect(lambda: self.add_external_component(handlebar, 8))
        btn_drink_holder_addition.clicked.connect(lambda: self.add_external_component(drink_holder, 9))
        btn_front_rack_addition.clicked.connect(lambda: self.add_external_component(front_rack, 10))
        btn_rear_rack_addition.clicked.connect(lambda: self.add_external_component(rear_rack, 11))
        btn_mudflaps_addition.clicked.connect(lambda: self.add_external_component(mudflaps, 12))
        btn_child_seat_addition.clicked.connect(lambda: self.add_external_component(child_seat, 13))
        btn_pass.clicked.connect(self.advance_turn) # doesn't need a lambda as there are no arguments being passed

        # Adjust the colour of the button to indicate what work station is next (in green)
        self.current_turn_index = 0
        self.highlight_current_button()

        # Layout Setup

        # - Create Menubar at the top of the screen
        self.create_menubar()

        self.main_layout = QGridLayout()
        # - Assembly Line
        self.main_layout.addWidget(lbl_assembly_line, 0, 0)
        self.main_layout.addWidget(lbl_bike_status, 18, 0)   # change
        self.main_layout.addWidget(self.lbl_production, 19, 0)   # change
        self.main_layout.addWidget(self.lbl_production_bin_component_status, 6, 1)
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
        self.main_layout.addWidget(btn_handlebar_addition, 12, 0)
        self.main_layout.addWidget(btn_drink_holder_addition, 13, 0)
        self.main_layout.addWidget(btn_pass, 13, 1)
        self.main_layout.addWidget(self.lbl_pass_btn_hint, 11, 1)
        self.main_layout.addWidget(btn_front_rack_addition, 14, 0)
        self.main_layout.addWidget(btn_rear_rack_addition, 15, 0)
        self.main_layout.addWidget(btn_mudflaps_addition, 16, 0)
        self.main_layout.addWidget(btn_child_seat_addition, 17, 0)

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
        self.main_layout.addWidget(btn_open_report_window, 1, 11)
        self.main_layout_widget = QWidget()
        self.main_layout_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_layout_widget)

    def get_restock_list(self) -> list[str]:
        """A getter function that returns the list of components that need to be restocked. Either the stock has been
        completely depleted or there is a very small number of stock left.

        Returns:
            list[string]: Returns a list of strings, wherein each item is a component that needs to be restocked.
            """
        return self.restock_list

    def get_assembly_line_buttons_precedence(self) -> dict[int, QPushButton]:
        """A getter function that returns a dictionary of what buttons are capable of being highlighted and what order
        they should be. The key represents the index of the button, whereas the value is the button itself.

        Returns:
            dictionary[integer, QPushbutton]: A dictionary of the order of what buttons are to be highlighted.
            Key = index (the order); Value = button
            """
        # Make an order of precedence from the assemblyline buttons
        precedence: dict = {}
        index: int = 0

        # Remove the frame, fork and pass button
        copy = self.assembly_line_buttons[3:]

        for button in copy:
            precedence[index] = button

            index += 1

        return precedence

    def highlight_current_button(self) -> None:
        """A subroutine that calculates what button should be highlighted."""
        precedences = self.get_assembly_line_buttons_precedence()
        buttons = precedences.values()
        too_many_component: list = []
        internal_components = self.internal_component_mapping   # maps buttons to component string equivalent
        production_bin = inventory.get_production_bin()

        # Initially reset all buttons back to default. However, if they are an internally-produced component and their
        # stock is over 3, the button will be made red but still usable to indicate overstock/overproducing.
        for button in self.assembly_line_buttons:
            button.setStyleSheet("")
            button.setDisabled(False)

            if button in internal_components.keys():
                # If the stock is more than 3
                if production_bin[internal_components[button]] > 3:
                    too_many_component.append(self.internal_component_mapping[button])
                    button.setStyleSheet("background-color: red; color: white")

        # Additional information to the user to showcase internal components that are overstocked
        if len(too_many_component) > 0:
            self.lbl_production_bin_component_status.show()
            self.lbl_production_bin_component_status.setText(
                f"There are too many of the following components:"
                f" {str(too_many_component).replace("'", "").replace("[", "").replace("]", "")}."
                f" Please refrain from adding more until they have been used."
            )
        else:
            self.lbl_production_bin_component_status.hide()

        # Overwrite the button for the current turn
        current_button = precedences[self.current_turn_index]
        current_button.setStyleSheet("background-color: green; color: white")

        # Set buttons after the index to non-interactable (the bin isn't up to them yet)
        for precedence in precedences:
            if precedence > self.current_turn_index:
                precedences[precedence].setDisabled(True)

    def advance_turn(self) -> None:
        """A subroutine that changes what button is highlighted, indicating where the production bin is."""
        # Move to the next button; reset to 0 if at the end
        self.current_turn_index = (self.current_turn_index + 1) % len(self.get_assembly_line_buttons_precedence())
        self.highlight_current_button()

    def reset_turn(self) -> None:
        """A subroutine that resets the current index of the button to be highlighted to 0, which would be the Front
        Fork Assembly."""
        self.current_turn_index = 0

    def add_restock(self, component: str) -> None:
        """A subroutine that appends the component passed in (as an argument) to the list of items that need to be
         restocked."""
        self.restock_list.append(component)

    def remove_restock(self, component: str) -> None:
        """A subroutine that removes the component passed in (as an argument) from the list of items that need to be
         restocked."""
        self.restock_list.remove(component)

    def set_restock_message(self) -> None:
        """A subroutine that lists what components need to be restocked. If there are no items in this list, the label
        is hidden from the user."""
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
        """A subroutine that shows a pop-up menu whenever the user presses a particular row in the Inventory table.
        This pop-up menu allows the user to choose how much stock they wish to purchase for the corresponding
        component."""

        row = index.row()

        component: str = self.inventory_model.data(self.inventory_model.index(row, 0))

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

    def on_produce_bike_cell_click(self, index) -> None:
        """A subroutine that produces the bike of the corresponding row clicked if there are a sufficient number of
         components. This subroutine is executed when the user presses on the final cell in the production bin table.
         If there is not a sufficient number of components to satisfy the bike's requirements, a critical information
         pop-up is displayed to the user to inform them. Otherwise, a normal information pop-up is shown to inform the
         user the bike has been successfully produced."""
        row = index.row()
        column = index.column()
        produced_bike = False

        can_produce_bike_column: int = self.production_model.columnCount() - 1
        can_produce_bike_column_data: bool = self.production_model.data(self.production_model.index(row, column))

        if column == can_produce_bike_column:
            # If the column that checks whether the bike can be produced reads 'True'
            if can_produce_bike_column_data is True:
                self.produce_bike(index)
                produced_bike = True

        # The bike cannot be produced yet.
        if produced_bike is False:
            QMessageBox.critical(self, "Production Error",
                                 "There are not enough required components in the production bin to make this bike.")

    def produce_bike(self, index) -> None:
        """A subroutine that produces a bike of the corresponding row of the index passed as an argument."""
        order_id = index.siblingAtColumn(0).data()

        for bike in history.get_current_productions():
            if bike.get_order_id() == order_id:
                bike.produce_bike()
                QMessageBox.information(self, "Production Success",
                                        f"Bike Order ID {order_id} produced successfully.")
        # update the model
        self.update_models_views()

    def auto_restock(self) -> None:
        """A subroutine that shows an input dialog menu to the user, prompting them to enter a quantity of stock
        to auto-resupply each component by. This is in contrast to manually restocking each component by pressing on
        their respective row."""
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

    def toggle_window(self, window: QWidget) -> None:
        """A subroutine that toggles the visibility of the window passed as an argument. This can only be one of two
        options: the Order Entry or the Reports window."""
        if window.isVisible():
            window.hide()
        else:
            window.show()

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
        """A subroutine that changes the frame to be used in the production bin (certain frames, either size
         and/or bike, require a larger quantity of tabular steel to build)."""
        self.bike_frame = frame

    def add_external_component(self, external_component: ExternalComponent, index: int) -> None:
        """A subroutine that attempts to add an External Component to the production bin. This may return an error
        should there be an amount equal or less than zero is entered. This should not be possible anyway as the
        input dialog does not show an integer beneath 1.

        Following this, the index of the current highlighted button will be incremented, presuming the
        user has pressed the currently highlighted button. If the user does not press the currently highlighted button,
        the production bin will stay at the current workstation until it has been interacted with."""
        try:
            external_component.add()
        except ValueError as x:
            QMessageBox.critical(self, "Invalid", str(x))
            return
        QMessageBox.information(self, "Component Added", f"1 {external_component} has been added to the Production Bin.")

        # Update the model views
        self.update_models_views()
        self.highlight_current_button()

        # Advance the button index
        if self.current_turn_index == index:
            self.advance_turn()
        # else a prior workstation is producing more parts, which is how I have interpreted the requirement.

    def add_internal_component(self, component: Component, index: int) -> None:
        """A subroutine that attempts to add an External Component to the production bin. This may return an error
        should there be an amount equal or less than zero is entered or if there is not a sufficient number of input
        materials to make this component.

        Following this, the index of the current highlighted button will be incremented, presuming the
        user has pressed the currently highlighted button. If the user does not press the currently highlighted button,
        the production bin will stay at the current workstation until it has been interacted with."""
        try:
            component.create()
        except ValueError as x:
            QMessageBox.critical(self, "Invalid", str(x))
            return
        QMessageBox.information(self, "Component Added", f"1 {component} has been added to the Production Bin.")

        # Update the model views
        self.update_models_views()
        self.highlight_current_button()

        # Advance the button index
        if index >= 0:  # ignore the frame and forks
            if self.current_turn_index == index:
                self.advance_turn()

        # else a prior workstation is producing more parts, which is how I have interpreted the requirement.

    def hide_assembly_line(self) -> None:
        """A subroutine that hides the buttons and labels relating to the assembly line. This is used in conjunction
        with there being no bikes/orders currently being produced."""
        for button in self.assembly_line_buttons:
            button.hide()
        self.lbl_production_bin_component_status.hide()
        self.lbl_pass_btn_hint.hide()

    def show_assembly_line(self) -> None:
        """A subroutine that hides the buttons and labels relating to the assembly line. This is to indicate there
        are bike(s) in production."""
        for button in self.assembly_line_buttons:
            button.show()
            self.lbl_pass_btn_hint.hide()

    def check_production(self) -> None:
        """A subroutine that handles the models and views for the inventory and assembly line. This is used to either
        create or refresh these models, which includes hiding them should there be no active productions."""
        bikes_in_production = history.get_current_productions()
        print(len(bikes_in_production))
        if len(bikes_in_production) > 0:
            self.lbl_production.hide()
            self.show_assembly_line()

            components_needed: list[list] = []
            all_components = [component for component in inventory.get_components_list()]

            # Tubular steel is not included in the production bin (it is not directly added to the bike)
            all_components.remove("Tubular Steel")

            column_headers = ["Order ID"] + all_components + ["Can Produce Bike?"]
            production_bin: dict = inventory.get_production_bin()

            # Each row in the table
            for bike in bikes_in_production:
                # Initialise each cell in the row with None
                row = [None] * len(all_components)

                # Overwrite cells with components that are present
                for component in bike.get_components():
                    row[all_components.index(component)] = production_bin[component]

                # Components that are used to create other components or are created from existing components.
                indirect_components = ["Frames", "Forks", "Painted Parts"]

                # Add the indirect components to the row
                for component in indirect_components:
                    row[all_components.index(component)] = production_bin[component]

                components_needed.append([bike.get_order_id()] + row + [bike.can_produce_bike()])

            # If the production table view has not been initialised
            if self.production_table_view is None:
                self.production_table_view = QTableView(self)
                self.main_layout.addWidget(self.production_table_view, 19, 0, 8, 12)
                self.production_table_view.clicked.connect(self.on_produce_bike_cell_click)

                assemblyline_custom_delegate = AssemblyLineCustomDelegate(self)
                self.production_table_view.setItemDelegate(assemblyline_custom_delegate)

                font = QFont()
                font.setPointSize(8)
                self.production_table_view.setFont(font)
                self.production_table_view.resizeColumnsToContents()

            production_data = components_needed

            self.production_model = CustomTableModel(production_data, column_headers)
            self.production_table_view.setModel(self.production_model)
            self.production_table_view.show()

        else:
            self.lbl_production.show()
            self.hide_assembly_line()

            # Hide the table view if it exists
            if self.production_table_view is not None:
                self.production_table_view.hide()
                # Reset the turn as it makes more sense for the production bin to be back at the start.
                self.reset_turn()

    def update_models_views(self) -> None:
        """A subroutine that calls all the models and views in the application to be refreshed in order to showcase
         updated information/data."""
        self.check_production()
        self.inventory_model.update_data(
            [[component, stock] for component, stock in inventory.get_components_dict().items()]
        )
        # Update the models in the Reports screen to match these changes.
        self.reports.update_models()

    def closeEvent(self, event) -> None:
        """A subroutine that handles when the user presses the close button. When pressed, the user is prompted will a
        pop-up menu dialog to ensure they would like to quit. Should the user decide to quit, the entire application
        will close down - irrespective of other windows that are open."""
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
        """A subroutine that overwrites the paint method to change the colour of certain cells depending on their stock.
        Should a components stock fall below three (in other words, 0, 1 or 2) the cell will be turned red, presenting
        a visual cue to the reader."""
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
        """A subroutine that overwrites the paint method to change the colour of certain cells in a row depending on
         their quantity in the production bin or whether they are needed to create a component. Components that are
         not needed to create a bike in a certain row are painted black, whereas an insufficient number of a required
         component will be painted red. Components that match or surpass that required are painted green, which
         includes the cell that showcases whether the bike can be made (the last cell title 'Can Produce Bike?'
        Should a components stock fall below three (in other words, 0, 1 or 2) the cell will be turned red, presenting
        a visual cue to the reader."""
        stock = index.data(Qt.ItemDataRole.DisplayRole)

        ignore_indexes = [0, 4, 5]
        # ignore the OrderID column and other components that don't contribute directly to the bike
        if index.column() not in ignore_indexes:
            # Change the colour of the cell depending on the quantity of stock
            if stock is None:
                # Fill black, indicating that component is not used
                painter.fillRect(option.rect, QColor(0, 0, 0))
            elif stock == 0 or stock is False:
                # Fill red, indicating not enough stock
                painter.fillRect(option.rect, QColor(255, 0, 0))
            else:   # stock > 0 or stock is True
                # Fill green, indicating a valid quantity of stock.
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

        # Disable the components that the user cannot change.
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
        customer_layout.addWidget(lbl_town_city)
        customer_layout.addWidget(self.txt_town_city)
        customer_layout.addWidget(lbl_county)
        customer_layout.addWidget(self.txt_county)
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

        # Disable the components that the user cannot change for the standard bik, which is the bike that is initially
        # chosen.
        self.set_disabled()

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
        """A getter function that returns a list of all the combo boxes which may be disabled. For some certain types
        of bikes, certain options that appear in combo boxes are enforced as a standard. For instance, the standard bike
        enforces that a handlebar type of 'Flat' as standard - the user cannot change it.

        Returns:
             dictionary: A dictionary that returns a list of combo boxes which may be disabled.
             Key = combo box name; Value = combo box itself.
            """
        # A dictionary containing all the combo boxes that can be disabled.
        component_cbo_mapping = self.get_additional_component_mapping()
        component_cbo_mapping.update({
            "Handlebar Type": self.cbo_handlebar_type,
            "Gear Type": self.cbo_gear_type,
            "Brake Type": self.cbo_brake_type
        })

        return component_cbo_mapping

    def get_additional_component_mapping(self) -> dict:
        """A getter function that returns a dictionary of components that do not come with the standard bike. This
        includes a drink holder, front rack, rear rack, mudflaps and a child seat.

        Returns:
            dictionary: A dictionary of components. Key = component name; Value = combo box mapping.
            """
        additional_components = {
            "Drink Holder": self.cbo_drink_holder,
            "Front Rack": self.cbo_front_rack,
            "Rear Rack": self.cbo_rear_rack,
            "Mudflaps": self.cbo_mudflaps,
            "Child Seat": self.cbo_child_seat
        }
        return additional_components

    def set_all_interactable(self) -> None:
        """A subroutine that sets all combo boxes to be interactable. This is because some bikes have certain components
        enforced as a standard or do not include them entirely. This function reverses this change."""
        components = self.get_component_mapping()
        for component in components.values():
            component: QComboBox = component
            component.setDisabled(False)
            component.setCurrentIndex(0)

    def set_disabled(self) -> None:
        """A subroutine that sets all combo boxes to be disabled. This is because some bikes have certain components
        enforced as a standard or do not include them entirely. Either way, the user is not allowed to interact with
        them."""

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

    def complete_order(self) -> None:
        """A subroutine that submits the order when a valid bike and customer detail requirements are met. This may
        return an error should there be any nulls or if the user were to enter information in the wrong format, such
        as an invalid phone number, email or postcode. If an error occurs, the user will be shown a critical error
        message, displaying exactly what went wrong."""
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
                return
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
        """A getter function that returns if there are any null input fields, which will result in an error.

        Returns:
            boolean: A boolean value that indicates whether there are any null input fields.
        """
        return not (
                self.txt_name.text() and self.txt_phone_number.text() and self.txt_email_address.text() and
                self.txt_house_number.text() and self.txt_street_name.text() and self.txt_county.text() and
                self.txt_town_city.text() and self.txt_postcode.text())

    def clear(self) -> None:
        """A subroutine that clears all input fields apart from the date, allowing for a clean slate for the next order
        to be submitted."""
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


def get_customers() -> list[list]:
    """A getter function that returns a list of lists, wherein each inner list is a string-formatted version of a UNIQUE
    customer instance. In other words, this returns a list of customers and their information. This has been
     achieved through making a set of customers to remove duplicates - based on their contact information (their phone
      number AND email address). (The implementation of this can be found in the customer class.)"""
    # If the customer names and contact details match on separate customer orders, they are treat as the same person
    customer_list: list[Customer] = []
    for production in history.get_completed_productions():
        customer = production.get_customer()
        customer_list.append(customer)

    customer_set: set[Customer] = set(customer_list)   # remove duplicates
    customer_and_info = []
    for customer in customer_set:
        name = customer.get_name()
        contact_info = str(customer.get_contact_information()).replace("'", "").replace("[", "").replace("]", "")
        address = str(customer.get_delivery_address()).replace("'", "").replace("[", "").replace("]", "")
        row = [name, contact_info, address]
        customer_and_info.append(row)

    return customer_and_info


def get_production_history() -> list[list]:
    """A getter function that returns a list of lists, wherein each inner list is a string-formatted version of a
        production instance. In other words, this returns a list of productions and their information/details. """
    production_history: list[list] = []
    # Get the details about each production
    for completed_production in history.get_completed_productions():
        order_id: int = completed_production.get_order_id()
        bike_details: str = str(completed_production.get_bike_details()).replace("'", "").replace("[", "").replace("]", "")
        customer_name: str = completed_production.get_customer_name()
        customer_contact_info: str = str(completed_production.get_customer_contact_information()).replace("'", "").replace("[", "").replace("]", "")
        customer_delivery_info: str = str(completed_production.get_customer_address()).replace("'", "").replace("[", "").replace("]", "")
        date_ordered = completed_production.get_date_ordered()

        formatted_row = [
            order_id, bike_details, customer_name, customer_contact_info,
            customer_delivery_info, date_ordered
        ]
        production_history.append(formatted_row)
        print(f"Details: {formatted_row}")
    print(f"Production History: {production_history}")

    return production_history


def get_production_rates() -> dict[str, int]:
    """A getter function that returns the quantity of orders produced on a certain day.

    Returns:
        dictionary: A dictionary containing the number of orders produced on a certain day.
        Key = a day in the format 'dd/MM/yyyy'; Value = the number of orders produced on that day.
        """
    # Declare a set that will contain all the possible dates used, avoiding redundancy caused by duplicate dates
    all_dates = set()

    # Declare a dictionary that will map the number of item sold in a day to the corresponding day
    production_rates: dict[str, int] = {}
    production_history: list[Production] = history.get_completed_productions()

    if len(production_history) > 0:
        for production in history.get_completed_productions():
            production_date: str = production.get_date_ordered()
            if production_date not in all_dates:
                # Add the date to the set and dictionary
                all_dates.add(production_date)
                production_rates[production_date] = 0
            # Increment the count of orders for that day
            production_rates[production_date] += 1
    return production_rates


class ReportsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reports")
        self.resize(1440, 740)

        # Create Widgets
        header_typography = QFont()
        header_typography.setBold(True)
        header_typography.setPointSize(12)

        lbl_production_history = QLabel("Production History")
        self.lbl_production_history_no_status = QLabel(
            "There is currently no production history, and therefore no customer details or production"
            " details are displayed."
        )
        lbl_customer_details = QLabel("Customer Details")
        lbl_production_rates = QLabel("Production Rates")

        lbl_production_history.setFont(header_typography)
        lbl_customer_details.setFont(header_typography)
        lbl_production_rates.setFont(header_typography)

        # Initialise models
        self.production_table_view = None
        self.production_history_model = None

        self.customers_table_view = None
        self.customer_model = None

        self.production_rate_graph_view = None
        self.production_rate_model = None
        # Layout Setup

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(lbl_production_history, 0, 0)
        self.main_layout.addWidget(self.lbl_production_history_no_status, 1, 0)
        self.main_layout.addWidget(lbl_customer_details, 0, 1)
        # The Customer Details and Production Details tables will be added at 1, 0 and 1, 1 respectively
        self.main_layout.addWidget(lbl_production_rates, 2, 0)
        self.setLayout(self.main_layout)

    def update_models(self) -> None:
        """A subroutine to initialise or refresh the models of the Reports page. This includes the Customer Details,
        the list of completed Productions and the Production Rates over time."""

        # Check whether there is any history
        if len(history.get_completed_productions()) > 0:
            self.lbl_production_history_no_status.hide()

            production_column_headers = [
                "Order ID", "Bike Details", "Customer Name", "Customer Contact Info", "Customer Delivery Address",
                "Date Ordered"
            ]

            # Retrieve the data for the models
            history_data = get_production_history()
            customer_data = get_customers()
            production_rates = get_production_rates()
            print(production_rates.values())
            # If the table view has not been initialised
            if self.production_table_view is None:
                self.production_table_view = QTableView()
                self.customers_table_view = QTableView()

            # Completed Productions
            self.production_history_model = CustomTableModel(history_data, production_column_headers)
            self.production_table_view.setModel(self.production_history_model)
            self.production_table_view.show()

            # Customer Details
            customer_headers = ["Customer Name", "Contact Details", "Delivery Address"]
            self.customer_model = CustomTableModel(customer_data, customer_headers)
            self.customers_table_view.setModel(self.customer_model)
            self.customers_table_view.show()

            # Production Rates
            self.chart = QChart()
            self.series = QLineSeries()
            self.series.setName("Production Rates")

            # Fetch the data to be used for the model
            production_rate_model = get_production_rates()
            # As the data is in a set, sort by the date so I can the axis is displayed in a sequential order.
            sorted_by_date: list = sorted(production_rate_model.keys())
            sorted_data = [(date, production_rate_model[date]) for date in sorted_by_date]

            for index in range(len(sorted_data)):
                date = sorted_data[index][0]
                date_format = "dd/MM/yyyy"

                x_axis = QDateTime().fromString(date, date_format).toSecsSinceEpoch()
                y_axis = sorted_data[index][1]  # the count
                print(f"Date: {date}\nDate Format: {date_format}\nX Axis: {x_axis}\nY Axis: {y_axis}")
                self.series.append(x_axis * 1000, y_axis) # time needs to be in milliseconds to work

            self.chart.addSeries(self.series)

            # X-Axis
            self.x_axis = QDateTimeAxis()
            self.x_axis.setTickCount(len(sorted_data))
            self.x_axis.setFormat("dd/MM/yyyy")
            self.x_axis.setTitleText("Date")
            self.chart.addAxis(self.x_axis, Qt.AlignmentFlag.AlignBottom)
            self.series.attachAxis(self.x_axis)

            # Y-Axis
            self.y_axis = QValueAxis()
            self.y_axis.setTickCount(max(count for date, count in sorted_data))
            self.y_axis.setLabelFormat("%.0f") # sets the value of the y-axis to integers
            self.y_axis.setTitleText("Number of Orders")
            self.chart.addAxis(self.y_axis, Qt.AlignmentFlag.AlignLeft)
            self.series.attachAxis(self.y_axis)

            self.production_rate_graph_view = QChartView(self.chart)
            self.production_rate_graph_view.setRenderHint(QPainter.Antialiasing)
            self.production_rate_graph_view.setFixedSize(960, 300)

            # Changing the typography of the tables so they better fit on the screen.
            font = QFont()
            font.setPointSize(8)
            self.production_table_view.setFont(font)
            self.production_table_view.resizeColumnsToContents()
            self.customers_table_view.setFont(font)
            self.customers_table_view.resizeColumnsToContents()
            self.production_rate_graph_view.setFont(font)

            # Add Widgets
            self.main_layout.addWidget(self.production_table_view, 1, 0)
            self.main_layout.addWidget(self.customers_table_view, 1, 1)
            self.main_layout.addWidget(self.production_rate_graph_view, 2, 0, 8, 4)

        else:
            self.lbl_production_history_no_status.show()
            # Hide the table view if it exists
            if self.production_table_view is not None:
                self.production_table_view.hide()
                self.customers_table_view.hide()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

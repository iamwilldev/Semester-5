import sys
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('UTS PEMDES - 210411100218 MUHAMMAD MUQTAFIN NUHA')

        # Create a tab widget
        self.tab_widget = QTabWidget()

        # Create tabs
        self.input_tab = QWidget()
        self.display_tab = QWidget()

        # Add tabs to the tab widget
        self.tab_widget.addTab(self.input_tab, 'Input Data')
        self.tab_widget.addTab(self.display_tab, 'Display Data')

        # Set the central widget of the main window as the tab widget
        self.setCentralWidget(self.tab_widget)

        # Create a list to store data
        self.data = []

        # Populate the input_tab
        self.setup_input_tab()

        # Populate the display_tab
        self.setup_display_tab()

    def setup_input_tab(self):
        # Create widgets for input_tab
        self.name_label = QLabel('Nama:')
        self.name_edit = QLineEdit()
        self.nim_label = QLabel('NIM:')
        self.nim_edit = QLineEdit()
        self.address_label = QLabel('Alamat:')
        self.address_edit = QTextEdit()
        self.email_label = QLabel('Email:')
        self.email_edit = QLineEdit()
        self.birth_date_label = QLabel('Tanggal Lahir:')
        self.birth_date_edit = QDateEdit()
        self.height_label = QLabel('Tinggi Badan:')
        self.height_slider = QSlider(Qt.Orientation.Horizontal)
        self.hobby_label = QLabel('Hobi:')
        self.hobby_edit = QLineEdit()

        # Set the validator for the NIM field to accept only integers
        int_validator = QIntValidator()
        self.nim_edit.setValidator(int_validator)

        # Set the range for the height_slider
        self.height_slider.setMinimum(0)
        self.height_slider.setMaximum(300)

        # Create a "Submit" button
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.save_data)

        # Create a layout for input_tab
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.name_label)
        input_layout.addWidget(self.name_edit)
        input_layout.addWidget(self.nim_label)
        input_layout.addWidget(self.nim_edit)
        input_layout.addWidget(self.address_label)
        input_layout.addWidget(self.address_edit)
        input_layout.addWidget(self.email_label)
        input_layout.addWidget(self.email_edit)
        input_layout.addWidget(self.birth_date_label)
        input_layout.addWidget(self.birth_date_edit)
        input_layout.addWidget(self.height_label)
        input_layout.addWidget(self.height_slider)
        input_layout.addWidget(self.hobby_label)
        input_layout.addWidget(self.hobby_edit)
        input_layout.addWidget(self.submit_button)  # Add the Submit button

        input_widget = QWidget()
        input_widget.setLayout(input_layout)

        # Set input_widget as the layout for input_tab
        input_tab_layout = QVBoxLayout()
        input_tab_layout.addWidget(input_widget)
        self.input_tab.setLayout(input_tab_layout)

    def setup_display_tab(self):
        # Create widgets for display_tab
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)  # Number of columns for data fields
        self.table_widget.setHorizontalHeaderLabels(['Nama', 'NIM', 'Alamat', 'Email', 'Tanggal Lahir', 'Tinggi Badan', 'Hobi'])

        # Create a layout for display_tab
        display_layout = QVBoxLayout()
        display_layout.addWidget(self.table_widget)

        display_widget = QWidget()
        display_widget.setLayout(display_layout)

        # Set display_widget as the layout for display_tab
        display_tab_layout = QVBoxLayout()
        display_tab_layout.addWidget(display_widget)
        self.display_tab.setLayout(display_tab_layout)

    def save_data(self):
        # Get data from input fields
        name = self.name_edit.text()
        nim = self.nim_edit.text()
        address = self.address_edit.toPlainText()
        email = self.email_edit.text()
        birth_date = self.birth_date_edit.date().toString()
        height = self.height_slider.value()
        hobby = self.hobby_edit.text()

        # Create a dictionary to store the data
        student_data = {
            'Nama': name,
            'NIM': nim,
            'Alamat': address,
            'Email': email,
            'Tanggal Lahir': birth_date,
            'Tinggi Badan': height,
            'Hobi': hobby
        }

        # Append the data to the list
        self.data.append(student_data)

        # Clear the input fields after saving
        self.name_edit.clear()
        self.nim_edit.clear()
        self.address_edit.clear()
        self.email_edit.clear()
        self.birth_date_edit.setDate(QDate.currentDate())
        self.height_slider.setValue(0)
        self.hobby_edit.clear()

        # Optionally, you can print the data for testing
        print("Data Saved:", student_data)
        
        # Refresh the table to display the latest data
        self.populate_table()
    
    def populate_table(self):
        # Clear existing rows in the table
        self.table_widget.setRowCount(0)

        # Populate the table with saved data
        for student_data in self.data:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            for column_index, field in enumerate(['Nama', 'NIM', 'Alamat', 'Email', 'Tanggal Lahir', 'Tinggi Badan', 'Hobi']):
                item = QTableWidgetItem(student_data.get(field, ''))
                self.table_widget.setItem(row_position, column_index, item)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

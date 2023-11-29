from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableView, QTableWidgetItem, QAbstractItemView
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel
from PyQt6.QtCore import Qt, QDate, QDateTime

from mainwindow import *
from login import *
from adminwindow import *
from random import randint

import sys
import os
import sqlite3
import datetime

db_filename = 'TokoKelontong.db'

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        
        if os.path.isfile(db_filename):
            try:
                db = sqlite3.connect(db_filename)
                cursor = db.cursor()

                self.ui.label_2.setText("[+] Connected to Database")

            except sqlite3.Error as e:
                print("Error:", e)
                self.ui.label_2.setText("[!] Failed to connect to Database")

            finally:
                if db:
                    db.close()
        else:
            self.ui.label_2.setText("[!] Failed to connect - Database not found")
        self.ui.login.clicked.connect(self.login)
        self.show()

    def login(self):
        username = self.ui.username.text()
        password = self.ui.password.text()
        
        if username == "" or password == "":
            QMessageBox.critical(self, "Error", "Username atau password tidak boleh kosong!")
            
        else:
            db = sqlite3.connect(db_filename)
            cursor = db.cursor()
            
            cursor.execute("SELECT * FROM Pengguna WHERE username = ? AND password = ?", (username, password))
            
            # Fetch the first row
            user_data = cursor.fetchone()

            if user_data is not None:
                # admin dan petugas
                if user_data[5] == "Admin":
                    QMessageBox.information(self, "Info", "Selamat datang, " + user_data[5])
                    self.admin_window = AdminWindow()
                    self.admin_window.show()
                    self.hide()
                else:
                    QMessageBox.information(self, "Info", "Selamat datang, " + user_data[5])
                    self.petugas_window = PetugasWindow()
                    self.petugas_window.show()
                    self.hide()
                    
class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AdminWindow()  
        self.ui.setupUi(self)
        self.show()
        
        self.ui.role.addItem("Admin")
        self.ui.role.addItem("Petugas")
        
        db = sqlite3.connect(db_filename)
        cursor = db.cursor()
        
        # table_emp on QTableWidget
        cursor.execute("SELECT * FROM Pengguna")
        data_pengguna = cursor.fetchall()
        self.ui.table_emp.setRowCount(len(data_pengguna))
        self.ui.table_emp.setColumnCount(len(data_pengguna[0])-1)
        self.ui.table_emp.setHorizontalHeaderLabels(['Nama', 'Username', 'Password', 'Salary', 'Role'])
        self.ui.table_emp.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.table_emp.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.ui.table_emp.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.ui.table_emp.setAlternatingRowColors(True)
        self.ui.table_emp.verticalHeader().setVisible(False)
        self.ui.table_emp.horizontalHeader().setStretchLastSection(True)
        self.ui.table_emp.setSortingEnabled(True)
        self.ui.table_emp.setShowGrid(False)
        
        for i in range(len(data_pengguna)):
            for j in range(1, len(data_pengguna[0])):
                self.ui.table_emp.setItem(i, j-1, QTableWidgetItem(str(data_pengguna[i][j])))
                self.ui.table_emp.item(i, j-1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
        # table_barang on QTableWidget
        cursor.execute("SELECT b.nama, b.quantity, b.sell, b.purchase, b.expiry_date, s.nama AS Supplier FROM Barang b JOIN Supplier s ON b.id_supplier = s.id_supplier")
        data_barang = cursor.fetchall()
        self.ui.table_barang.setRowCount(len(data_barang))
        self.ui.table_barang.setColumnCount(len(data_barang[0]))
        self.ui.table_barang.setHorizontalHeaderLabels(['Nama', 'Qty', 'Harga Jual', 'Harga Beli', 'Exp Date', 'Supplier'])
        self.ui.table_barang.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.table_barang.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.ui.table_barang.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.ui.table_barang.setAlternatingRowColors(True)
        self.ui.table_barang.verticalHeader().setVisible(False)
        self.ui.table_barang.horizontalHeader().setStretchLastSection(True)
        self.ui.table_barang.setSortingEnabled(True)
        self.ui.table_barang.setShowGrid(False)
        
        for i in range(len(data_barang)):
            for j in range(len(data_barang[0])):
                self.ui.table_barang.setItem(i, j, QTableWidgetItem(str(data_barang[i][j])))
                self.ui.table_barang.item(i, j).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
        # table_supplier on QTableWidget
        cursor.execute("SELECT * FROM Supplier")
        data_supplier = cursor.fetchall()
        self.ui.table_supp.setRowCount(len(data_supplier))
        self.ui.table_supp.setColumnCount(len(data_supplier[0])-1)
        self.ui.table_supp.setHorizontalHeaderLabels(['Nama', 'No. Telp', 'Alamat'])
        self.ui.table_supp.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.table_supp.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.ui.table_supp.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.ui.table_supp.setAlternatingRowColors(True)
        self.ui.table_supp.verticalHeader().setVisible(False)
        self.ui.table_supp.horizontalHeader().setStretchLastSection(True)
        self.ui.table_supp.setSortingEnabled(True)
        self.ui.table_supp.setShowGrid(False)
    
        for i in range(len(data_supplier)):
            for j in range(1, len(data_supplier[0])):
                self.ui.table_supp.setItem(i, j-1, QTableWidgetItem(str(data_supplier[i][j])))
                self.ui.table_supp.item(i, j-1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # tampilkan data supplier ke ComboBox barang_supplier
            self.ui.barang_supplier.addItem(data_supplier[i][1], data_supplier[i][0])
        
        # table_cust on QTableWidget
        cursor.execute("SELECT * FROM Customer")
        data_customer = cursor.fetchall()
        self.ui.table_cust.setRowCount(len(data_customer))
        self.ui.table_cust.setColumnCount(len(data_customer[0])-1)
        self.ui.table_cust.setHorizontalHeaderLabels(['Nama', 'No. Telp', 'Alamat'])
        self.ui.table_cust.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.table_cust.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.ui.table_cust.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.ui.table_cust.setAlternatingRowColors(True)
        self.ui.table_cust.verticalHeader().setVisible(False)
        self.ui.table_cust.horizontalHeader().setStretchLastSection(True)
        self.ui.table_cust.setSortingEnabled(True)
        self.ui.table_cust.setShowGrid(False)
    
        for i in range(len(data_customer)):
            for j in range(1, len(data_customer[0])):
                self.ui.table_cust.setItem(i, j-1, QTableWidgetItem(str(data_customer[i][j])))
                self.ui.table_cust.item(i, j-1).setTextAlignment(Qt.AlignmentFlag.AlignCenter) 

        # Button Pengguna
        self.ui.emp_tambah.clicked.connect(self.emp_tambah)
        self.ui.emp_edit.clicked.connect(self.emp_edit)
        self.ui.emp_hapus.clicked.connect(self.emp_hapus)
        self.ui.emp_refresh.clicked.connect(self.emp_refresh)
        
        # Button Barang
        self.ui.barang_tambah.clicked.connect(self.barang_tambah)
        self.ui.barang_edit.clicked.connect(self.barang_edit)
        self.ui.barang_hapus.clicked.connect(self.barang_hapus)
        self.ui.barang_check.clicked.connect(self.barang_check)
        self.ui.barang_refresh.clicked.connect(self.barang_refresh)
        
        # Button Supplier
        self.ui.supp_tambah.clicked.connect(self.supp_tambah)
        self.ui.supp_edit.clicked.connect(self.supp_edit)
        self.ui.supp_hapus.clicked.connect(self.supp_hapus)
        self.ui.supp_refresh.clicked.connect(self.supp_refresh)
    
        # Button Customer
        self.ui.cust_tambah.clicked.connect(self.cust_tambah)
        self.ui.cust_edit.clicked.connect(self.cust_edit)
        self.ui.cust_hapus.clicked.connect(self.cust_hapus)
        self.ui.cust_refresh.clicked.connect(self.cust_refresh)
        
        
            
    # Pengguna
    def emp_tambah(self):
        if self.ui.emp_tambah.text() == "Tambah":
            db = sqlite3.connect(db_filename)
            cursor = db.cursor()
            
            nama = self.ui.emp_nama.text()
            username = self.ui.emp_username.text()
            password = self.ui.emp_password.text()
            salary = self.ui.emp_salary.text()
            is_admin = self.ui.role.currentText()
            
            if nama == "" or username == "" or password == "" or salary == "":
                QMessageBox.critical(self, "Error", "Data tidak boleh kosong!")
            else:
                try:
                    salary = int(salary)
                    cursor.execute("INSERT INTO Pengguna (nama, username, password, salary, is_admin) VALUES (?, ?, ?, ?, ?)", (nama, username, password, salary, is_admin))
                    db.commit()
                    QMessageBox.information(self, "Info", "Data berhasil ditambahkan!")
                except ValueError as ve:
                    print("Value error:", ve)
                    QMessageBox.critical(self, "Error", "Invalid value error. Data gagal ditambahkan!")
                finally:
                    if db:
                        db.close()
                    # kosongkan line edit
                    self.ui.emp_nama.setText("")
                    self.ui.emp_username.setText("")
                    self.ui.emp_password.setText("")
                    self.ui.emp_salary.setText("")
                    self.ui.role.setCurrentIndex(0)
                    # refresh table
                    self.emp_refresh()
                    
        elif self.ui.emp_tambah.text() == "Edit":
            db = sqlite3.connect(db_filename)
            cursor = db.cursor()
            
            nama = self.ui.emp_nama.text()
            self.ui.emp_username.setReadOnly(True)
            username = self.ui.emp_username.text()
            password = self.ui.emp_password.text()
            salary = self.ui.emp_salary.text()
            is_admin = self.ui.role.currentText()
            
            if nama == "" or username == "" or password == "" or salary == "":
                QMessageBox.critical(self, "Error", "Data tidak boleh kosong!")
            else:
                try:
                    salary = int(salary)
                    cursor.execute("UPDATE Pengguna SET nama = ?, password = ?, salary = ?, is_admin = ? WHERE username = ?", (nama, password, salary, is_admin, username))
                    db.commit()
                    QMessageBox.information(self, "Info", "Data berhasil diubah!")
                except ValueError as ve:
                    print("Value error:", ve)
                    QMessageBox.critical(self, "Error", "Invalid value error. Data gagal diubah!")
                finally:
                    if db:
                        db.close()
                    # kosongkan line edit
                    self.ui.emp_nama.setText("")
                    self.ui.emp_username.setText("")
                    self.ui.emp_password.setText("")
                    self.ui.emp_salary.setText("")
                    self.ui.role.setCurrentIndex(0)
                    self.ui.emp_tambah.setText("Tambah")
                    self.ui.emp_edit.setText("Edit")
                    # refresh table
                    self.emp_refresh()

    def emp_edit(self):
        if self.ui.emp_edit.text() == "Edit":
            # ambil dari current index table widget table_emp
            row = self.ui.table_emp.currentRow()
            nama = self.ui.table_emp.item(row, 0).text()
            username = self.ui.table_emp.item(row, 1).text()
            password = self.ui.table_emp.item(row, 2).text()
            salary = self.ui.table_emp.item(row, 3).text()
            is_admin = self.ui.table_emp.item(row, 4).text()
            
            self.ui.emp_nama.setText(nama)
            self.ui.emp_username.setReadOnly(True)
            self.ui.emp_username.setText(username)
            self.ui.emp_password.setText(password)
            self.ui.emp_salary.setText(salary)
            self.ui.role.setCurrentText(is_admin)
            
            self.ui.emp_tambah.setText("Edit")
            self.ui.emp_edit.setText("Cancel")
            
        elif self.ui.emp_edit.text() == "Cancel":
            self.ui.emp_nama.setText("")
            self.ui.emp_username.setReadOnly(False)
            self.ui.emp_username.setText("")
            self.ui.emp_password.setText("")
            self.ui.emp_salary.setText("")
            self.ui.role.setCurrentIndex(0)
            
            self.ui.emp_edit.setText("Edit")
            self.ui.emp_tambah.setText("Tambah")
            
    def emp_hapus(self):
        db = sqlite3.connect(db_filename)
        cursor = db.cursor()
        
        # ambil dari current index table widget table_emp
        row = self.ui.table_emp.currentRow()
        username = self.ui.table_emp.item(row, 1).text()
        # hapus data
        try:
            cursor.execute("DELETE FROM Pengguna WHERE username = ?", (username,))
            db.commit()
            QMessageBox.information(self, "Info", "Data berhasil dihapus!")
        except sqlite3.Error as e:
            print("Error:", e)
            QMessageBox.critical(self, "Error", "Data gagal dihapus!")
        finally:
            if db:
                db.close()
            # refresh table
            self.emp_refresh()
                
    def emp_refresh(self):
        if self.ui.emp_refresh.text() == "Refresh":
            db = sqlite3.connect(db_filename)
            cursor = db.cursor()
            
            # table_emp on QTableWidget
            cursor.execute("SELECT * FROM Pengguna")
            data_pengguna = cursor.fetchall()
            self.ui.table_emp.setRowCount(len(data_pengguna))
            self.ui.table_emp.setColumnCount(len(data_pengguna[0])-1)
            self.ui.table_emp.setHorizontalHeaderLabels(['Nama', 'Username', 'Password', 'Salary', 'Role'])
            self.ui.table_emp.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.ui.table_emp.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
            self.ui.table_emp.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            self.ui.table_emp.setAlternatingRowColors(True)
            self.ui.table_emp.verticalHeader().setVisible(False)
            self.ui.table_emp.horizontalHeader().setStretchLastSection(True)
            self.ui.table_emp.setSortingEnabled(True)
            self.ui.table_emp.setShowGrid(False)
            
            for i in range(len(data_pengguna)):
                for j in range(1, len(data_pengguna[0])):
                    self.ui.table_emp.setItem(i, j-1, QTableWidgetItem(str(data_pengguna[i][j])))
                    self.ui.table_emp.item(i, j-1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.ui.emp_username.setReadOnly(False)

        elif self.ui.emp_refresh.text() == "Cancel":
            self.ui.emp_nama.setText("")
            self.ui.emp_username.setReadOnly(False)
            self.ui.emp_username.setText("")
            self.ui.emp_password.setText("")
            self.ui.emp_salary.setText("")
            self.ui.role.setCurrentIndex(0)

            self.ui.emp_refresh.setText("Refresh")
            self.ui.emp_tambah.setText("Tambah")

            self.emp_refresh()
    
    # Barang
    def barang_tambah(self):
        if self.ui.barang_tambah.text() == "Tambah":
            db = sqlite3.connect(db_filename)
            cursor = db.cursor()
            
            nama = self.ui.barang_nama.text()
            qty = self.ui.barang_quantity.text()
            sell = self.ui.barang_sellprice.text()
            purchase = self.ui.barang_buyprice.text()
            expiry_date = self.ui.barang_expired.date()
            expiry = expiry_date.toPyDate().strftime("%Y-%m-%d")
            supplier = self.ui.barang_supplier.currentData()
            
            if nama == "" or qty == "" or sell == "" or purchase == "" or expiry == "":
                QMessageBox.critical(self, "Error", "Data tidak boleh kosong!")
            else:
                try:
                    qty = int(qty)
                    sell = int(sell)
                    purchase = int(purchase)
                    cursor.execute("INSERT INTO Barang (nama, quantity, sell, purchase, expiry_date, id_supplier) VALUES (?, ?, ?, ?, ?, ?)", (nama, qty, sell, purchase, expiry, supplier))
                    db.commit()
                    QMessageBox.information(self, "Info", "Data berhasil ditambahkan!")
                except ValueError as ve:
                    print("Value error:", ve)
                    QMessageBox.critical(self, "Error", "Invalid value error. Data gagal ditambahkan!")
                finally:
                    if db:
                        db.close()
                    # kosongkan line edit
                    self.ui.barang_nama.setText("")
                    self.ui.barang_quantity.setText("")
                    self.ui.barang_sellprice.setText("")
                    self.ui.barang_buyprice.setText("")
                    self.ui.barang_expired.setDate(QDate())
                    self.ui.barang_supplier.setCurrentIndex(0)
                    # refresh table
                    self.barang_refresh()
                
        elif self.ui.barang_tambah.text() == "Edit":
            db = sqlite3.connect(db_filename)
            cursor = db.cursor()
            
            nama = self.ui.barang_nama.text()
            qty = self.ui.barang_quantity.text()
            sell = self.ui.barang_sellprice.text()
            purchase = self.ui.barang_buyprice.text()
            expiry_date = self.ui.barang_expired.date()
            expiry = expiry_date.toPyDate().strftime("%Y-%m-%d")
            supplier = self.ui.barang_supplier.currentData()
            
            if nama == "" or qty == "" or sell == "" or purchase == "" or expiry == "":
                QMessageBox.critical(self, "Error", "Data tidak boleh kosong!")
            else:
                try:
                    qty = int(qty)
                    sell = int(sell)
                    purchase = int(purchase)
                    cursor.execute("UPDATE Barang SET nama = ?, quantity = ?, sell = ?, purchase = ?, expiry_date = ?, id_supplier = ? WHERE nama = ?", (nama, qty, sell, purchase, expiry, supplier, nama))
                    db.commit()
                    QMessageBox.information(self, "Info", "Data berhasil diubah!")
                except ValueError as ve:
                    print("Value error:", ve)
                    QMessageBox.critical(self, "Error", "Invalid value error. Data gagal diubah!")
                finally:
                    if db:
                        db.close()
                    # kosongkan line edit
                    self.ui.barang_nama.setText("")
                    self.ui.barang_quantity.setText("")
                    self.ui.barang_sellprice.setText("")
                    self.ui.barang_buyprice.setText("")
                    self.ui.barang_expired.setDate(QDate())
                    self.ui.barang_supplier.setCurrentIndex(0)
                    self.ui.barang_tambah.setText("Tambah")
                    self.ui.barang_edit.setText("Edit")
                    # refresh table
                    self.barang_refresh()
    
    def barang_edit(self):
        if self.ui.barang_edit.text() == "Edit":
            # ambil dari current index table widget table_barang
            row = self.ui.table_barang.currentRow()
            nama = self.ui.table_barang.item(row, 0).text()
            qty = self.ui.table_barang.item(row, 1).text()
            sell = self.ui.table_barang.item(row, 2).text()
            purchase = self.ui.table_barang.item(row, 3).text()
            expiry = self.ui.table_barang.item(row, 4).text()
            supplier = self.ui.table_barang.item(row, 5).text()
            # isi line edit
            self.ui.barang_nama.setReadOnly(True)
            self.ui.barang_nama.setText(nama)
            self.ui.barang_quantity.setText(qty)
            self.ui.barang_sellprice.setText(sell)
            self.ui.barang_buyprice.setText(purchase)
            self.ui.barang_expired.setDate(QDate.fromString(expiry, "yyyy-MM-dd"))
            self.ui.barang_supplier.setCurrentText(supplier)
            # ubah button text menjadi Edit dan disable tombol tambah
            self.ui.barang_tambah.setText("Edit")
            self.ui.barang_edit.setText("Cancel")
            
        elif self.ui.barang_edit.text() == "Cancel":
            self.ui.barang_nama.setText("")
            self.ui.barang_quantity.setText("")
            self.ui.barang_sellprice.setText("")
            self.ui.barang_buyprice.setText("")
            self.ui.barang_expired.setDate(QDate())
            self.ui.barang_supplier.setCurrentIndex(0)

            self.ui.barang_edit.setText("Edit")
            self.ui.barang_tambah.setText("Tambah")
                    
    def barang_hapus(self):
        db = sqlite3.connect(db_filename)
        cursor = db.cursor()
        
        # ambil dari current index table widget table_barang
        row = self.ui.table_barang.currentRow()
        nama = self.ui.table_barang.item(row, 0).text()
        
        # hapus data
        try:
            cursor.execute("DELETE FROM Barang WHERE nama = ?", (nama,))
            db.commit()
            QMessageBox.information(self, "Info", "Data berhasil dihapus!")
        except sqlite3.Error as e:
            print("Error:", e)
            QMessageBox.critical(self, "Error", "Data gagal dihapus!")
        finally:
            if db:
                db.close()
            # refresh table
            self.barang_refresh()
    
    def barang_check(self):
        db = sqlite3.connect(db_filename)
        cursor = db.cursor()

        # Retrieve selected product details based on user input
        nama_barang = self.ui.barang_inputcheck.text()

        try:
            # Query to retrieve details from the database
            cursor.execute("SELECT b.nama, b.quantity, b.sell, b.purchase, b.expiry_date, s.nama AS Supplier FROM Barang b JOIN Supplier s ON b.id_supplier = s.id_supplier WHERE b.nama = ?", (nama_barang,))
            product_details = cursor.fetchone()

            if product_details:
                # Display details in a pop-up or dialog window
                details_text = f"Nama: {product_details[0]}\nQuantity: {product_details[1]}\nHarga Jual: {product_details[2]}\nHarga Beli: {product_details[3]}\nExp Date: {product_details[4]}\nSupplier: {product_details[5]}"

                QMessageBox.information(self, "Product Details", details_text)
            else:
                QMessageBox.warning(self, "Warning", "Product not found!")

        except sqlite3.Error as e:
            print("SQLite error:", e)
            QMessageBox.critical(self, "Error", f"SQLite error: {e}. Unable to retrieve product details!")

        finally:
            if db:
                db.close()
            
            
    def barang_refresh(self):
        if self.ui.barang_refresh.text() == "Refresh":
            db = sqlite3.connect(db_filename)
            cursor = db.cursor()
            
            # table_barang on QTableWidget
            cursor.execute("SELECT b.nama, b.quantity, b.sell, b.purchase, b.expiry_date, s.nama AS Supplier FROM Barang b JOIN Supplier s ON b.id_supplier = s.id_supplier")
            data_barang = cursor.fetchall()
            self.ui.table_barang.setRowCount(len(data_barang))
            self.ui.table_barang.setColumnCount(len(data_barang[0]))
            self.ui.table_barang.setHorizontalHeaderLabels(['Nama', 'Qty', 'Harga Jual', 'Harga Beli', 'Exp Date', 'Supplier'])
            self.ui.table_barang.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.ui.table_barang.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
            self.ui.table_barang.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            self.ui.table_barang.setAlternatingRowColors(True)
            self.ui.table_barang.verticalHeader().setVisible(False)
            self.ui.table_barang.horizontalHeader().setStretchLastSection(True)
            self.ui.table_barang.setSortingEnabled(True)
            self.ui.table_barang.setShowGrid(False)
            
            for i in range(len(data_barang)):
                for j in range(len(data_barang[0])):
                    self.ui.table_barang.setItem(i, j, QTableWidgetItem(str(data_barang[i][j])))
                    self.ui.table_barang.item(i, j).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    
            self.ui.barang_nama.setReadOnly(False)

        elif self.ui.barang_refresh.text() == "Cancel":
            self.ui.barang_nama.setText("")
            self.ui.barang_qty.setText("")
            self.ui.barang_sell.setText("")
            self.ui.barang_purchase.setText("")
            self.ui.barang_expired.setDate(QDate())
            self.ui.barang_supplier.setCurrentIndex(0)

            self.ui.barang_refresh.setText("Refresh")
            self.ui.barang_tambah.setText("Tambah")

            self.barang_refresh()
    
    # Supplier
    def supp_tambah(self):
        if self.ui.supp_tambah.text() == "Tambah":
            db = sqlite3.connect(db_filename)
            cursor = db.cursor()
            
            nama = self.ui.supp_nama.text()
            contact = self.ui.supp_contact.text()
            alamat = self.ui.supp_alamat.text()
            
            if nama == "" or contact == "" or alamat == "":
                QMessageBox.critical(self, "Error", "Data tidak boleh kosong!")
            else:
                try:
                    cursor.execute("INSERT INTO Supplier (nama, contact, alamat) VALUES (?, ?, ?)", (nama, contact, alamat))
                    db.commit()
                    QMessageBox.information(self, "Info", "Data berhasil ditambahkan!")
                except sqlite3.Error as e:
                    print("Error:", e)
                    QMessageBox.critical(self, "Error", "Data gagal ditambahkan!")
                finally:
                    if db:
                        db.close()
                    # kosongkan line edit
                    self.ui.supp_nama.setText("")
                    self.ui.supp_contact.setText("")
                    self.ui.supp_alamat.setText("")
                    # refresh table
                    self.supp_refresh()
                
        elif self.ui.supp_tambah.text() == "Edit":
            db = sqlite3.connect(db_filename)
            cursor = db.cursor()
            
            nama = self.ui.supp_nama.text()
            contact = self.ui.supp_contact.text()
            alamat = self.ui.supp_alamat.text()
            
            if nama == "" or contact == "" or alamat == "":
                QMessageBox.critical(self, "Error", "Data tidak boleh kosong!")
            else:
                try:
                    cursor.execute("UPDATE Supplier SET nama = ?, contact = ?, alamat = ? WHERE nama = ?", (nama, contact, alamat, nama))
                    db.commit()
                    QMessageBox.information(self, "Info", "Data berhasil diubah!")
                except sqlite3.Error as e:
                    print("Error:", e)
                    QMessageBox.critical(self, "Error", "Data gagal diubah!")
                finally:
                    if db:
                        db.close()
                    # kosongkan line edit
                    self.ui.supp_nama.setText("")
                    self.ui.supp_contact.setText("")
                    self.ui.supp_alamat.setText("")
                    self.ui.supp_tambah.setText("Tambah")
                    self.ui.supp_edit.setText("Edit")
                    # refresh table
                    self.supp_refresh()
    
    def supp_edit(self):
        if self.ui.supp_edit.text() == "Edit":
            # ambil dari current index table widget table_supp
            row = self.ui.table_supp.currentRow()
            nama = self.ui.table_supp.item(row, 0).text()
            contact = self.ui.table_supp.item(row, 1).text()
            alamat = self.ui.table_supp.item(row, 2).text()
            
            self.ui.supp_nama.setReadOnly(True)
            self.ui.supp_nama.setText(nama)
            self.ui.supp_contact.setText(contact)
            self.ui.supp_alamat.setText(alamat)
            
            self.ui.supp_tambah.setText("Edit")
            self.ui.supp_edit.setText("Cancel")
            
        elif self.ui.supp_edit.text() == "Cancel":
            self.ui.supp_nama.setText("")
            self.ui.supp_contact.setText("")
            self.ui.supp_alamat.setText("")
            
            self.ui.supp_edit.setText("Edit")
            self.ui.supp_tambah.setText("Tambah")
    
    def supp_hapus(self):
        db = sqlite3.connect(db_filename)
        cursor = db.cursor()
        
        # ambil dari current index table widget table_supp
        row = self.ui.table_supp.currentRow()
        nama = self.ui.table_supp.item(row, 0).text()
        
        # hapus data
        try:
            cursor.execute("DELETE FROM Supplier WHERE nama = ?", (nama,))
            db.commit()
            QMessageBox.information(self, "Info", "Data berhasil dihapus!")
        except sqlite3.Error as e:
            print("Error:", e)
            QMessageBox.critical(self, "Error", "Data gagal dihapus!")
        finally:
            if db:
                db.close()
            # refresh table
            self.supp_refresh()
    
    def supp_refresh(self):
        if self.ui.supp_refresh.text() == "Refresh":
            db = sqlite3.connect(db_filename)
            cursor = db.cursor()
            
            # table_supp on QTableWidget
            cursor.execute("SELECT * FROM Supplier")
            data_supplier = cursor.fetchall()
            self.ui.table_supp.setRowCount(len(data_supplier))
            self.ui.table_supp.setColumnCount(len(data_supplier[0])-1)
            self.ui.table_supp.setHorizontalHeaderLabels(['Nama', 'No. Telp', 'Alamat'])
            self.ui.table_supp.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.ui.table_supp.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
            self.ui.table_supp.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            self.ui.table_supp.setAlternatingRowColors(True)
            self.ui.table_supp.verticalHeader().setVisible(False)
            self.ui.table_supp.horizontalHeader().setStretchLastSection(True)
            self.ui.table_supp.setSortingEnabled(True)
            self.ui.table_supp.setShowGrid(False)
            
            for i in range(len(data_supplier)):
                for j in range(1, len(data_supplier[0])):
                    self.ui.table_supp.setItem(i, j-1, QTableWidgetItem(str(data_supplier[i][j])))
                    self.ui.table_supp.item(i, j-1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.ui.supp_nama.setReadOnly(False)

        elif self.ui.supp_refresh.text() == "Cancel":
            self.ui.supp_nama.setText("")
            self.ui.supp_contact.setText("")
            self.ui.supp_alamat.setText("")

            self.ui.supp_refresh.setText("Refresh")
            self.ui.supp_tambah.setText("Tambah")

            self.supp_refresh()
            
    # Customer
    def cust_tambah(self):
        if self.ui.cust_tambah.text() == "Tambah":
            db = sqlite3.connect(db_filename)
            cursor = db.cursor()
            
            nama = self.ui.cust_nama.text()
            contact = self.ui.cust_contact.text()
            alamat = self.ui.cust_alamat.text()
            
            if nama == "" or contact == "" or alamat == "":
                QMessageBox.critical(self, "Error", "Data tidak boleh kosong!")
            else:
                try:
                    cursor.execute("INSERT INTO Customer (nama, contact, alamat) VALUES (?, ?, ?)", (nama, contact, alamat))
                    db.commit()
                    QMessageBox.information(self, "Info", "Data berhasil ditambahkan!")
                except sqlite3.Error as e:
                    print("Error:", e)
                    QMessageBox.critical(self, "Error", "Data gagal ditambahkan!")
                finally:
                    if db:
                        db.close()
                    # kosongkan line edit
                    self.ui.cust_nama.setText("")
                    self.ui.cust_contact.setText("")
                    self.ui.cust_alamat.setText("")
                    # refresh table
                    self.cust_refresh()
                
        elif self.ui.cust_tambah.text() == "Edit":
            db = sqlite3.connect(db_filename)
            cursor = db.cursor()
            
            nama = self.ui.cust_nama.text()
            contact = self.ui.cust_contact.text()
            alamat = self.ui.cust_alamat.text()
            
            if nama == "" or contact == "" or alamat == "":
                QMessageBox.critical(self, "Error", "Data tidak boleh kosong!")
            else:
                try:
                    cursor.execute("UPDATE Customer SET nama = ?, contact = ?, alamat = ? WHERE nama = ?", (nama, contact, alamat, nama))
                    db.commit()
                    QMessageBox.information(self, "Info", "Data berhasil diubah!")
                except sqlite3.Error as e:
                    print("Error:", e)
                    QMessageBox.critical(self, "Error", "Data gagal diubah!")
                finally:
                    if db:
                        db.close()
                    # kosongkan line edit
                    self.ui.cust_nama.setText("")
                    self.ui.cust_contact.setText("")
                    self.ui.cust_alamat.setText("")
                    self.ui.cust_tambah.setText("Tambah")
                    self.ui.cust_edit.setText("Edit")
                    # refresh table
                    self.cust_refresh()
            
    def cust_edit(self):
        if self.ui.cust_edit.text() == "Edit":
            # ambil dari current index table widget table_cust
            row = self.ui.table_cust.currentRow()
            nama = self.ui.table_cust.item(row, 0).text()
            contact = self.ui.table_cust.item(row, 1).text()
            alamat = self.ui.table_cust.item(row, 2).text()
            
            self.ui.cust_nama.setReadOnly(True)
            self.ui.cust_nama.setText(nama)
            self.ui.cust_contact.setText(contact)
            self.ui.cust_alamat.setText(alamat)
            
            self.ui.cust_tambah.setText("Edit")
            self.ui.cust_edit.setText("Cancel")
            
        elif self.ui.cust_edit.text() == "Cancel":
            self.ui.cust_nama.setText("")
            self.ui.cust_contact.setText("")
            self.ui.cust_alamat.setText("")
            
            self.ui.cust_edit.setText("Edit")
            self.ui.cust_tambah.setText("Tambah")
    
    def cust_hapus(self):
        db = sqlite3.connect(db_filename)
        cursor = db.cursor()
        
        # ambil dari current index table widget table_cust
        row = self.ui.table_cust.currentRow()
        nama = self.ui.table_cust.item(row, 0).text()
        
        # hapus data
        try:
            cursor.execute("DELETE FROM Customer WHERE nama = ?", (nama,))
            db.commit()
            QMessageBox.information(self, "Info", "Data berhasil dihapus!")
        except sqlite3.Error as e:
            print("Error:", e)
            QMessageBox.critical(self, "Error", "Data gagal dihapus!")
        finally:
            if db:
                db.close()
            # refresh table
            self.cust_refresh()
        
    def cust_refresh(self):
        if self.ui.cust_refresh.text() == "Refresh":
            db = sqlite3.connect(db_filename)
            cursor = db.cursor()
            
            # table_cust on QTableWidget
            cursor.execute("SELECT * FROM Customer")
            data_customer = cursor.fetchall()
            self.ui.table_cust.setRowCount(len(data_customer))
            self.ui.table_cust.setColumnCount(len(data_customer[0])-1)
            self.ui.table_cust.setHorizontalHeaderLabels(['Nama', 'No. Telp', 'Alamat'])
            self.ui.table_cust.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.ui.table_cust.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
            self.ui.table_cust.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            self.ui.table_cust.setAlternatingRowColors(True)
            self.ui.table_cust.verticalHeader().setVisible(False)
            self.ui.table_cust.horizontalHeader().setStretchLastSection(True)
            self.ui.table_cust.setSortingEnabled(True)
            self.ui.table_cust.setShowGrid(False)
            
            for i in range(len(data_customer)):
                for j in range(1, len(data_customer[0])):
                    self.ui.table_cust.setItem(i, j-1, QTableWidgetItem(str(data_customer[i][j])))
                    self.ui.table_cust.item(i, j-1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.ui.cust_nama.setReadOnly(False)

        elif self.ui.cust_refresh.text() == "Cancel":
            self.ui.cust_nama.setText("")
            self.ui.cust_contact.setText("")
            self.ui.cust_alamat.setText("")

            self.ui.cust_refresh.setText("Refresh")
            self.ui.cust_tambah.setText("Tambah")

            self.cust_refresh()
            
class PetugasWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PetugasWindow()  
        self.ui.setupUi(self)
        self.show()
        
        self.cart = []
        
        db = sqlite3.connect(db_filename)
        cursor = db.cursor()
        
        cursor.execute("SELECT * FROM Supplier")
        data_supplier = cursor.fetchall()
    
        for i in range(len(data_supplier)):
            self.ui.barang_supplier.addItem(data_supplier[i][1], data_supplier[i][0])
        
        cursor.execute("SELECT * FROM Customer")
        data_customer = cursor.fetchall()
        for i in range(len(data_customer)):
            self.ui.barang_customer.addItem(data_customer[i][1], data_customer[i][0])
        
        # table_barang on QTableWidget
        cursor.execute("SELECT nama FROM Barang")
        data_barang = cursor.fetchall()
        self.ui.table_barang.setRowCount(len(data_barang))
        self.ui.table_barang.setColumnCount(len(data_barang[0]))
        self.ui.table_barang.setHorizontalHeaderLabels(['Nama'])
        self.ui.table_barang.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.table_barang.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.ui.table_barang.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.ui.table_barang.setAlternatingRowColors(True)
        self.ui.table_barang.verticalHeader().setVisible(False)
        self.ui.table_barang.horizontalHeader().setStretchLastSection(True)
        self.ui.table_barang.setSortingEnabled(True)
        self.ui.table_barang.setShowGrid(False)
        
        for i in range(len(data_barang)):
            for j in range(len(data_barang[0])):
                self.ui.table_barang.setItem(i, j, QTableWidgetItem(str(data_barang[i][j])))
                self.ui.table_barang.item(i, j).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.ui.barang_nama.setReadOnly(True)
        self.ui.barang_harga.setReadOnly(True)
        self.ui.barang_stok.setReadOnly(True)
        self.ui.barang_expired.setReadOnly(True)
        self.ui.barang_supplier.setDisabled(True)
        
        # Button Barang
        self.ui.barang_preview.clicked.connect(self.barang_preview)
        self.ui.barang_refresh.clicked.connect(self.barang_refresh)
        self.ui.barang_viewCart.clicked.connect(self.barang_viewCart)
        self.ui.barang_back.clicked.connect(self.barang_back)
        self.ui.barang_addCart.clicked.connect(self.barang_addCart)
        self.ui.barang_sum.clicked.connect(self.barang_sum)
        self.ui.barang_delete.clicked.connect(self.barang_delete)
        self.ui.barang_pay.clicked.connect(self.barang_pay)
        
        # Button Customer
        self.ui.cust_tambah.clicked.connect(self.cust_tambah)
        self.ui.cust_edit.clicked.connect(self.cust_edit)
        self.ui.cust_hapus.clicked.connect(self.cust_hapus)
        self.ui.cust_refresh.clicked.connect(self.cust_refresh)
    
    def barang_preview(self):
        db = sqlite3.connect(db_filename)
        cursor = db.cursor()
        
        # ambil index tabel_barang
        row = self.ui.table_barang.currentRow()
        nama = self.ui.table_barang.item(row, 0).text()
        
        # query ke database untuk mendapatkan detail dari barang yg dipilih
        cursor.execute("SELECT b.nama, b.sell, b.quantity, b.expiry_date, s.nama AS Supplier FROM Barang b JOIN Supplier s ON b.id_supplier = s.id_supplier WHERE b.nama = ?", (nama,))
        
        # tampilkan kedalam line edit
        data_barang = cursor.fetchone()
        self.ui.barang_nama.setText(data_barang[0])
        self.ui.barang_harga.setText(str(data_barang[1]))
        self.ui.barang_stok.setText(str(data_barang[2]))
        self.ui.barang_expired.setDate(QDate.fromString(data_barang[3], "yyyy-MM-dd"))
        self.ui.barang_supplier.setCurrentText(data_barang[4])
        
        self.ui.barang_nama.setReadOnly(True)
        self.ui.barang_harga.setReadOnly(True)
        self.ui.barang_stok.setReadOnly(True)
        self.ui.barang_expired.setReadOnly(True)
        self.ui.barang_supplier.setDisabled(True)
    
    def barang_refresh(self):
        db = sqlite3.connect(db_filename)
        cursor = db.cursor()
        
        # table_barang on QTableWidget
        cursor.execute("SELECT nama FROM Barang")
        data_barang = cursor.fetchall()
        self.ui.table_barang.setRowCount(len(data_barang))
        self.ui.table_barang.setColumnCount(len(data_barang[0]))
        self.ui.table_barang.setHorizontalHeaderLabels(['Nama'])
        self.ui.table_barang.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.table_barang.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.ui.table_barang.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.ui.table_barang.setAlternatingRowColors(True)
        self.ui.table_barang.verticalHeader().setVisible(False)
        self.ui.table_barang.horizontalHeader().setStretchLastSection(True)
        self.ui.table_barang.setSortingEnabled(True)
        self.ui.table_barang.setShowGrid(False)
        
        for i in range(len(data_barang)):
            for j in range(len(data_barang[0])):
                self.ui.table_barang.setItem(i, j, QTableWidgetItem(str(data_barang[i][j])))
                self.ui.table_barang.item(i, j).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.ui.barang_nama.setText("")
        self.ui.barang_harga.setText("")
        self.ui.barang_stok.setText("")
        self.ui.barang_expired.setDate(QDate())
        self.ui.barang_supplier.setCurrentIndex(0)
        
        self.ui.barang_nama.setReadOnly(True)
        self.ui.barang_harga.setReadOnly(True)
        self.ui.barang_stok.setReadOnly(True)
        self.ui.barang_expired.setReadOnly(True)
        self.ui.barang_supplier.setDisabled(True)
    
    def barang_viewCart(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    
    def barang_back(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    
    def barang_addCart(self):
        db = sqlite3.connect(db_filename)
        cursor = db.cursor()
        
        # ambil nama barang dan totalBeli dari line edit
        nama = self.ui.barang_nama.text()
        totalBeli = self.ui.barang_totalBeli.text()
        
        # query ke database untuk mendapatkan detail dari barang yg dipilih
        cursor.execute("SELECT b.nama, b.sell, b.quantity, b.expiry_date, s.nama AS Supplier FROM Barang b JOIN Supplier s ON b.id_supplier = s.id_supplier WHERE b.nama = ?", (nama,))
        data_barang = cursor.fetchone()
        
        # CEK STOK > qty self.cart = ['Nama', 'Harga', 'Qty', 'Total']
        if int(totalBeli) > data_barang[2]:
            QMessageBox.critical(self, "Error", "Stok tidak cukup!")
        else:
            # CEK BARANG SUDAH ADA DI CART ATAU BELUM
            if len(self.cart) == 0:
                # cek qty cart > data_barang[2]
                if int(totalBeli) > data_barang[2]:
                    QMessageBox.critical(self, "Error", "Stok tidak cukup!")
                    return
                else:
                    self.cart.append([data_barang[0], data_barang[1], int(totalBeli), int(totalBeli)*data_barang[1]])
            else:
                # cek qty cart > data_barang[2]
                for item in self.cart:
                    if item[0] == data_barang[0]:
                        if item[2] + int(totalBeli) > data_barang[2]:
                            QMessageBox.critical(self, "Error", "Stok tidak cukup!")
                            return
                        else:
                            item[2] += int(totalBeli)
                            item[3] = item[2] * item[1]
                            break
                else:
                    self.cart.append([data_barang[0], data_barang[1], int(totalBeli), int(totalBeli)*data_barang[1]])
                    
        # update table cart
        self.ui.table_cart.setRowCount(len(self.cart))
        self.ui.table_cart.setColumnCount(len(self.cart[0]))
        self.ui.table_cart.setHorizontalHeaderLabels(['Nama', 'Harga', 'Qty', 'Total'])
        self.ui.table_cart.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.table_cart.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.ui.table_cart.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.ui.table_cart.setAlternatingRowColors(True)
        self.ui.table_cart.verticalHeader().setVisible(False)
        self.ui.table_cart.horizontalHeader().setStretchLastSection(True)
        self.ui.table_cart.setSortingEnabled(True)
        self.ui.table_cart.setShowGrid(False)
        
        for i in range(len(self.cart)):
            for j in range(len(self.cart[0])):
                self.ui.table_cart.setItem(i, j, QTableWidgetItem(str(self.cart[i][j])))
                self.ui.table_cart.item(i, j).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
        self.ui.barang_nama.setText("")
        self.ui.barang_harga.setText("")
        self.ui.barang_stok.setText("")
        self.ui.barang_expired.setDate(QDate())
        self.ui.barang_supplier.setCurrentIndex(0)
        self.ui.barang_totalBeli.setText("")
        # update subtotal
        subtotal = 0
        for item in self.cart:
            subtotal += item[3]
        self.ui.barang_subTotal.setText(str(subtotal))

    def barang_sum(self):
        db = sqlite3.connect(db_filename)
        cursor = db.cursor()
        
        #  cek apakah table_cart kosong
        if len(self.cart) == 0:
            QMessageBox.critical(self, "Error", "Cart kosong!")
        else:
            if self.ui.barang_dibayar.text() == "":
                QMessageBox.critical(self, "Error", "Uang tidak boleh kosong!")
            elif int(self.ui.barang_dibayar.text()) < int(self.ui.barang_subTotal.text()):
                QMessageBox.critical(self, "Error", "Uang tidak cukup!")
            else:
                subtotal = int(self.ui.barang_subTotal.text())
                dibayar = int(self.ui.barang_dibayar.text())
                kembali = dibayar - subtotal
                self.ui.barang_kembali.setText(str(kembali))
            
    def barang_delete(self):
        db = sqlite3.connect(db_filename)
        cursor = db.cursor()
        
        # ambil index tabel_cart
        row = self.ui.table_cart.currentRow()
        nama = self.ui.table_cart.item(row, 0).text()
        
        # hapus data
        for item in self.cart:
            if item[0] == nama:
                self.cart.remove(item)
                break
        
        # update table cart
        self.ui.table_cart.setRowCount(len(self.cart))
        self.ui.table_cart.setColumnCount(len(self.cart[0]))
        self.ui.table_cart.setHorizontalHeaderLabels(['Nama', 'Harga', 'Qty', 'Total'])
        self.ui.table_cart.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.table_cart.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.ui.table_cart.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.ui.table_cart.setAlternatingRowColors(True)
        self.ui.table_cart.verticalHeader().setVisible(False)
        self.ui.table_cart.horizontalHeader().setStretchLastSection(True)
        self.ui.table_cart.setSortingEnabled(True)
        self.ui.table_cart.setShowGrid(False)
        
        for i in range(len(self.cart)):
            for j in range(len(self.cart[0])):
                self.ui.table_cart.setItem(i, j, QTableWidgetItem(str(self.cart[i][j])))
                self.ui.table_cart.item(i, j).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
        self.ui.barang_nama.setText("")
        self.ui.barang_harga.setText("")
        self.ui.barang_stok.setText("")
        self.ui.barang_expired.setDate(QDate())
        self.ui.barang_supplier.setCurrentIndex(0)
        self.ui.barang_totalBeli.setText("")
        # update subtotal
        subtotal = 0
        for item in self.cart:
            subtotal += item[3]
        self.ui.barang_subTotal.setText(str(subtotal))
        # update total bayar dan kembalian
        self.ui.barang_dibayar.setText("")
        self.ui.barang_kembali.setText("")
        
    def barang_pay(self):
        db = sqlite3.connect(db_filename)
        cursor = db.cursor()
        
        if self.ui.table_cart.rowCount() == 0:
            QMessageBox.critical(self, "Error", "Cart kosong!")
        else:
            # cek apakah barang_kembali kosong
            if self.ui.barang_kembali.text() == "":
                QMessageBox.critical(self, "Error", "Silahkan hitung total belanja terlebih dahulu!")
            else:
                if int(self.ui.barang_dibayar.text()) < int(self.ui.barang_subTotal.text()):
                    QMessageBox.critical(self, "Error", "Uang tidak cukup!")
                else:
                    total = int(self.ui.barang_subTotal.text())
                    dibayar = int(self.ui.barang_dibayar.text())
                    kembali = int(self.ui.barang_kembali.text())
                    
                    # tampilkan id_customer dari database berdasarkan combobox
                    id_customer = self.ui.barang_customer.currentData()
                    
                    # generate faktur penjualan
                    id_faktur = "F" + QDateTime.currentDateTime().toString("ddMMyyyyhhmmss")
                    
                    # ambil data dari QTableWidget table_cart
                    for row in range(self.ui.table_cart.rowCount()):
                        nama = self.ui.table_cart.item(row, 0).text()
                        harga = self.ui.table_cart.item(row, 1).text()
                        qty = self.ui.table_cart.item(row, 2).text()
                        total = self.ui.table_cart.item(row, 3).text()
                        
                        # ambil id barang dari nama barang
                        cursor.execute("SELECT id_barang FROM Barang WHERE nama = ?", (nama,))
                        id_barang = cursor.fetchone()[0]
                        
                        # insert data ke tabel penjualan Penjualan (id_faktur, id_customer, id_barang, tgl_penjualan, jumlah, sum_price)
                        cursor.execute("INSERT INTO Penjualan (id_faktur, id_customer, id_barang, tgl_penjualan, jumlah, sum_price) VALUES (?, ?, ?, ?, ?, ?)", (id_faktur, id_customer, id_barang, QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss"), qty, total))
                        
                        # update stok barang
                        cursor.execute("UPDATE Barang SET quantity = quantity - ? WHERE id_barang = ?", (qty, id_barang))
                    
                    # masukkan penjualan ke tabel Transaksi (id_faktur, total, dibayar, kembali)
                    cursor.execute("INSERT INTO Transaksi (id_faktur, total, dibayar, kembali) VALUES (?, ?, ?, ?)", (id_faktur, total, dibayar, kembali))
                    db.commit()
                    # message box berhasil
                    QMessageBox.information(self, "Penjualan Berhasil", "Transaksi telah disimpan.")
                
                    self.cart.clear()
                    self.ui.table_cart.clear()
                    
                    # kosongkan med_subTotal
                    self.ui.barang_subTotal.setText("")
                    self.ui.barang_dibayar.setText("")
                    self.ui.barang_kembali.setText("")
                    
                    # refresh table barang
                    self.barang_refresh()
    
    # Customer
    def cust_tambah(self):
        if self.ui.cust_tambah.text() == "Tambah":
            db = sqlite3.connect(db_filename)
            cursor = db.cursor()
            
            nama = self.ui.cust_nama.text()
            contact = self.ui.cust_contact.text()
            alamat = self.ui.cust_alamat.text()
            
            if nama == "" or contact == "" or alamat == "":
                QMessageBox.critical(self, "Error", "Data tidak boleh kosong!")
            else:
                try:
                    cursor.execute("INSERT INTO Customer (nama, contact, alamat) VALUES (?, ?, ?)", (nama, contact, alamat))
                    db.commit()
                    QMessageBox.information(self, "Info", "Data berhasil ditambahkan!")
                except sqlite3.Error as e:
                    print("Error:", e)
                    QMessageBox.critical(self, "Error", "Data gagal ditambahkan!")
                finally:
                    if db:
                        db.close()
                    # kosongkan line edit
                    self.ui.cust_nama.setText("")
                    self.ui.cust_contact.setText("")
                    self.ui.cust_alamat.setText("")
                    # refresh table
                    self.cust_refresh()
                
        elif self.ui.cust_tambah.text() == "Edit":
            db = sqlite3.connect(db_filename)
            cursor = db.cursor()
            
            nama = self.ui.cust_nama.text()
            contact = self.ui.cust_contact.text()
            alamat = self.ui.cust_alamat.text()
            
            if nama == "" or contact == "" or alamat == "":
                QMessageBox.critical(self, "Error", "Data tidak boleh kosong!")
            else:
                try:
                    cursor.execute("UPDATE Customer SET nama = ?, contact = ?, alamat = ? WHERE nama = ?", (nama, contact, alamat, nama))
                    db.commit()
                    QMessageBox.information(self, "Info", "Data berhasil diubah!")
                except sqlite3.Error as e:
                    print("Error:", e)
                    QMessageBox.critical(self, "Error", "Data gagal diubah!")
                finally:
                    if db:
                        db.close()
                    # kosongkan line edit
                    self.ui.cust_nama.setText("")
                    self.ui.cust_contact.setText("")
                    self.ui.cust_alamat.setText("")
                    self.ui.cust_tambah.setText("Tambah")
                    self.ui.cust_edit.setText("Edit")
                    # refresh table
                    self.cust_refresh()
            
    def cust_edit(self):
        if self.ui.cust_edit.text() == "Edit":
            # ambil dari current index table widget table_cust
            row = self.ui.table_cust.currentRow()
            nama = self.ui.table_cust.item(row, 0).text()
            contact = self.ui.table_cust.item(row, 1).text()
            alamat = self.ui.table_cust.item(row, 2).text()
            
            self.ui.cust_nama.setReadOnly(True)
            self.ui.cust_nama.setText(nama)
            self.ui.cust_contact.setText(contact)
            self.ui.cust_alamat.setText(alamat)
            
            self.ui.cust_tambah.setText("Edit")
            self.ui.cust_edit.setText("Cancel")
            
        elif self.ui.cust_edit.text() == "Cancel":
            self.ui.cust_nama.setText("")
            self.ui.cust_contact.setText("")
            self.ui.cust_alamat.setText("")
            
            self.ui.cust_edit.setText("Edit")
            self.ui.cust_tambah.setText("Tambah")
    
    def cust_hapus(self):
        db = sqlite3.connect(db_filename)
        cursor = db.cursor()
        
        # ambil dari current index table widget table_cust
        row = self.ui.table_cust.currentRow()
        nama = self.ui.table_cust.item(row, 0).text()
        
        # hapus data
        try:
            cursor.execute("DELETE FROM Customer WHERE nama = ?", (nama,))
            db.commit()
            QMessageBox.information(self, "Info", "Data berhasil dihapus!")
        except sqlite3.Error as e:
            print("Error:", e)
            QMessageBox.critical(self, "Error", "Data gagal dihapus!")
        finally:
            if db:
                db.close()
            # refresh table
            self.cust_refresh()
        
    def cust_refresh(self):
        if self.ui.cust_refresh.text() == "Refresh":
            db = sqlite3.connect(db_filename)
            cursor = db.cursor()
            
            # table_cust on QTableWidget
            cursor.execute("SELECT * FROM Customer")
            data_customer = cursor.fetchall()
            self.ui.table_cust.setRowCount(len(data_customer))
            self.ui.table_cust.setColumnCount(len(data_customer[0])-1)
            self.ui.table_cust.setHorizontalHeaderLabels(['Nama', 'No. Telp', 'Alamat'])
            self.ui.table_cust.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.ui.table_cust.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
            self.ui.table_cust.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            self.ui.table_cust.setAlternatingRowColors(True)
            self.ui.table_cust.verticalHeader().setVisible(False)
            self.ui.table_cust.horizontalHeader().setStretchLastSection(True)
            self.ui.table_cust.setSortingEnabled(True)
            self.ui.table_cust.setShowGrid(False)
            
            for i in range(len(data_customer)):
                for j in range(1, len(data_customer[0])):
                    self.ui.table_cust.setItem(i, j-1, QTableWidgetItem(str(data_customer[i][j])))
                    self.ui.table_cust.item(i, j-1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.ui.cust_nama.setReadOnly(False)

        elif self.ui.cust_refresh.text() == "Cancel":
            self.ui.cust_nama.setText("")
            self.ui.cust_contact.setText("")
            self.ui.cust_alamat.setText("")

            self.ui.cust_refresh.setText("Refresh")
            self.ui.cust_tambah.setText("Tambah")

            self.cust_refresh()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    sys.exit(app.exec())
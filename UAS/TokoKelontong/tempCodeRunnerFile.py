db = sqlite3.connect(db_filename)
        # cursor = db.cursor()
        
        # # ambil nama barang dan totalBeli dari line edit
        # nama = self.ui.barang_nama.text()
        # totalBeli = self.ui.barang_totalBeli.text()
        
        # # query ke database untuk mendapatkan detail dari barang yg dipilih
        # cursor.execute("SELECT b.nama, b.sell, b.quantity, b.expiry_date, s.nama AS Supplier FROM Barang b JOIN Supplier s ON b.id_supplier = s.id_supplier WHERE b.nama = ?", (nama,))
        # data_barang = cursor.fetchone()
        
        # # cek apakah barang sudah ada di cart QTableWidget
        # for i in range(self.ui.table_cart.rowCount()):
        #     if self.ui.table_cart.item(i, 0).text() == nama:
        #         QMessageBox.critical(self, "Error", "Barang sudah ada di cart!")
        #         return
            
        #     # message box berhasil
        #     QMessageBox.information(self, "Info", "Barang berhasil ditambahkan ke cart!")
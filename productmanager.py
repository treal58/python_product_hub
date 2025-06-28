import products
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QDialog, QCheckBox,
                             QLineEdit, QHBoxLayout, QVBoxLayout, QMessageBox, QInputDialog,
                             QDialogButtonBox)
from PyQt5.QtCore import Qt

class ProductManager(QWidget):
    def __init__(self):
        super().__init__()
        self.title = QLabel("Product Manager", self)
        self.insert_title = QLabel("Insert new product data:", self)

        self.name_label = QLabel("· Name: ", self)
        self.name_textbox = QLineEdit(self)
        self.name_textbox.setPlaceholderText("Enter the name of your product")

        self.topic_label = QLabel("· Topic: ", self)
        self.topic_textbox = QLineEdit(self)
        self.topic_textbox.setPlaceholderText("Enter the topic of your product")

        self.price_label = QLabel("· Price: ", self)
        self.price_textbox = QLineEdit(self)
        self.price_textbox.setPlaceholderText("Enter the price of your product")

        self.message_label = QLabel(self)
        self.create_product_button = QPushButton("Create Product", self)
        self.delete_products_button = QPushButton("Delete Products", self)
        self.import_button = QPushButton("Import Products", self)
        self.export_button = QPushButton("Export Current Products", self)

        self.create_product_button.clicked.connect(self.create_product)
        self.delete_products_button.clicked.connect(self.delete_products)
        self.import_button.clicked.connect(self.import_prd)
        self.export_button.clicked.connect(self.export_prd)

        self.setMinimumWidth(400)
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.title)
        vbox.addWidget(self.insert_title)
        vbox.addWidget(self.name_label)
        vbox.addWidget(self.name_textbox)
        vbox.addWidget(self.topic_label)
        vbox.addWidget(self.topic_textbox)
        vbox.addWidget(self.price_label)
        vbox.addWidget(self.price_textbox)
        vbox.addWidget(self.message_label)
        vbox.addWidget(self.create_product_button)
        vbox.addWidget(self.delete_products_button)

        # So the import and export buttons look different
        hbox = QHBoxLayout()
        hbox.addWidget(self.import_button)
        hbox.addWidget(self.export_button)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setStyleSheet("""
            * {
                font-size: 18px;
                font-family: Calibri;
            } 
        """)

        self.title.setAlignment(Qt.AlignCenter)
        self.message_label.setAlignment(Qt.AlignCenter)

        self.setWindowTitle("Product Creator")

    def create_product(self):
        try:
            name = self.name_textbox.text()
            topic = self.topic_textbox.text()
            price = self.price_textbox.text()
            if name and topic and float(price) > 0:
                current = products.Product(name, topic.lower(), float(price))
                object_message = (f"· Name: {current.name}\n"
                                  f"· Topic: {current.topic}\n"
                                  f"· Price: {current.price}\n"
                                  f"· Price without taxes: {current.notax_price}")
                if current.topic == "default":
                    object_message += f"\n\nTopic '{topic}' not found, using 'default'"
                    self.name_textbox.setText("")
                    self.topic_textbox.setText("")
                    self.price_textbox.setText("")
                else:
                    self.message_label.setText("")
                    self.name_textbox.setText("")
                    self.topic_textbox.setText("")
                    self.price_textbox.setText("")
            else:
                raise ValueError
            self.message_label.setText("Product Successfully Created!")
            QMessageBox.information(self, "New Product Created", object_message)
        except ValueError:
            warning = QMessageBox()
            warning.critical(self, "Error", "Product data is not in the right format or the product already exists.\n\n"
                                            "* Price must not contain any symbols,\nand must be greater than 0")

    def delete_products(self):
        if not products.Product.get_instances():
            QMessageBox.warning(self, "Product Deleter", "There are no products available")
            return
        product_deleter = ProductDeleter()
        if product_deleter.exec_():
            selected = product_deleter.get_selected_products()
            for prd in selected:
                products.delete_products(prd.name)



    def import_prd(self):
        success = False

        default = QMessageBox.question(self, "Import", "Would you like to use default file (products.json)?")
        if default == QMessageBox.Yes:
            success = products.import_prd_from_json() ## Will import from products.json
        else:
            file, ok = QInputDialog.getText(self, "Import", "Enter the directory of the file being imported (.json needed):")
            if ok and file:
                success = products.import_prd_from_json(file)

        if success:
            self.message_label.setText("Successfully imported!")
        else:
            QMessageBox.critical(self, "Error Importing", "Could not import the file.\nMake sure it exists and is valid.")

    def export_prd(self):
        default = QMessageBox.question(self, "Export", "Would you like to export to the default file (products.json)?")
        if default == QMessageBox.Yes:
            if products.Product.get_instances():
                products.export_prd_to_json() ## Will export to products.json
            else:
                QMessageBox.critical(self, "Error Exporting", "There are no products to export")
        else:
            file, ok = QInputDialog.getText(self, "Import",
                                            "Enter the directory of where you want to export the file(.json needed):")
            if (ok and file) and products.Product.get_instances():
                products.export_prd_to_json(file)
                self.message_label.setText("Successfully exported!")
            else:
                QMessageBox.critical(self, "Error Exporting", "There are no products to export")


# Window just for deleting products, with checkboxes
class ProductDeleter(QDialog):
    def __init__(self):
        super().__init__()

        self.setMinimumWidth(250)

        self.setWindowTitle("Product deleter")
        self.title = QLabel("Delete Products", self)
        self.select_all_button = QPushButton("Select All", self)
        self.unselect_all_button = QPushButton("Unselect All", self)
        self.checkboxes = list()

        self.title.setAlignment(Qt.AlignCenter)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        self.select_all_button.clicked.connect(self.select_all)
        self.unselect_all_button.clicked.connect(self.unselect_all)

        vbox = QVBoxLayout()
        vbox.addWidget(self.title)
        vbox.addWidget(self.select_all_button)
        vbox.addWidget(self.unselect_all_button)

        for product in products.Product.get_instances():
            checkbox = QCheckBox(f"{product.name}")
            checkbox.prd = product
            self.checkboxes.append(checkbox)
            vbox.addWidget(checkbox)

        vbox.addWidget(button_box)

        self.setLayout(vbox)

        self.setStyleSheet("""
            * {
                font-size: 14px;
                font-family: Calibri;
            }
        """)

    def get_selected_products(self):
        return [
            cb.prd
            for cb in self.checkboxes if cb.isChecked()
        ]

    def select_all(self):
        for cb in self.checkboxes:
            cb.setChecked(True)

    def unselect_all(self):
        for cb in self.checkboxes:
            cb.setChecked(False)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    creator = ProductManager()
    creator.show()
    sys.exit(app.exec_())

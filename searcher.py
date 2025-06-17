import products

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                             QPushButton, QLineEdit, QMessageBox, QInputDialog)
from PyQt5.QtCore import Qt

class Searcher(QWidget):
    def __init__(self):
        super().__init__()
        self.title         = QLabel("Search for an Item...", self)
        self.search_button = QPushButton("Search", self)
        self.search_box    = QLineEdit(self)
        self.search_box.setPlaceholderText("Write the name of a product")

        self.item_name_label  = QLabel("Item Name: ...", self)
        self.item_price_label = QLabel("Item Price: ...", self)
        self.item_notax_label = QLabel("Price without taxes: ...", self)
        self.item_topic_label = QLabel("Item Topic: ...", self)
        self.message_label = QLabel(self)

        self.search_button.clicked.connect(self.search)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Searcher")

        vbox = QVBoxLayout()
        vbox.addWidget(self.title)
        vbox.addWidget(self.search_box)
        vbox.addWidget(self.search_button)
        vbox.addWidget(self.item_name_label)
        vbox.addWidget(self.item_price_label)
        vbox.addWidget(self.item_notax_label)
        vbox.addWidget(self.item_topic_label)
        vbox.addWidget(self.message_label)

        self.search_button.setMinimumHeight(55)

        self.setLayout(vbox)
        self.title.setObjectName("title")
        self.search_button.setObjectName("search_button")
        self.item_name_label.setObjectName("item_name_label")
        self.item_price_label.setObjectName("item_price_label")
        self.item_notax_label.setObjectName("item_notax_label")
        self.item_topic_label.setObjectName("item_topic_label")

        self.setStyleSheet("""
            * {
                font-size: 25px;
                font-family: Calibri;
            }
            QMessageBox{
                font-size: 15px;
            }
            QLabel#title{
                font-size: 40px;
                padding: 10px;
                background-color: hsl(140, 100%, 79%);
                border-radius: 15px;
            }
            QPushButton#search_button{
                padding: 10px 20px;
                font-weight: bold;
                background-color: hsl(206, 78%, 80%);
            }
            QPushButton#search_button:hover{
                font-size: 27px;
                font-weight: bold;
                background-color: hsl(206, 78%, 65%);
            }
            QLabel#item_name_label, QLabel#item_price_label, QLabel#item_topic_label, QLabel#item_notax_label{
                background-color: hsl(140, 100%, 79%);
                border-radius: 5px;
            }
        """)

        self.title.setAlignment(Qt.AlignCenter)
        self.message_label.setAlignment(Qt.AlignCenter)

    def search(self):
        product_list = products.Product.get_instances()
        found = False
        for product in product_list:
            if self.search_box.text().strip().lower() in product.name.lower():
                self.search_box.setText("")
                self.item_name_label.setText(f"Item Name: {product.name}")
                self.item_price_label.setText(f"Item Price: ${product.price}")
                self.item_notax_label.setText(f"Price without taxes: ${product.notax_price}")
                self.item_topic_label.setText(f"Item Topic: {product.topic.capitalize()} ({products.topics[product.topic]}% tax)")
                self.message_label.setText("")
                found = True
                break
        if not found:
            self.message_label.setText("Product not found!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    searcher = Searcher()
    searcher.show()
    sys.exit(app.exec_())
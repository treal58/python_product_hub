import products
from searcher import Searcher
from topicmanager import TopicManager, TopicImportDialog, TopicExportDialog
from productmanager import ProductCreator
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QMessageBox, QLabel, QPushButton,
                             QLineEdit, QDialog, QHBoxLayout, QVBoxLayout, QInputDialog,
                             QCheckBox, QDialogButtonBox)
from PyQt5.QtCore import Qt


class ProductHub(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Products Hub")

        self.title = QLabel("Products Hub", self)


        self.searcher = Searcher()
        self.topicman = TopicManager()
        self.productman = ProductCreator()

        self.searcher_button = QPushButton("Open Searcher", self)
        self.topicman_button = QPushButton("Open Topic Manager", self)
        self.productman_button = QPushButton("Open Product Manager", self)

        self.show_current_products_button = QPushButton("Show Current Products", self)
        self.show_current_topics_button = QPushButton("Show Current Topics", self)

        self.initUI()

        self.searcher_button.clicked.connect(self.searcher.show)
        self.topicman_button.clicked.connect(self.topicman.show)
        self.productman_button.clicked.connect(self.productman.show)
        self.show_current_topics_button.clicked.connect(self.show_current_topics)
        self.show_current_products_button.clicked.connect(self.show_current_products)

    def initUI(self):
        self.setMinimumWidth(500)

        vbox = QVBoxLayout()
        vbox.setSpacing(10)
        vbox.addWidget(self.title)
        self.title.setMinimumWidth(100)
        self.title.setMaximumHeight(150)

        vbox.addWidget(self.searcher_button)
        self.searcher_button.setMaximumHeight(150)

        vbox.addWidget(self.topicman_button)
        self.topicman_button.setMaximumHeight(150)

        vbox.addWidget(self.productman_button)
        self.productman_button.setMaximumHeight(150)

        hbox = QHBoxLayout()
        hbox.addWidget(self.show_current_products_button)
        self.show_current_products_button.setMaximumHeight(150)
        hbox.addWidget(self.show_current_topics_button)
        self.show_current_topics_button.setMaximumHeight(150)
        vbox.addLayout(hbox)

        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("title")
        self.searcher_button.setObjectName("searcher")
        self.productman_button.setObjectName("productman")
        self.topicman_button.setObjectName("topicman")
        self.show_current_topics_button.setObjectName("current_topics")
        self.show_current_products_button.setObjectName("current_products")

        self.setStyleSheet("""
            * {
                font-size: 25px;
                font-family: Calibri;
            }
            
            QPushButton {
                padding: 10px;
                border-radius: 8px;
            }

            
            QLabel#title{
                font-size: 40px;
                font-weight: bold;
                background-color: hsl(44, 90%, 60%);
                border-radius: 10px;
                margin: 10px;
            }
            
            QPushButton#searcher{
                background-color: hsl(140, 100%, 79%);
            }
            QPushButton#searcher:hover{
                font-size: 27px;
                background-color: hsl(140, 100%, 74%);
            }
            
            QPushButton#topicman{
                background-color: hsl(140, 83%, 43%);
            }
            QPushButton#topicman:hover{
                font-size: 27px;
                background-color: hsl(140, 83%, 38%);
            }
            
            QPushButton#productman{
                background-color: hsl(205, 82%, 56%);
            }
            QPushButton#productman:hover{
                font-size: 27px;
                background-color: hsl(205, 82%, 51%);
            }
            
            QPushButton#current_products, QPushButton#current_topics{
                font-size: 20px;
                background-color: hsl(110, 0%, 56%);
            }
            QPushButton#current_products:hover, QPushButton#current_topics:hover{
                font-size: 22px;
                background-color: hsl(110, 0%, 51%);
            }
        """)

        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

    def show_current_products(self):
        if products.Product.get_instances():
            info = ("Current products:\n"
                    "Format: name / topic / price\n\n")
            for product in products.Product.get_instances():
                info += f"- {product.name} / {product.topic} / ${product.price}\n"
            QMessageBox.information(self, "Current Products", info)
        else:
            QMessageBox.warning(self, "Current Products", "No products found")

    def show_current_topics(self):
        current_topics = ("--------------------\n"
        "  Current Topics:  \n"
        "--------------------")
        for key, value in products.topics.items():
            current_topics += f"\n{value}% - {key} "
        QMessageBox.information(self, "Tax Help", current_topics)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    product_hub = ProductHub()
    product_hub.show()
    sys.exit(app.exec_())
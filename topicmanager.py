import products
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox, QLabel, QPushButton,
                             QLineEdit, QDialog, QHBoxLayout, QVBoxLayout, QInputDialog,
                             QCheckBox, QDialogButtonBox)
from PyQt5.QtCore import Qt

class TopicManager(QWidget):
    def __init__(self):
        super().__init__()
        self.title = QLabel("Topic Manager")
        self.create_topic_title = QLabel("Create a new topic:")

        self.name_label = QLabel("· Name:", self)
        self.name_textbox = QLineEdit(self)
        self.name_textbox.setPlaceholderText("Enter the name of your new topic")


        self.tax_label = QLabel("· Tax Percentage:", self)
        self.tax_textbox = QLineEdit(self)
        self.tax_textbox.setPlaceholderText("Enter the tax percentage of your new topic")

        self.create_topic_button = QPushButton("Create Topic", self)

        self.import_topics_button = QPushButton("Import Custom Topics",self)
        self.export_topics_button = QPushButton("Export Custom Topics")

        self.message_label = QLabel(self)

        self.create_topic_button.clicked.connect(self.create_topic)
        self.import_topics_button.clicked.connect(self.open_import_dialog)
        self.export_topics_button.clicked.connect(self.open_export_dialog)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Topic Manager")
        self.setMinimumWidth(300)

        vbox = QVBoxLayout()
        vbox.addWidget(self.title)
        vbox.addWidget(self.create_topic_title)
        vbox.addWidget(self.name_label)
        vbox.addWidget(self.name_textbox)
        vbox.addWidget(self.tax_label)
        vbox.addWidget(self.tax_textbox)
        vbox.addWidget(self.create_topic_button)

        hbox = QHBoxLayout()
        hbox.addWidget(self.import_topics_button)
        hbox.addWidget(self.export_topics_button)
        vbox.addLayout(hbox)

        vbox.addWidget(self.message_label)

        self.setLayout(vbox)

        self.title.setAlignment(Qt.AlignCenter)
        self.message_label.setAlignment(Qt.AlignCenter)

        self.title.setObjectName("title")
        self.create_topic_title.setObjectName("create_topic_title")

        self.setStyleSheet("""
            * {
                font-size: 14px;
                font-family: Calibri;
            }
            QLabel#create_topic_title{
                padding-top: 10px;
            }
            QLabel#title{
                font-size: 18px;
            }
        """)

    def open_import_dialog(self):
        # Checks what file the user wants to import from
        default = QMessageBox.question(self, "Import", "Would you like to use default file (topics.json)?")
        if default == QMessageBox.Yes:
            data = products.import_topics_json(preview=True)  ## Will import from topics.json
        elif default == QMessageBox.No:
            file, ok = QInputDialog.getText(self, "Import",
                                            "Enter the directory of the file being imported (.json needed):")
            if ok and file:
                data = products.import_topics_json(file, preview=True)
            else:
                QMessageBox.critical(self, "Error", "The directory is invalid")
                return

        if not data:
            QMessageBox.critical(self, "Error", "No topics found in .json file")
            return
        # If there's no data in the .json the process will stop, but it will else continue

        dialog = TopicImportDialog(data, self)
        if dialog.exec_():
            selected = dialog.get_selected_topics()
            imported = 0
            for topic in selected:
                for name, tax in topic.items():
                    if name not in products.topics:
                        products.create_topic(name, tax)
                        imported += 1
            QMessageBox.information(self, "Success", f"{imported} topic(s) imported.")

    def open_export_dialog(self):
        # Checks what file the user wants to export to
        default = QMessageBox.question(self, "Export", "Would you like to use default file (topics.json)?")
        if default == QMessageBox.Yes:
            filedir = "topics.json" # Will use the default .json to export
        elif default == QMessageBox.No:
            file, ok = QInputDialog.getText(self, "Export",
                                            "Enter the directory of the output file (.json needed):")
            if ok and file:
                filedir = file
            else:
                QMessageBox.critical(self, "Error", "The directory is invalid")
                return

        dialog = TopicExportDialog(self)
        if dialog.exec_():
            selected = dialog.get_selected_topics()
            selected_names = [list(topic.keys())[0] for topic in selected]

            if not selected_names:
                QMessageBox.warning(self, "Warning", "No topics selected for export.")
                return

            products.export_topics_json(filedir, topics_to_export=selected_names)
            QMessageBox.information(self, "Success", f"{len(selected_names)} topic(s) exported.")

    def create_topic(self):
        name = self.name_textbox.text().lower().strip()
        tax = self.tax_textbox.text().strip()
        if not (name and tax):
            QMessageBox.warning(self, "Error", "Please type in the required information.")
            self.message_label.setText("Error creating the topic")
        else:
            try:
                tax = int(tax)
                if not name.isalpha(): raise ValueError
            except ValueError:
                QMessageBox.critical(self, "Error", "Name must be ONLY letters (a-z)\nTax Percentage must be an integer")
                self.message_label.setText("Error creating the topic")
                return
            if type(tax) is int:
                if name in products.topics.keys():
                    self.name_textbox.setText("")
                    self.tax_textbox.setText("")
                    QMessageBox.critical(self, "Error",f"Unable to create the topic.\nTopic '{name}' already exists")
                    self.message_label.setText("Error creating the topic")
                else:
                    products.create_topic(name, tax)
                    self.name_textbox.setText("")
                    self.tax_textbox.setText("")
                    self.message_label.setText(f"Topic '{name}' with {tax}% of taxes was created")

class TopicImportDialog(QDialog):
    def __init__(self, topics_list, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Topics to Import")
        self.setMinimumWidth(300)

        self.checkboxes = []
        vbox = QVBoxLayout()

        self.title = QLabel("Select the topics you want to import:")
        vbox.addWidget(self.title)

        self.select_all_button = QPushButton("Select All", self)
        self.unselect_all_button = QPushButton("Unselect All", self)
        vbox.addWidget(self.select_all_button)
        vbox.addWidget(self.unselect_all_button)

        for topic in topics_list:
            name, tax = list(topic.items())[0]
            checkbox = QCheckBox(f"{name} ({tax}%)")
            checkbox.topic_name = name
            checkbox.tax_percentage = tax
            self.checkboxes.append(checkbox)
            vbox.addWidget(checkbox)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.select_all_button.clicked.connect(self.select_all)
        self.unselect_all_button.clicked.connect(self.unselect_all)
        vbox.addWidget(button_box)

        self.setLayout(vbox)

    def get_selected_topics(self):
        return [
            {cb.topic_name: cb.tax_percentage}
            for cb in self.checkboxes if cb.isChecked()
        ]

    def select_all(self):
        for cb in self.checkboxes:
            cb.setChecked(True)

    def unselect_all(self):
        for cb in self.checkboxes:
            cb.setChecked(False)

class TopicExportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Topics to Export")
        self.setMinimumWidth(300)

        self.checkboxes = []
        vbox = QVBoxLayout()

        self.title = QLabel("Select the topics you want to export:")
        vbox.addWidget(self.title)

        self.select_all_button = QPushButton("Select All", self)
        self.unselect_all_button = QPushButton("Unselect All", self)
        vbox.addWidget(self.select_all_button)
        vbox.addWidget(self.unselect_all_button)

        for name, tax in list(products.topics.items())[10:]:
            checkbox = QCheckBox(f"{name} ({tax}%)")
            checkbox.topic_name = name
            checkbox.tax_percentage = tax
            self.checkboxes.append(checkbox)
            vbox.addWidget(checkbox)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.select_all_button.clicked.connect(self.select_all)
        self.unselect_all_button.clicked.connect(self.unselect_all)
        vbox.addWidget(button_box)

        self.setLayout(vbox)

    def get_selected_topics(self):
        return [
            {cb.topic_name: cb.tax_percentage}
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
    topic_man = TopicManager()
    topic_man.show()
    sys.exit(app.exec_())

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QMessageBox, QFileDialog
from ...buttons.group_buttons import DataGroupButtons
from ...dialogs.data_dialog import DataDialog
from ...tables.data_table import DataTable


class DataSettingsWidget(QWidget):

    addDatasetSignal = pyqtSignal(str, str)
    deleteDatasetSignal = pyqtSignal(list)
    changeDatasetSignal = pyqtSignal(int, str, str)
    copyDatasetSignal = pyqtSignal(list)

    loadSignal = pyqtSignal(str)
    saveSignal = pyqtSignal(str)
    clearSignal = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        layouts = QHBoxLayout()
        self.__table = DataTable(self)
        self.__buttons = DataGroupButtons(self)
        layouts.addWidget(self.__table)
        layouts.addWidget(self.__buttons)
        self.setLayout(layouts)
        self.__set_connections()

    def __set_connections(self):
        self.__buttons.get_buttons()['Add information'].clicked.connect(self.__show_dialog_add_dataset)
        self.__buttons.get_buttons()['Delete information'].clicked.connect(self.__click_delete_button)
        self.__buttons.get_buttons()['Change information'].clicked.connect(self.__show_dialog_change_dataset)
        self.__buttons.get_buttons()['Copy information'].clicked.connect(self.__copy_data)
        self.__buttons.get_buttons()['Load data'].clicked.connect(self.__show_dialog_parser_config)
        self.__buttons.get_buttons()['Save data'].clicked.connect(self.__show_dialog_create_config)
        self.__buttons.get_buttons()['Clear table'].clicked.connect(self.clearSignal.emit)

    def __show_dialog_add_dataset(self):
        dialog = DataDialog(self)
        if dialog.exec():
            self.addDatasetSignal.emit(*dialog.get_values())

    def __show_dialog_change_dataset(self):
        if len(self.__table.get_selected_rows()) != 1:
            QMessageBox.warning(self, 'Warning!', 'Choose one row!')
            return
        dialog = DataDialog(self)
        row = self.__table.get_selected_rows()[0]
        idx = 0
        for tag in dialog.tags:
            dialog.edits[tag].setText(self.__table.item(row, idx).text())
            idx += 1
        if dialog.exec():
            self.changeDatasetSignal.emit(row, *dialog.get_values())
        self.__table.remove_selection()

    def __show_dialog_parser_config(self):
        path_to_config = QFileDialog.getOpenFileName(self, 'Open File', '', 'XML files (*.xml)')
        if path_to_config[0]:
            self.loadSignal.emit(path_to_config[0])

    def __show_dialog_create_config(self):
        path_to_config = QFileDialog.getSaveFileName(self, 'Save File', '', 'XML files (*.xml)')
        if path_to_config[0]:
            self.saveSignal.emit(path_to_config[0])

    def show_message_status_saving(self, status):
        if status:
            QMessageBox.information(self, 'Success', 'Datasets data was created successfully!')
        else:
            QMessageBox.warning(self, 'Fail', 'Datasets data was not created!')

    def __click_delete_button(self):
        self.delDatasetSignal.emit(self.get_selected_rows())
        self.__table.remove_selection()

    def __copy_data(self):
        self.copyDatasetSignal.emit(self.get_selected_rows())

    def get_selected_rows(self):
        return self.__table.get_selected_rows()

    def update(self, model):
        self.__table.update(model.get_data())

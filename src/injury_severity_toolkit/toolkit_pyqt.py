import pandas as pd
import APACHEIII_Calculator as apache_Calc
import SOFA_Calculator as sofa_Calc
import CCI_Calculator as cci_Calc
import VFDs
import oxygenation
import sys
from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui
from pathlib import Path


class Stream(QtCore.QObject):
    """
    Stream object to emit text signal for console text box
    """
    text = QtCore.pyqtSignal(str)

    def write(self, text):
        self.text.emit(str(text))


class Toolkit(QMainWindow):
    """
    Main Toolkit UI Class
    """

    # Headers for future, currently not implemented
    apache_headers = []
    sofa_headers = []
    cci_headers = []

    def __init__(self):
        super().__init__()
        self.csv = None
        self.current_method = 'APACHE'
        self.results = None
        self.initUI()

    def initUI(self):
        """
        Acutal UI Initialization
        :return:
        """
        self.resize(500, 500)
        self.center()
        # Setup Main Window layout
        self.setCentralWidget(QWidget(self))
        self.hbox = QHBoxLayout()
        self.centralWidget().setLayout(self.hbox)
        sys.stdout = Stream(text=self.update_text)

        # Title
        self.setWindowTitle('Illness Severity Toolkit')

        # Menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        import_action = QAction('Import CSV', self)
        file_menu.addAction(import_action)
        import_action.triggered.connect(self.import_csv)

        # Create a top-level layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a text box the display console outputs.
        self.console_text = QTextEdit(self, readOnly=True)
        self.console_text.moveCursor(QtGui.QTextCursor.Start)
        self.console_text.ensureCursorVisible()
        self.console_text.setLineWrapColumnOrWidth(500)
        self.console_text.setLineWrapMode(QTextEdit.FixedPixelWidth)

        layout.addWidget(self.console_text)
        self.hbox.addLayout(layout)

        tabs = QTabWidget()
        tabs.addTab(self.methods_tab(), 'Methods')
        tabs.addTab(self.mapping_tab(), 'Mapping')
        tabs.addTab(self.results_preview(), 'Results Preview')
        layout.addWidget(tabs)

        # Add layout to main window
        self.hbox.addLayout(layout)

        # Run button
        self.run_btn = QPushButton('Run')
        self.run_btn.clicked.connect(self.run)
        self.run_btn.clicked.connect(self.export_csv)
        self.run_btn.clicked.connect(self.update_results_tab)
        self.run_btn.setDisabled(True)
        self.hbox.addWidget(self.run_btn)

    def methods_tab(self):
        """
        A QWidget that allows the presentation and selection of methods.
        :return: the QWidget itself.
        """
        generalTab = QWidget()
        layout = QVBoxLayout()

        self.method_dropdown = QComboBox(self)
        self.method_dropdown.addItem('APACHE')
        self.method_dropdown.addItem('SOFA')
        self.method_dropdown.addItem('CCI')
        self.method_dropdown.addItem('VFD')
        self.method_dropdown.addItem('OI')
        self.method_dropdown.activated[str].connect(self.select_method)

        layout.addWidget(self.method_dropdown)
        generalTab.setLayout(layout)
        return generalTab

    def mapping_tab(self):
        """Create a tab for mapping variables."""
        network_tab = QWidget()
        layout = QGridLayout()

        layout.addWidget(QLabel("Heart Rate High", self), 0, 0)
        layout.addWidget(QComboBox(self), 0, 1)
        network_tab.setLayout(layout)
        return network_tab

    def results_preview(self):
        """
        Presents the results of a method calculation for users to preview.
        :return: QWidget
        """
        results_tab = QWidget()
        layout = QVBoxLayout()
        self.table_view = QTableView(self)
        self.results_model = PandasModel(pd.DataFrame([]))

        self.table_view.setModel(self.results_model)

        layout.addWidget(self.table_view)
        results_tab.setLayout(layout)
        return results_tab

    def update_results_tab(self):
        """
        Update the results tab
        :return: None
        """
        self.results_model = PandasModel(self.results)
        self.table_view.setModel(self.results_model)

    def select_method(self, method):
        """
        Selects a method.
        :param method: APACHE, SOFA, OI, etc.
        :return: None
        """
        self.current_method = method

    def center(self):
        """
        Centers the main frame on the screen.
        :return: None
        """
        main_window = self.frameGeometry()
        # QDesktop gets screen info, availableGeometry gets rectangle of monitor and center gets the center
        center_point = QDesktopWidget().availableGeometry().center()

        main_window.moveCenter(center_point)
        self.move(main_window.topLeft())

    def import_csv(self):
        """
        Imports a csv file.
        :return: None
        """
        base_dir = str(Path.home())
        file = QFileDialog.getOpenFileName(self, 'Open file', base_dir)

        if file[0] != '':
            self.csv = pd.read_csv(file[0])
            self.run_btn.setEnabled(True)
            print(f"File: {file[0]} imported")

    def export_csv(self):
        """
        Exports a csv file.
        :return: None
        """
        name = QFileDialog.getSaveFileName(self, 'Save File', filter='*.csv')
        if name[0] != '':
            if self.current_method != 'SOFA':
                self.results.to_csv(name[0], index=None, header=True)
            else:
                self.results.to_csv(name[0], index=True, header=True)
        print(f"File {name[0]} exported")

    def run(self):
        """
        Runs a script depending on the current selected button.
        :return: None
        """
        if self.current_method == "APACHE":
            self.results = apache_Calc.run(self.csv)
        elif self.current_method == "SOFA":
            self.results = sofa_Calc.run(self.csv)
        elif self.current_method == "CCI":
            self.results = cci_Calc.run(self.csv)
        elif self.current_method == "VFD":
            self.results = VFDs.run(self.csv)
        elif self.current_method == "OI":
            self.results = oxygenation.run(self.csv)

    def update_text(self, text):
        """
        Updates the console text box with what was sent to console output
        :param text: str text in std_out
        :return: None
        """
        cursor = self.console_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.console_text.setTextCursor(cursor)
        self.console_text.ensureCursorVisible()

    def __del__(self):
        sys.stdout = sys.__stdout__


class PandasModel(QAbstractTableModel):
    """
    Custom table model for results preview. Allows PyQT5 to display pandas datafames.
    """
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


def main():
    app = QApplication(sys.argv)

    toolkit = Toolkit()
    toolkit.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

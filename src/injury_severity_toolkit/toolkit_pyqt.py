import pandas as pd
import APACHEIII_Calculator as apache_Calc
import SOFA_Calculator as sofa_Calc
import CCI_Calculator as cci_Calc
import VFDs
import oxygenation
import sys
from PyQt5.Qt import *
from PyQt5 import QtCore
from pathlib import Path


class Toolkit(QMainWindow):

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
        self.resize(500, 500)
        self.center()
        # Setup Main Window layout
        self.setCentralWidget(QWidget(self))
        self.hbox = QHBoxLayout()
        self.centralWidget().setLayout(self.hbox)

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
        """Create the General page UI."""
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
        """Create the Network page UI."""
        network_tab = QWidget()
        layout = QGridLayout()

        layout.addWidget(QLabel("Heart Rate High", self), 0, 0)
        layout.addWidget(QComboBox(self), 0, 1)
        network_tab.setLayout(layout)
        return network_tab

    def results_preview(self):
        results_tab = QWidget()
        layout = QVBoxLayout()
        self.table_view = QTableView(self)
        self.results_model = PandasModel(pd.DataFrame([]))

        self.table_view.setModel(self.results_model)

        layout.addWidget(self.table_view)
        results_tab.setLayout(layout)
        return results_tab

    def update_results_tab(self):
        self.results_model = PandasModel(self.results)
        self.table_view.setModel(self.results_model)

    def select_method(self, method):
        self.current_method = method

    def center(self):
        main_window = self.frameGeometry()
        # QDesktop gets screen info, availableGeometry gets rectangle of monitor and center gets the center
        center_point = QDesktopWidget().availableGeometry().center()

        main_window.moveCenter(center_point)
        self.move(main_window.topLeft())

    def import_csv(self):
        base_dir = str(Path.home())
        file = QFileDialog.getOpenFileName(self, 'Open file', base_dir)

        if file[0] != '':
            self.csv = pd.read_csv(file[0])
            self.run_btn.setEnabled(True)

    def export_csv(self):
        name = QFileDialog.getSaveFileName(self, 'Save File', filter='*.csv')
        if name[0] != '':
            if self.current_method != 'SOFA':
                self.results.to_csv(name[0], index=None, header=True)
            else:
                self.results.to_csv(name[0], index=True, header=True)

    def run(self):

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


class PandasModel(QAbstractTableModel):
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


class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()

        ok_button = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(ok_button)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        msg = ""


def main():
    app = QApplication(sys.argv)

    toolkit = Toolkit()
    toolkit.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

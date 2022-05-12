import pandas as pd
import APACHEIII_Calculator as apache_Calc
import SOFA_Calculator as sofa_Calc
import CCI_Calculator as cci_Calc
import VFDs
import oxygenation
import sys
from PyQt5.QtWidgets import QComboBox, QPushButton, QApplication, QDesktopWidget, QFileDialog, QMainWindow
from PyQt5.Qt import *
from pathlib import Path


class Toolkit(QMainWindow):

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
        layout.addWidget(tabs)

        # Add layout to main window
        self.hbox.addLayout(layout)

    def methods_tab(self):
        """Create the General page UI."""
        generalTab = QWidget()
        layout = QVBoxLayout()

        self.method_dropdown = QComboBox(self)
        self.method_dropdown.move(100, 0)
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
        networkTab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QCheckBox("Network Option 1"))
        layout.addWidget(QCheckBox("Network Option 2"))
        networkTab.setLayout(layout)
        return networkTab

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

    # def select_scoring(self, pressed):


def main():
    app = QApplication(sys.argv)

    toolkit = Toolkit()
    toolkit.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

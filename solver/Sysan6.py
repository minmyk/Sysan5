from PyQt5.QtWidgets import QTableWidget, QSpinBox, QLabel, QApplication, QLineEdit, QDialog, QGroupBox, \
    QHBoxLayout, QComboBox, QGridLayout, QStyleFactory, QCheckBox, QPushButton, QWidget, QTableWidgetItem, QTabWidget, \
    QHeaderView
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtCore import Qt
import numpy as np
import sys


class UI(QDialog):
    def __init__(self, parent=None):
        super(UI, self).__init__(parent)

        self.reset = QPushButton("Reset")
        self.run = QPushButton("Execute")
        self.useStylePaletteCheckBox = QCheckBox("Light")
        self.tab1hbox = QHBoxLayout()
        self.tab2hbox = QHBoxLayout()
        self.Btab1 = QWidget()
        self.Btab2 = QWidget()
        self.tables = [QTableWidget(self.Btab1), QTableWidget(self.Btab1),
                       QTableWidget(self.Btab2), QTableWidget(self.Btab2)]

        self.bottomBox = QTabWidget()

        self.Mlabel2 = QLabel("Optimal weights TOPSAS:")
        self.Mlabel1 = QLabel("Optimal weights VIKTOR:")
        self.MspinBox2 = QLineEdit("")
        self.MspinBox1 = QLineEdit("")
        self.middleBox = QGroupBox("Optimal strategies")

        self.outputs = []
        self.results = QLabel()
        self.originalPalette = QApplication.palette()
        self.topBox = QHBoxLayout()
        self.setWindowIcon(QIcon('icon.jpg'))
        self.setWindowTitle("SWOT")
        self.setWindowIconText('SWOT')

        self.create_top_box()
        self.create_bottom_box()
        self.create_middle_box()

        self.mainLayout = QGridLayout()
        self.mainLayout.addLayout(self.topBox,      0, 0)
        self.mainLayout.addWidget(self.middleBox,   1, 0)
        self.mainLayout.addWidget(self.bottomBox,   2, 0)

        self.setLayout(self.mainLayout)
        self.resize(800, 600)
        self.change_palette()

    def change_palette(self):
        dark_palette = QPalette()

        QApplication.setStyle(QStyleFactory.create("Fusion"))

        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
        dark_palette.setColor(QPalette.Base, QColor(42, 42, 42))
        dark_palette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
        dark_palette.setColor(QPalette.Dark, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.Shadow, QColor(20, 20, 20))
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80))
        dark_palette.setColor(QPalette.HighlightedText, Qt.white)
        dark_palette.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(127, 127, 127))

        if self.useStylePaletteCheckBox.isChecked():
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(dark_palette)

    def create_top_box(self):
        self.useStylePaletteCheckBox.setChecked(False)
        self.reset.setFlat(True)
        self.run.setFlat(True)
        self.topBox.addWidget(self.useStylePaletteCheckBox)
        self.topBox.addStretch(1)
        self.topBox.addWidget(self.run)
        self.topBox.addWidget(self.reset)

    def create_bottom_box(self):
        for index in range(len(self.tables)):
            self.tables[index].setColumnCount(2)
            if index in (0, 1):
                self.tables[index].setRowCount(12)
            else:
                self.tables[index].setRowCount(10)
            self.tables[index].setHorizontalHeaderLabels(["Strength level", "F"])
            header = self.tables[index].horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.Stretch)

        self.tab1hbox.setContentsMargins(5, 5, 5, 5)
        self.tab1hbox.addWidget(self.tables[0])
        self.tab1hbox.addWidget(self.tables[1])
        self.Btab1.setLayout(self.tab1hbox)

        self.tab2hbox.setContentsMargins(5, 5, 5, 5)
        self.tab2hbox.addWidget(self.tables[2])
        self.tab2hbox.addWidget(self.tables[3])
        self.Btab2.setLayout(self.tab2hbox)

        self.bottomBox.addTab(self.Btab1, "Strengths / Weaknesses")
        self.bottomBox.addTab(self.Btab2, "Opportunities / Threats")

    def create_middle_box(self):
        self.outputs.append(self.MspinBox1)
        self.outputs.append(self.MspinBox2)

        layout = QGridLayout()
        self.MspinBox1.setPlaceholderText("Here will be displayed optimal VIKTOR strategies after calculations")
        self.MspinBox2.setPlaceholderText("Here will be displayed optimal TOP SAS strategies after calculations")
        layout.addWidget(self.MspinBox1, 0, 1, 1, 4)
        layout.addWidget(self.MspinBox2, 1, 1, 1, 4)
        layout.addWidget(self.Mlabel1, 0, 0, 1, 1)
        layout.addWidget(self.Mlabel2, 1, 0)

        self.middleBox.setLayout(layout)

    def clr(self):
        pass

    def execute(self):
        self.useStylePaletteCheckBox.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = UI()
    main_window.show()
    main_window.useStylePaletteCheckBox.toggled.connect(main_window.change_palette)
    main_window.reset.clicked.connect(main_window.clr)
    main_window.run.clicked.connect(main_window.execute)
    app.exec_()

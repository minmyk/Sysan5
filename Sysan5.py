from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QTableWidget, QLabel, QApplication, QLineEdit, QDialog, QGroupBox, \
    QHBoxLayout, QComboBox, QGridLayout, QStyleFactory, QCheckBox, QPushButton, QWidget, QTableWidgetItem, QTabWidget
from PyQt5.QtGui import QPalette, QColor, QIcon
import sys
from PyQt5.QtCore import Qt
from sklearn.preprocessing import Normalizer
import pandas as pd
from solver.IneqSolver import *


class Graph(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, title=None):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_title(title)
        self.compute_initial_figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

    def compute_initial_figure(self):
        pass


class UI(QDialog):
    def __init__(self, parent=None):
        super(UI, self).__init__(parent)

        self.confidence_label = QLabel("Confidence interval")
        self.confidence_value = QComboBox()
        self.confidence_value.addItems(["0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9"])
        self.reset = QPushButton("Reset")
        self.run = QPushButton("Execute")
        self.useStylePaletteCheckBox = QCheckBox("Light")

        self.tab1hbox = QHBoxLayout()
        self.Btab1 = QWidget()
        self.Btable = QTableWidget(self.Btab1)
        self.middleBox = QTabWidget()

        self.Mlabel4 = QLabel("For S4:")
        self.Mlabel3 = QLabel("For S3:")
        self.Mlabel2 = QLabel("For S2:")
        self.Mlabel1 = QLabel("For S1:")
        self.MspinBox4 = QLineEdit("")
        self.MspinBox3 = QLineEdit("")
        self.MspinBox2 = QLineEdit("")
        self.MspinBox1 = QLineEdit("")
        self.bottomBox = QGroupBox("Results")

        self.outputs = []
        self.results = QLabel()
        self.originalPalette = QApplication.palette()
        self.topBox = QHBoxLayout()
        self.setWindowIcon(QIcon('icon.jpg'))
        self.setWindowTitle("Solver")
        self.setWindowIconText('Solver')

        self.create_top_box()
        self.create_middle_box()
        self.create_bottom_box()

        self.canvas1 = Graph(self, width=6, height=3, dpi=100, title='Y1')
        self.canvas2 = Graph(self, width=6, height=3, dpi=100, title='Y2')
        self.canvas3 = Graph(self, width=6, height=3, dpi=100, title='Y3')
        self.canvas4 = Graph(self, width=6, height=3, dpi=100, title='Y4')

        self.mainLayout = QGridLayout()
        self.mainLayout.addLayout(self.topBox, 0, 0, 1, 6)
        self.mainLayout.addWidget(self.middleBox, 1, 2, 1, 2)
        self.mainLayout.addWidget(self.bottomBox, 2, 2, 2, 2)
        self.mainLayout.addWidget(self.canvas1, 1, 0)
        self.mainLayout.addWidget(self.canvas2, 2, 0)
        self.mainLayout.addWidget(self.canvas3, 1, 4)
        self.mainLayout.addWidget(self.canvas4, 2, 4)

        self.setLayout(self.mainLayout)
        self.resize(1360, 600)
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
        self.useStylePaletteCheckBox.setChecked(True)
        self.reset.setFlat(True)
        self.run.setFlat(True)

        self.topBox.addWidget(self.confidence_label)
        self.topBox.addWidget(self.confidence_value)
        self.topBox.addStretch(1)
        self.topBox.addWidget(self.useStylePaletteCheckBox)
        self.topBox.addWidget(self.run)
        self.topBox.addWidget(self.reset)

    def create_middle_box(self):
        self.Btable.setColumnCount(7)
        self.Btable.setRowCount(0)
        self.Btable.setHorizontalHeaderLabels(["       1        ",
                                               "       2        ",
                                               "       3        ",
                                               "       4        ",
                                               "       5        ",
                                               "       6        ",
                                               "       7        "])
        for j in range(4):
            self.Btable.insertRow(j)
            for i in range(7):
                self.Btable.setColumnWidth(i, 622/7)

                self.Btable.setItem(j, i, QTableWidgetItem(''))
        self.Btable.setFixedHeight(144)

        self.tab1hbox.setContentsMargins(5, 5, 5, 5)
        self.tab1hbox.addWidget(self.Btable)

        self.Btab1.setLayout(self.tab1hbox)

        self.middleBox.addTab(self.Btab1, "S[ i ] / Ф[ j ]")

    def create_bottom_box(self):

        self.outputs.append(self.MspinBox1)
        self.outputs.append(self.MspinBox2)
        self.outputs.append(self.MspinBox3)
        self.outputs.append(self.MspinBox4)

        layout = QGridLayout()

        layout.addWidget(self.MspinBox1, 0, 1, 1, 4)
        layout.addWidget(self.MspinBox2, 1, 1, 1, 4)
        layout.addWidget(self.MspinBox3, 2, 1, 1, 4)
        layout.addWidget(self.MspinBox4, 3, 1, 1, 4)
        layout.addWidget(self.Mlabel1, 0, 0, 1, 1)
        layout.addWidget(self.Mlabel2, 1, 0)
        layout.addWidget(self.Mlabel3, 2, 0)
        layout.addWidget(self.Mlabel4, 3, 0)

        self.bottomBox.setFixedWidth(645)
        self.bottomBox.setLayout(layout)

    def clr(self):
        self.Btable.clear()

    def view(self, solver):
        for i in range(4):
            for j in range(7):
                if solver.intervals_left[i][j] != 0 and solver.intervals_right[i][j] != 0:
                    self.Btable.setItem(i,
                                        j,
                                        QTableWidgetItem('[' + str(np.round(solver.intervals_left[i][j], 2)) +
                                                         ' ; ' + str(np.round(solver.intervals_right[i][j], 2)) + ']'))
                else:
                    self.Btable.setItem(i, j, QTableWidgetItem('Empty'))

    def plot(self, solver):
        pass

    def execute(self):
        self.useStylePaletteCheckBox.setEnabled(False)
        solver = Solver(float(self.confidence_value.currentText()))
        solver.solve()
        print(solver.intervals[0])
        print(solver.intervals[1])
        print(solver.intervals[2])
        print(solver.intervals_right)
        print(solver.t_plus_t_minus())
        self.view(solver)


def collect_data(path='data/sys_lab5.txt'):
    file = open(path, 'r')
    data = file.read()
    file.close()
    for matrix in data.split(';'):
        yield pd.DataFrame(np.array([el.split() for el in matrix.split('\n') if el]).flatten().reshape(4, 7)).apply(
                pd.to_numeric)


class Solver:
    def __init__(self, upper_bound):
        self.intervals = [[[0, 0]]*7]*4
        self.intervals_left = np.zeros((4, 7))
        self.intervals_right = np.zeros((4, 7))
        self.params = ['a_hat', 'I_p_hat', 'I_t_hat', 'I_d_hat']
        self.tables = {k: v for k, v in zip(self.params, list(collect_data()))}
        self.mask = self.tables['a_hat'] != 0
        self.upper_bound = upper_bound
        self.select = lambda i, j: {k: v for k, v in zip(self.params,
                                                         [matrix.iat[i, j] for matrix in self.tables.values()])}
        self.t_plus_t_minus = lambda: {'min': np.amax(self.intervals_left, axis=1),
                                       'max': np.amax(self.intervals_right, axis=1)}

    def classificator(self):
        fuzzy_constraints = {
            0: [0.1, 0.4],
            0.1: [0.12, 0.42],
            0.2: [0.14, 0.44],
            0.3: [0.16, 0.46],
            0.4: [0.18, 0.48],
            0.5: [0.2, 0.5],
            0.6: [0.22, 0.52],
            0.7: [0.24, 0.54],
            0.8: [0.26, 0.56],
            0.9: [0.28, 0.58],
            1: [0.3, 0.6]}

    def plot(self):
        pass

    def solve(self, lower_bound=0):
        for i in range(4):
            for j in range(7):
                if self.mask.to_numpy()[i, j]:
                    self.intervals[i][j] = IneqSolver(
                        param_dict=self.select(i, j)
                    ).solve(entropy, lower_bound, self.upper_bound).get_interval()
                    self.intervals_left[i][j] = self.intervals[i][j][0]
                    self.intervals_right[i][j] = self.intervals[i][j][1]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = UI()
    main_window.show()
    main_window.useStylePaletteCheckBox.toggled.connect(main_window.change_palette)
    main_window.reset.clicked.connect(main_window.clr)
    main_window.run.clicked.connect(main_window.execute)
    app.exec_()

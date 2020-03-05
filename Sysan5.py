from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QTableWidget, QSpinBox, QLabel, QApplication, QLineEdit, QDialog, QGroupBox, \
    QHBoxLayout, QComboBox, QGridLayout, QStyleFactory, QCheckBox, QPushButton, QWidget, QTableWidgetItem, QTabWidget
from PyQt5.QtGui import QPalette, QColor, QIcon
import sys
from PyQt5.QtCore import Qt
import pandas as pd
from solver.IneqSolver import *
from itertools import product


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
        self.i_label = QLabel('i')
        self.i = QSpinBox()
        self.j_label = QLabel('j')
        self.j = QSpinBox()
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

        self.canvas1 = Graph(self, width=6, height=3, dpi=100, title='I_t')
        self.canvas2 = Graph(self, width=6, height=3, dpi=100, title='I_p')
        self.canvas3 = Graph(self, width=6, height=3, dpi=100, title='I_d')
        self.canvas4 = Graph(self, width=6, height=3, dpi=100, title='I')

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
        self.topBox.addWidget(self.i_label)
        self.topBox.addWidget(self.i)
        self.topBox.addWidget(self.j_label)
        self.topBox.addWidget(self.j)
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
        for i in range(4):
            self.outputs[i].clear()

    def view(self, solver):
        for i in range(4):
            for j in range(7):
                if solver.intervals_right[i][j] != 0:
                    self.Btable.setItem(i,
                                        j,
                                        QTableWidgetItem('[' + str(np.round(solver.intervals_left[i][j], 2)) +
                                                         ' ; ' + str(np.round(solver.intervals_right[i][j], 2)) + ']'))
                elif solver.mask.to_numpy()[i, j]:
                    self.Btable.setItem(i, j, QTableWidgetItem('Empty'))
                else:
                    self.Btable.setItem(i, j, QTableWidgetItem('-'))

    def plot(self, solver):
        I_p1 = np.vectorize(
            lambda t, I_p_hat: min(t / np.sqrt(1 + (1 - 1e-4 ** 2) / (1 - I_p_hat - 1e-4) ** 2 - 1 * t ** 2) + I_p_hat,
                                   1))

        I_d1 = np.vectorize(
            lambda t, I_d_hat: min(np.log(1 + np.exp(np.log(2 * np.exp(1 - I_d_hat) - 1) * t)) - np.log(2) + I_d_hat,
                                   1))

        I_t1 = np.vectorize(lambda t, I_t_hat: max(I_t_hat * (1 - t ** 2), 0))

        I1 = np.vectorize(lambda t, I_p_hat, I_d_hat, I_t_hat: I_p(t, I_p_hat) * I_d(t, I_d_hat) * I_t(t, I_t_hat))

        i_t = I_t1(np.linspace(0, 1, 1001), solver.tables['I_t_hat'][self.i.value()][self.j.value()])
        i_p = I_p1(np.linspace(0, 1, 1001), solver.tables['I_p_hat'][self.i.value()][self.j.value()])
        i_d = I_d1(np.linspace(0, 1, 1001), solver.tables['I_d_hat'][self.i.value()][self.j.value()])
        i = i_t * i_d * i_p

        self.canvas1.axes.clear()
        self.canvas2.axes.clear()
        self.canvas3.axes.clear()
        self.canvas4.axes.clear()
        self.canvas1.axes.set_title('I_t')
        self.canvas2.axes.set_title('I_p')
        self.canvas3.axes.set_title('I_d')
        self.canvas4.axes.set_title('I')
        self.canvas1.axes.plot(np.linspace(0, 1, 1001), i_t, lw=1, color='blue')
        self.canvas2.axes.plot(np.linspace(0, 1, 1001), i_p, lw=1, color='green')
        self.canvas3.axes.plot(np.linspace(0, 1, 1001), i_d, lw=1, color='red')
        self.canvas4.axes.plot(np.linspace(0, 1, 1001), i, lw=1, color='brown')
        self.canvas1.draw()
        self.canvas2.draw()
        self.canvas3.draw()
        self.canvas4.draw()

    def execute(self):
        self.useStylePaletteCheckBox.setEnabled(False)
        solver = Solver(float(self.confidence_value.currentText()))
        solver.solve()
        self.view(solver)
        self.plot(solver)
        for i in range(4):
            self.outputs[i].clear()
            self.outputs[i].setText(solver.classificator()[i])


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
        self.t_plus_t_minus = None

    def classificator(self):
        states = []
        for interval in self.t_plus_t_minus:
            if (interval[1] - interval[0]) / interval[1] > 0.66:
                states.append('Normal situation')
            elif 0.33 < (interval[1] - interval[0]) / interval[1] < 0.66:
                states.append('Potential hazard')
            else:
                states.append('Emergency')
        return states

    def solve(self, lower_bound=0):
        self.intervals = np.zeros((4, 7), dtype='f,f')
        self.mask = self.tables['a_hat'] != 0
        for i, j in product(range(4), range(7)):
            if self.mask.to_numpy()[i, j]:
                solution = IneqSolver(self.select(i, j)).solve(entropy, lower_bound, self.upper_bound).get_interval()
                self.intervals[i][j] = tuple(solution)
                self.intervals_left[i][j] = self.intervals[i][j][0]
                self.intervals_right[i][j] = self.intervals[i][j][1]
        self.t_plus_t_minus = [(a, b) for a, b in zip(np.amax(self.intervals_left, axis=0),
                               np.amax(self.intervals_right, axis=0))]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = UI()
    main_window.show()
    main_window.useStylePaletteCheckBox.toggled.connect(main_window.change_palette)
    main_window.reset.clicked.connect(main_window.clr)
    main_window.run.clicked.connect(main_window.execute)
    app.exec_()

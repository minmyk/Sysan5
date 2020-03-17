from PyQt5.QtWidgets import QTableWidget, QLabel, QApplication, QLineEdit, QDialog, QGroupBox, \
    QHBoxLayout, QGridLayout, QStyleFactory, QCheckBox, QPushButton, QWidget, QTableWidgetItem, QTabWidget, \
    QHeaderView
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtCore import Qt
import sys
import numpy as np
from Sysan_6.create_swot_table import *


class SWOTComponentMatrix(object):
    """
    Object to load/save SWOT component matrix
    """

    def __init__(self, strengths=None, weaknesses=None, opportunities=None, threats=None):
        """
        Args:
            strengths(array-like): list of strengths considered in SWOT analysis
            weaknesses(array-like): list of weaknesses considered in SWOT analysis
            opportunities(array-like): list of opportunities considered in SWOT analysis
            threats(array-like): list of threats considered in SWOT analysis
        """
        if strengths == None:
            self.strengths = (
                "No human interaction in driving",
                "Prevention of car accidents",
                "Speed limit",
                "Traffic analysis and lane moving control",
                "ABS, ESP systems",
                "Automatic Parking",
                "Fully automated Traffic Regulations",
                "Rational route selection",
                "Rational fuel usage",
                "Public transport sync",
                "Automatic photos",
                "Rational time management",
            )
        else:
            self.strengths = strengths

        if weaknesses == None:
            self.weaknesses = (
                "System wear",
                "Huge computational complexity",
                "Electric dependency",
                "Computer vision weaknesses (accuracy)",
                "Huge error price",
                "Potential persnal data leakage",
                "GPS/Internet quality",
                "No relationships with non-automated cars",
                "Trolley problem",
                "Software bugs",
                "High price",
                "Man depends on vehicle"
            )
        else:
            self.weaknesses = weaknesses

        if opportunities == None:
            self.opportunities = (
                "E-maps of road signs",
                "Vehicle to vehicle connection",
                "More passanger places (no driver needed)",
                "System to prevent trafic jams",
                "Alternative energy usage",
                "New powerful computer vision technologies",
                "Cars technologies with less polution",
                "High efficency engines",
                "High demand on cars",
                "Goverment support of autonomous cars dev",
            )
        else:
            self.opportunities = opportunities

        if threats == None:
            self.threats = (
                "High production price",
                "High service price",
                "Not enough qualified mechanics",
                "Bad road cover surface",
                "Not ordinary behaivor of some road users",
                "Rejection by people",
                "Hacking, confidentiality problems",
                "Increased scam interest",
                "Job abolition",
                "Inadequacy of legal system",
            )
        else:
            self.threats = threats

            self.SWOT = None

    def load(self, filename):
        """
        Load data from .html file.
        Args:
             filename(str): path to .html file with values

        Returns:
             self(SWOTComponentMatrixParser):self object
        """
        self.SWOT = pd.read_html(filename, index_col=0)[0]
        return self

    def get_components(self):
        """
        Decompose SWOT matrix into 4 components.
        Returns:
             SO(pandas.DataFrame): strengths-opportunities component matrix
             ST(pandas.DataFrame): strengths-threats component matrix
             WO(pandas.DataFrame): weaknesses-opportunities component matrix
             WT(pandas.DataFrame): weaknesses-threats component matrix
        """
        so = self.SWOT.loc[pd.IndexSlice[self.strengths, self.opportunities]]
        st = self.SWOT.loc[pd.IndexSlice[self.strengths, self.threats]]
        wo = self.SWOT.loc[pd.IndexSlice[self.weaknesses, self.opportunities]]
        wt = self.SWOT.loc[pd.IndexSlice[self.weaknesses, self.threats]]
        return so, st, wo, wt

    def save_html_table(self, filename, fontsize=8, text_align='center', font='Arial', header_color="#87c5c5"):
        """
        Save nice looking .html file of SWOT table.
        Args:
            filename(str): path to file where to save .html table
            fontsize(int): Size of font in pt
            text_align(str): alligning table elements. Options: left,center,right
            font(str): Font to use in html render
            header_color(str): html hex code of color
        Returns:
        """

        # Set CSS properties for td elements in dataframe
        def hover(hover_color="#add8e6"):
            return dict(selector="tbody tr:hover", props=[("background-color", "%s" % hover_color)])

        styles = [
            # table properties
            dict(selector=" ",
                 props=[("margin", "0"),
                        ("font-family", font),
                        ("border-collapse", "collapse"),
                        ("border", "none"),
                        ("border", "2px solid #ccf")
                        ]),

            # header color - optional
            dict(selector="thead",
                 props=[("background-color", header_color)]),

            # background shading
            dict(selector="tbody tr:nth-child(even)",
                 props=[("background-color", "#fff")]),
            dict(selector="tbody tr:nth-child(odd)",
                 props=[("background-color", "#eee")]),

            # cell spacing
            dict(selector="td",
                 props=[("padding", ".1em")]),

            # header cell properties
            dict(selector="th",
                 props=[("font-size", str(fontsize) + "pt"),
                        ("text-align", text_align)]),
            # render hover last to override background-color
            hover()
        ]
        html = self.SWOT.style.background_gradient(
            subset=(self.SWOT.index[self.SWOT.index.isin(self.strengths)], self.SWOT.columns.isin(self.threats)),
            cmap="Oranges",
            axis=None,
        ).background_gradient(
            subset=(self.SWOT.index[self.SWOT.index.isin(self.weaknesses)], self.SWOT.columns.isin(self.threats)),
            cmap="Reds",
            axis=None,
        ).background_gradient(
            subset=(self.SWOT.index[self.SWOT.index.isin(self.strengths)], self.SWOT.columns.isin(self.opportunities)),
            cmap="Greens",
            axis=None,
        ).background_gradient(
            subset=(self.SWOT.index[self.SWOT.index.isin(self.weaknesses)], self.SWOT.columns.isin(self.opportunities)),
            cmap="Blues",
            axis=None,
        ).set_table_styles(styles).set_properties(**{'text-align': text_align})
        with open(filename, "w") as f:
            f.write(html.render())


def initialize():
    """ by Vamdemon """
    databank = Parasha()
    databank.parasha()
    so = databank.so_letters
    st = databank.st_letters
    wo = databank.wo_letters
    wt = databank.wt_letters

    swot = pd.concat((pd.concat((st, so), axis=1), pd.concat((wt, wo), axis=1)), axis=0)

    return swot


def get_weights(swot_table):
    s = swot_table.index.str[0] == 'S'
    w = swot_table.index.str[0] == 'W'
    o = swot_table.columns.str[0] == 'O'
    t = swot_table.columns.str[0] == 'T'

    t_score = swot_table.loc[s, t].sum(axis=0) - swot_table.loc[w, t].sum(axis=0)
    o_score = swot_table.loc[s, o].sum(axis=0) - swot_table.loc[w, o].sum(axis=0)
    s_score = swot_table.loc[s, t].sum(axis=1) + swot_table.loc[s, o].sum(axis=1)
    w_score = swot_table.loc[w, t].sum(axis=1) + swot_table.loc[w, o].sum(axis=1)

    return t_score, o_score, s_score, w_score


def get_parasha_tables(swot_table):
    o = swot_table.columns.str[0] == 'O'
    t = swot_table.columns.str[0] == 'T'
    s = swot_table.index.str[0] == 'S'
    w = swot_table.index.str[0] == 'W'

    parasha_so = pd.Series(
        {col: swot_table.loc[s, col][swot_table[col] != 0.].index.values for col in swot_table.loc[:, o].columns},
        name='SO')
    parasha_wo = pd.Series(
        {col: swot_table.loc[w, col][swot_table[col] != 0.].index.values for col in swot_table.loc[:, o].columns},
        name='WO')
    parasha_wt = pd.Series(
        {col: swot_table.loc[w, col][swot_table[col] != 0.].index.values for col in swot_table.loc[:, t].columns},
        name='WT')
    parasha_st = pd.Series(
        {col: swot_table.loc[s, col][swot_table[col] != 0.].index.values for col in swot_table.loc[:, t].columns},
        name='ST')

    parasha_o = pd.concat([parasha_so, parasha_wo], axis=1)
    parasha_t = pd.concat([parasha_st, parasha_wt], axis=1)
    return parasha_o, parasha_t


def form_strategies():
    strategies = pd.DataFrame(np.load("data/strategy.npy"))
    return strategies


def get_d_upper_lower(strategies):
    strategies_max = pd.concat((strategies, pd.DataFrame({'maximal': strategies.max(axis=1)})), axis=1)
    strategies_max_min = pd.concat((strategies_max, pd.DataFrame({'minimal': strategies.min(axis=1)})), axis=1)
    bounds = []
    for strategy in strategies.columns:
        bounds.append([0, 0])
        for index in strategies.index:
            bounds[-1][0] += (strategies[strategy][index] - strategies_max_min['minimal'][index]) ** 2
            bounds[-1][1] += (strategies[strategy][index] - strategies_max_min['maximal'][index]) ** 2
        bounds[-1][0] = np.sqrt(bounds[-1][0])
        bounds[-1][1] = np.sqrt(bounds[-1][1])

    criterions = list(map(lambda bound: bound[0] / (bound[0] + bound[1]), bounds))
    return strategies.columns[np.argmax(criterions)]


def topsis():
    strategies = form_strategies()
    strategy = get_d_upper_lower(strategies)

    return "Strategy " + str(strategy)


def vikor(w=np.array([1 / 44] * 44), v=0.51):
    """
        by Volomos
        @matr_E - Matr(nxr) - матриця значень вагових коеф.
            n – кількість варіантів системи; R – кількість показників.
        @w - dim = r - вектор вагових коефіцієнтів показників
        @v - коефіцієнт збалансованості з інтервалу [0, 1]
    """

    e = form_strategies().T
    e = e.to_numpy()
    n = e.shape[0]
    r = e.shape[1]

    # 1st stage

    best_e = np.zeros(r)
    worst_e = np.zeros(r)

    for j in range(r):
        best_e[j] = np.max(e[:, j])
        worst_e[j] = np.min(e[:, j])

    # 2nd stage

    # print(e)

    s = [sum([w[j] * (best_e[j] - e[i, j]) / (best_e[j] - worst_e[j])
              for j in range(r)]) for i in range(n)]
    # print(S)
    # 3rd stage
    r = np.array([np.max([(w[j] * (best_e[j] - e[i, j])) / (best_e[j] - worst_e[j])
                          for j in range(r)]) for i in range(n)])
    # 4th stage
    # print(e)
    best_r = np.max(r)
    best_s = np.max(s)

    worst_r = np.min(r)
    worst_s = np.min(s)
    q = np.array([np.array([(r[i] - worst_r) / (best_r - worst_r) if best_s == worst_s else
                            (s[i] - worst_s) / (best_s - worst_s) if best_r == worst_r else
                            v * (s[i] - worst_s) / (best_s - worst_s) +
                            (1 - v) * (r[i] - worst_r) / (best_r - worst_r), i]) for i in range(n)])

    # 6th stage
    q = q[q[:, 0].argsort()]

    # 1st - preference criterion
    criterion_1 = False

    d_q = 1 / (n - 1)

    if q[0][0] - q[1][0] > d_q:
        criterion_1 = True

    # 2nd - partial values criterion
    criterion_2 = False
    if s[int(q[0][1])] < s[int(q[1][1])] and r[int(q[0][1])] < r[int(q[1][1])]:
        criterion_2 = True

    if criterion_1 and criterion_2:
        print('Альтернатива ' + str(q[0][0]) + ' найкраща')

    elif not criterion_1 and criterion_2:
        k = 1
        while q[0][0] - q[k][0] < d_q:
            k += 1
            if k >= q.shape[0]:
                break
        print('До множини компромісних альтернатив входять ' + str(k) +
              ' альтернатив: ' + str([q[i][1] for i in range(k)]))

    elif criterion_1 and not criterion_2:
        print('Розгляду підлягають альтернативи ' + str(q[0][1]) + ', ' + str(q[1][1]))

    else:
        print('---')
    return "Strategy " + str(int(q[0][1] + 1))


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

        self.Mlabel2 = QLabel("Optimal weights TOPSIS:")
        self.Mlabel1 = QLabel("Optimal weights VITOR:")
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
        self.mainLayout.addLayout(self.topBox, 0, 0)
        self.mainLayout.addWidget(self.middleBox, 1, 0)
        self.mainLayout.addWidget(self.bottomBox, 2, 0)

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
            header = self.tables[index].horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.Stretch)

        self.tables[0].setHorizontalHeaderLabels(["Strength level", "F"])
        self.tables[1].setHorizontalHeaderLabels(["Weakness level", "F"])
        self.tables[2].setHorizontalHeaderLabels(["Opportunities level", "F"])
        self.tables[3].setHorizontalHeaderLabels(["Threats level", "F"])

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
        self.MspinBox1.setPlaceholderText("Here will be displayed optimal VITOR strategy "
                                          "after calculations are finished.")
        self.MspinBox2.setPlaceholderText("Here will be displayed optimal TOPSIS strategy "
                                          "after calculations are finished.")
        layout.addWidget(self.MspinBox1, 0, 1, 1, 4)
        layout.addWidget(self.MspinBox2, 1, 1, 1, 4)
        layout.addWidget(self.Mlabel1, 0, 0, 1, 1)
        layout.addWidget(self.Mlabel2, 1, 0)

        self.middleBox.setLayout(layout)

    def clr(self):
        self.MspinBox1.setText("")
        self.MspinBox2.setText("")
        for table in self.tables:
            table.clearContents()

    def fill_table(self, table_index, table_to_fill):
        for index in range(len(table_to_fill.to_numpy())):
            item1 = QTableWidgetItem(list(table_to_fill.index)[index])
            item1.setTextAlignment(Qt.AlignHCenter)
            self.tables[table_index].setItem(index, 0, item1)
            item2 = QTableWidgetItem(str(np.round(table_to_fill.to_numpy(), 3)[index]))
            item2.setTextAlignment(Qt.AlignHCenter)
            self.tables[table_index].setItem(index, 1, item2)

    def execute(self):
        self.clr()
        swot = initialize()
        scores = get_weights(swot)
        self.MspinBox1.setText(vikor())
        self.MspinBox2.setText(topsis())
        self.fill_table(0, scores[2])
        self.fill_table(1, scores[3])
        self.fill_table(2, scores[1])
        self.fill_table(3, scores[0])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = UI()
    main_window.show()
    main_window.useStylePaletteCheckBox.toggled.connect(main_window.change_palette)
    main_window.reset.clicked.connect(main_window.clr)
    main_window.run.clicked.connect(main_window.execute)
    app.exec_()

import csv
from utilities import operations
from datetime import datetime
from PyQt6 import uic, QtGui
import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QCalendarWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt, QDate
from tkinter.filedialog import askopenfilename


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        # self.open_file()

        uic.loadUi('C:\\Users\\gianm\\OneDrive\\Desktop\\Scalable\\try2.ui', self)

        self.pushButton.clicked.connect(self.open_file)
        self.tabWidget.setTabVisible(0, False)
        self.tabWidget.setTabVisible(1, False)
        self.calendarWidget.setVisible(False)
        self.calendarWidget_2.setVisible(False)
        self.lineEdit.setVisible(False)
        self.lineEdit_2.setVisible(False)
        self.pushButton_2.setVisible(False)
        self.pushButton_3.setVisible(False)

        self.show()

    def open_file(self):
        global list_rows
        list_rows = []
        filename = askopenfilename()
        if 'ScalableCapital-Broker' in filename:
            with open(filename, 'r') as f:
                input_file = csv.reader(f, delimiter=';')
                for row in input_file:
                    if row[2] != 'Cancelled' and row[2] != 'status':
                        list_rows.append(row)
        ranges = operations.dates_range(list_rows)
        list_rows.reverse()
        capital = operations.find_capital(list_rows)
        stock_list, interests = operations.find_closed_positions_buyorientedtry(list_rows)
        self.ui_tabs(capital, stock_list, interests, ranges)

    def ui_tabs(self, capital, stock_list, interests, ranges):
        uic.loadUi('C:\\Users\\gianm\\OneDrive\\Desktop\\Scalable\\try2.ui', self)
        self.pushButton.clicked.connect(self.open_file)
        self.lineEdit.setText(ranges[0])
        self.lineEdit_2.setText(ranges[1])
        self.lineEdit.setInputMask('00/00/0000')
        self.lineEdit_2.setInputMask('00/00/0000')
        self.calendarWidget.setVisible(False)
        self.calendarWidget_2.setVisible(False)
        self.pushButton_2.setIcon(QtGui.QIcon("utilities/calendar.png"))
        self.pushButton_2.clicked.connect(self.calendar_end)
        self.pushButton_3.setIcon(QtGui.QIcon("utilities/calendar.png"))
        self.pushButton_3.clicked.connect(self.calendar_start)
        # self.lineEdit.textEdited.connect(self.open_file)

        self.label_recap.setText(f"Capital:   {capital}")
        self.label_recap_2.setText(f"Earnings:   {interests}")
        self.label_recap_3.setText(f"({round(interests * 100 / capital, 2)}%)")

        label_recaps = [self.label_recap, self.label_recap_2, self.label_recap_3]
        for label in label_recaps:
            label.setStyleSheet("color: #888888; font-weight: 700; font-size: 12px;")
            label.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.tabWidget.setStyleSheet("color: #fff; background-color: #313131; font-size: 12px;")

        labels = [self.label, self.label_2, self.label_3, self.label_4, self.label_5, self.label_6]
        for i in range(len(labels)):
            labels[i].setStyleSheet("color: #888888; font-weight: 700;")

        stock_list.reverse()

        #  Set up table
        for stock in range(len(stock_list)):
            self.tableWidget.insertRow(stock)

            if stock % 2 == 0:
                background_color = QtGui.QColor('#444444')
            else:
                background_color = QtGui.QColor('#313131')

            list_attr = [stock_list[stock].name, stock_list[stock].price_diff, stock_list[stock].percentage]

            #  Populate table
            for i in range(len(list_attr)):
                item = QTableWidgetItem(str(list_attr[i]))
                item.setBackground(background_color)
                if i != 0:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if i == 2:
                    item.setText(f"{str(list_attr[i])}%")
                    if list_attr[i] > 0:
                        item.setForeground(QtGui.QColor('green'))
                    else:
                        item.setForeground(QtGui.QColor('red'))
                self.tableWidget.setItem(stock, i, item)

        #  Tab by title
        try:
            for stock in range(len(stock_list)):
                for check in range(stock + 1, len(stock_list)):
                    if stock_list[stock].name == stock_list[check].name:
                        stock_list[stock].price_diff += stock_list[check].price_diff
                        stock_list[stock].money_out += stock_list[check].money_out
                        stock_list[stock].percentage = round((stock_list[stock].price_diff / -stock_list[stock].money_out) * 100, 2)
                        stock_list.pop(check)
                        break
        except IndexError:
            pass

        for stock in range(len(stock_list)):
            self.tableWidget_2.insertRow(stock)

            if stock % 2 == 0:
                background_color = QtGui.QColor('#444444')
            else:
                background_color = QtGui.QColor('#313131')

            list_attr = [stock_list[stock].name, stock_list[stock].price_diff, stock_list[stock].percentage]

            #  Populate table
            for i in range(len(list_attr)):
                item = QTableWidgetItem(str(list_attr[i]))
                item.setBackground(background_color)
                if i != 0:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if i == 2:
                    item.setText(f"{str(list_attr[i])}%")
                    if list_attr[i] > 0:
                        item.setForeground(QtGui.QColor('green'))
                    else:
                        item.setForeground(QtGui.QColor('red'))
                self.tableWidget_2.setItem(stock, i, item)

        tab_widgets = [self.tableWidget, self.tableWidget_2]
        for tab in tab_widgets:
            tab.verticalHeader().setVisible(False)
            header = tab.horizontalHeader()
            header.setVisible(False)
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            tab.setShowGrid(False)
            tab.setStyleSheet("font-weight:800; padding: 10 0 10 0px; color: #fff;"
                              "background-color: rgb(49, 49, 49);")

        self.show()

    def calendar_start(self):
        date = QDate(int(self.lineEdit.text()[-4:]),
                     int(self.lineEdit.text()[3:-5].replace('0', '')),
                     int(self.lineEdit.text()[:2]))
        self.calendarWidget_2.setSelectedDate(date)
        self.calendarWidget.setVisible(False)
        self.calendarWidget_2.show()
        self.calendarWidget_2.clicked.connect(lambda start: self.date_sel(True))

    def calendar_end(self):
        date = QDate(int(self.lineEdit_2.text()[-4:]),
                     int(self.lineEdit_2.text()[3:-5].replace('0', '')),
                     int(self.lineEdit_2.text()[:2]))
        self.calendarWidget.setSelectedDate(date)
        self.calendarWidget_2.setVisible(False)
        self.calendarWidget.show()
        self.calendarWidget.clicked.connect(lambda start: self.date_sel(False))

    def date_sel(self, start):
        if not start:
            date_selected = str(self.calendarWidget.selectedDate()).split('(')[1].split(')')[0]
        else:
            date_selected = str(self.calendarWidget_2.selectedDate()).split('(')[1].split(')')[0]
        date_selected = date_selected.split(', ')
        for i in range(len(date_selected)):
            if len(date_selected[i]) == 1:
                date_selected[i] = '0' + date_selected[i]
        date_selected = ''.join(date_selected)

        date_selected = date_selected[-2:] + '/' + date_selected[4:-2] + '/' + date_selected[:4]
        if start:
            self.lineEdit.setText(date_selected)
            self.calendarWidget_2.setVisible(False)
        else:
            self.lineEdit_2.setText(date_selected)
            self.calendarWidget.setVisible(False)

        date_ranges = []
        date_ranges.append(self.lineEdit.text())
        date_ranges.append(self.lineEdit_2.text())

        self.updated_range(date_ranges)

    def updated_range(self, date_selected):
        for i in range(len(date_selected)):
            date_selected[i] = datetime.strptime(date_selected[i], "%d/%m/%Y").date()
        new_list = []
        for row in list_rows:
            date = datetime.strptime(row[0], "%Y-%m-%d").date()
            if date_selected[0] <= date <= date_selected[1]:
                new_list.append(row)
        ranges = operations.dates_range(new_list)
        ranges[0], ranges[1] = ranges[1], ranges[0]
        capital = operations.find_capital(new_list)
        stock_list, interests = operations.find_closed_positions_buyorientedtry(new_list)
        self.ui_tabs(capital, stock_list, interests, ranges)


app = QApplication(sys.argv)
UIWindow = UI()
app.exec()

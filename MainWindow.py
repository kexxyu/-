# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(555, 394)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        Form.setFont(font)
        Form.setWindowOpacity(0.8)
        Form.setStyleSheet("")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 531, 75))
        self.tableWidget.setMaximumSize(QtCore.QSize(16777215, 75))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tableWidget.setFont(font)
        self.tableWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidget.setStyleSheet("QTableWidget{\n"
"color:#DCDCDC;\n"
"background:#444444;\n"
"border:1px solid #242424;\n"
"alternate-background-color:#525252;\n"
"gridline-color:#242424;\n"
"}\n"
" \n"
"QTableWidget::item:selected{\n"
"color:#DCDCDC;\n"
"background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #484848,stop:1 #383838);\n"
"}\n"
" \n"
"QTableWidget::item:hover{\n"
"background:#5B5B5B;\n"
"}\n"
"QHeaderView::section{\n"
"text-align:center;\n"
"background:#5E5E5E;\n"
"padding:3px;\n"
"margin:0px;\n"
"color:#DCDCDC;\n"
"border:1px solid #242424;\n"
"border-left-width:0;\n"
"}\n"
" \n"
"QScrollBar:vertical{\n"
"background:#484848;\n"
"padding:0px;\n"
"border-radius:6px;\n"
"max-width:12px;\n"
"}\n"
" \n"
" \n"
"QScrollBar::handle:vertical{\n"
"background:#CCCCCC;\n"
"}\n"
" \n"
"QScrollBar::handle:hover:vertical,QScrollBar::handle:pressed:vertical{\n"
"background:#A7A7A7;\n"
"}\n"
"QScrollBar::sub-page:vertical{\n"
"background:444444;\n"
"}\n"
" \n"
" \n"
"QScrollBar::add-page:vertical{\n"
"background:5B5B5B;\n"
"}\n"
" \n"
"QScrollBar::add-line:vertical{\n"
"background:none;\n"
"}\n"
"QScrollBar::sub-line:vertical{\n"
"background:none;\n"
"}")
        self.tableWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tableWidget.setMidLineWidth(-1)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setAutoScroll(False)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setTextElideMode(QtCore.Qt.ElideNone)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(15)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setKerning(True)
        item.setFont(font)
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 6, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 7, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 8, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 9, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 10, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 11, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 12, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 13, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 14, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(35)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(0)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(30)
        self.tableWidget.verticalHeader().setHighlightSections(True)
        self.tableWidget.verticalHeader().setMinimumSectionSize(0)
        self.tableWidget.verticalHeader().setSortIndicatorShown(False)
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setGeometry(QtCore.QRect(10, 160, 531, 221))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 529, 219))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.PredictedCard = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.PredictedCard.setGeometry(QtCore.QRect(10, 70, 201, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.PredictedCard.setFont(font)
        self.PredictedCard.setStyleSheet("")
        self.PredictedCard.setFrameShape(QtWidgets.QFrame.Panel)
        self.PredictedCard.setLineWidth(1)
        self.PredictedCard.setAlignment(QtCore.Qt.AlignCenter)
        self.PredictedCard.setObjectName("PredictedCard")
        self.LPlayedCard = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.LPlayedCard.setGeometry(QtCore.QRect(10, 10, 201, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.LPlayedCard.setFont(font)
        self.LPlayedCard.setStyleSheet("")
        self.LPlayedCard.setFrameShape(QtWidgets.QFrame.Panel)
        self.LPlayedCard.setLineWidth(1)
        self.LPlayedCard.setAlignment(QtCore.Qt.AlignCenter)
        self.LPlayedCard.setObjectName("LPlayedCard")
        self.RPlayedCard = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.RPlayedCard.setGeometry(QtCore.QRect(320, 10, 201, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.RPlayedCard.setFont(font)
        self.RPlayedCard.setStyleSheet("")
        self.RPlayedCard.setFrameShape(QtWidgets.QFrame.Panel)
        self.RPlayedCard.setLineWidth(1)
        self.RPlayedCard.setAlignment(QtCore.Qt.AlignCenter)
        self.RPlayedCard.setObjectName("RPlayedCard")
        self.ThreeLandlordCards = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.ThreeLandlordCards.setGeometry(QtCore.QRect(220, 10, 91, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.ThreeLandlordCards.setFont(font)
        self.ThreeLandlordCards.setStyleSheet("")
        self.ThreeLandlordCards.setFrameShape(QtWidgets.QFrame.Panel)
        self.ThreeLandlordCards.setLineWidth(1)
        self.ThreeLandlordCards.setAlignment(QtCore.Qt.AlignCenter)
        self.ThreeLandlordCards.setObjectName("ThreeLandlordCards")
        self.splitter = QtWidgets.QSplitter(self.scrollAreaWidgetContents)
        self.splitter.setGeometry(QtCore.QRect(320, 170, 201, 41))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.HandButton = QtWidgets.QPushButton(self.splitter)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.HandButton.setFont(font)
        self.HandButton.setObjectName("HandButton")
        self.AutoButton = QtWidgets.QPushButton(self.splitter)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.AutoButton.setFont(font)
        self.AutoButton.setObjectName("AutoButton")
        self.StopButton = QtWidgets.QPushButton(self.splitter)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.StopButton.setFont(font)
        self.StopButton.setObjectName("StopButton")
        self.WinRate = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.WinRate.setGeometry(QtCore.QRect(220, 70, 301, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.WinRate.setFont(font)
        self.WinRate.setStyleSheet("")
        self.WinRate.setFrameShape(QtWidgets.QFrame.Panel)
        self.WinRate.setLineWidth(1)
        self.WinRate.setAlignment(QtCore.Qt.AlignCenter)
        self.WinRate.setObjectName("WinRate")
        self.scrollArea_11 = QtWidgets.QScrollArea(self.scrollAreaWidgetContents)
        self.scrollArea_11.setGeometry(QtCore.QRect(220, 120, 91, 91))
        self.scrollArea_11.setWidgetResizable(True)
        self.scrollArea_11.setObjectName("scrollArea_11")
        self.scrollAreaWidgetContents_11 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_11.setGeometry(QtCore.QRect(0, 0, 89, 89))
        self.scrollAreaWidgetContents_11.setObjectName("scrollAreaWidgetContents_11")
        self.BidWinrate = QtWidgets.QLabel(self.scrollAreaWidgetContents_11)
        self.BidWinrate.setGeometry(QtCore.QRect(10, 0, 81, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.BidWinrate.setFont(font)
        self.BidWinrate.setObjectName("BidWinrate")
        self.suggest_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_11)
        self.suggest_1.setGeometry(QtCore.QRect(10, 30, 81, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.suggest_1.setFont(font)
        self.suggest_1.setObjectName("suggest_1")
        self.suggest_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_11)
        self.suggest_2.setGeometry(QtCore.QRect(10, 60, 81, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.suggest_2.setFont(font)
        self.suggest_2.setObjectName("suggest_2")
        self.scrollArea_11.setWidget(self.scrollAreaWidgetContents_11)
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label.setGeometry(QtCore.QRect(320, 120, 201, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("")
        self.label.setFrameShape(QtWidgets.QFrame.Panel)
        self.label.setLineWidth(1)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.scrollArea_4 = QtWidgets.QScrollArea(self.scrollAreaWidgetContents)
        self.scrollArea_4.setGeometry(QtCore.QRect(10, 120, 201, 91))
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setObjectName("scrollArea_4")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 199, 89))
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.code_label = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.code_label.setGeometry(QtCore.QRect(0, 0, 101, 91))
        self.code_label.setStyleSheet("image: url(:/pics/code.png);")
        self.code_label.setText("")
        self.code_label.setObjectName("code_label")
        self.label_5 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.label_5.setGeometry(QtCore.QRect(100, 10, 41, 71))
        font = QtGui.QFont()
        font.setFamily("华文琥珀")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.label_4.setGeometry(QtCore.QRect(140, 30, 51, 31))
        font = QtGui.QFont()
        font.setFamily("华文新魏")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea_5 = QtWidgets.QScrollArea(Form)
        self.scrollArea_5.setGeometry(QtCore.QRect(10, 90, 531, 61))
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollArea_5.setObjectName("scrollArea_5")
        self.scrollAreaWidgetContents_5 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_5.setGeometry(QtCore.QRect(0, 0, 529, 59))
        self.scrollAreaWidgetContents_5.setObjectName("scrollAreaWidgetContents_5")
        self.bid_label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.bid_label_2.setGeometry(QtCore.QRect(320, 0, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.bid_label_2.setFont(font)
        self.bid_label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.bid_label_2.setObjectName("bid_label_2")
        self.bid_lineEdit_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.bid_lineEdit_2.setGeometry(QtCore.QRect(220, 30, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.bid_lineEdit_2.setFont(font)
        self.bid_lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.bid_lineEdit_2.setObjectName("bid_lineEdit_2")
        self.bid_label_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.bid_label_4.setGeometry(QtCore.QRect(440, 0, 61, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.bid_label_4.setFont(font)
        self.bid_label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.bid_label_4.setObjectName("bid_label_4")
        self.bid_label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.bid_label_3.setGeometry(QtCore.QRect(210, 0, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.bid_label_3.setFont(font)
        self.bid_label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.bid_label_3.setObjectName("bid_label_3")
        self.bid_lineEdit_3 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.bid_lineEdit_3.setGeometry(QtCore.QRect(330, 30, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.bid_lineEdit_3.setFont(font)
        self.bid_lineEdit_3.setAlignment(QtCore.Qt.AlignCenter)
        self.bid_lineEdit_3.setObjectName("bid_lineEdit_3")
        self.bid_label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.bid_label_1.setGeometry(QtCore.QRect(110, 0, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.bid_label_1.setFont(font)
        self.bid_label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.bid_label_1.setObjectName("bid_label_1")
        self.bid_lineEdit_4 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.bid_lineEdit_4.setGeometry(QtCore.QRect(440, 30, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.bid_lineEdit_4.setFont(font)
        self.bid_lineEdit_4.setAlignment(QtCore.Qt.AlignCenter)
        self.bid_lineEdit_4.setObjectName("bid_lineEdit_4")
        self.bid_lineEdit_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.bid_lineEdit_1.setGeometry(QtCore.QRect(120, 30, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.bid_lineEdit_1.setFont(font)
        self.bid_lineEdit_1.setAlignment(QtCore.Qt.AlignCenter)
        self.bid_lineEdit_1.setObjectName("bid_lineEdit_1")
        self.ResetButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents_5)
        self.ResetButton.setGeometry(QtCore.QRect(10, 10, 71, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.ResetButton.setFont(font)
        self.ResetButton.setObjectName("ResetButton")
        self.scrollArea_5.setWidget(self.scrollAreaWidgetContents_5)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Hi"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "大"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "小"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "2"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "A"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "K"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Q"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Form", "J"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Form", "10"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("Form", "9"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("Form", "8"))
        item = self.tableWidget.horizontalHeaderItem(10)
        item.setText(_translate("Form", "7"))
        item = self.tableWidget.horizontalHeaderItem(11)
        item.setText(_translate("Form", "6"))
        item = self.tableWidget.horizontalHeaderItem(12)
        item.setText(_translate("Form", "5"))
        item = self.tableWidget.horizontalHeaderItem(13)
        item.setText(_translate("Form", "4"))
        item = self.tableWidget.horizontalHeaderItem(14)
        item.setText(_translate("Form", "3"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("Form", "0"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("Form", "0"))
        item = self.tableWidget.item(0, 2)
        item.setText(_translate("Form", "0"))
        item = self.tableWidget.item(0, 3)
        item.setText(_translate("Form", "0"))
        item = self.tableWidget.item(0, 4)
        item.setText(_translate("Form", "0"))
        item = self.tableWidget.item(0, 5)
        item.setText(_translate("Form", "0"))
        item = self.tableWidget.item(0, 6)
        item.setText(_translate("Form", "0"))
        item = self.tableWidget.item(0, 7)
        item.setText(_translate("Form", "0"))
        item = self.tableWidget.item(0, 8)
        item.setText(_translate("Form", "0"))
        item = self.tableWidget.item(0, 9)
        item.setText(_translate("Form", "0"))
        item = self.tableWidget.item(0, 10)
        item.setText(_translate("Form", "0"))
        item = self.tableWidget.item(0, 11)
        item.setText(_translate("Form", "0"))
        item = self.tableWidget.item(0, 12)
        item.setText(_translate("Form", "0"))
        item = self.tableWidget.item(0, 13)
        item.setText(_translate("Form", "0"))
        item = self.tableWidget.item(0, 14)
        item.setText(_translate("Form", "0"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.PredictedCard.setText(_translate("Form", "AI出牌区域"))
        self.LPlayedCard.setText(_translate("Form", "上家出牌区域"))
        self.RPlayedCard.setText(_translate("Form", "下家出牌区域"))
        self.ThreeLandlordCards.setText(_translate("Form", "底牌"))
        self.HandButton.setText(_translate("Form", "手动"))
        self.AutoButton.setText(_translate("Form", "自动"))
        self.StopButton.setText(_translate("Form", "停止"))
        self.WinRate.setText(_translate("Form", "评分"))
        self.BidWinrate.setText(_translate("Form", "得分："))
        self.suggest_1.setText(_translate("Form", "建议："))
        self.suggest_2.setText(_translate("Form", "建议："))
        self.label.setText(_translate("Form", "游戏状态"))
        self.label_5.setText(_translate("Form", "开 扫\n"
"源 码\n"
"不 求\n"
"易 赞\n"
""))
        self.label_4.setText(_translate("Form", "马  云"))
        self.bid_label_2.setText(_translate("Form", "超级加倍"))
        self.bid_label_4.setText(_translate("Form", "明牌"))
        self.bid_label_3.setText(_translate("Form", "抢地主  加倍"))
        self.bid_label_1.setText(_translate("Form", "叫地主"))
        self.ResetButton.setText(_translate("Form", "恢复默认"))
import picture_rc

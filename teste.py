from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtPrintSupport import*
import sys
import sqlite3
import time
import os

class InsertDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(InsertDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Registrar")

        self.setWindowTitle("Add cartão")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.setWindowTitle("dados do cartão")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.QBtn.clicked.connect(self.cartao)

        layout = QVBoxLayout()

        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("Nome")
        layout.addWidget(self.nameinput)

        self.branchinput = QComboBox()
        self.branchinput.addItem("Banco do Brasil")
        self.branchinput.addItem("Santander")
        self.branchinput.addItem("Bradesco")
        self.branchinput.addItem("Itau")
        self.branchinput.addItem("Nubank")
        layout.addWidget(self.branchinput)

        self.dateinput = QLineEdit()
        self.dateinput.setPlaceholderText("Validade (DD/MM/AAAA)")
        layout.addWidget(self.dateinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def cartao(self):
        name= ""
        branch=""
        date=""

        name= self.nameinput.text()
        branch= self.branchinput.itemText(self.branchinput.currentIndex())
        date= self.dateinput.text()

class SearchDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Pesquisar")

        self.setWindowTitle("Pesquisar cartão")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        self.QBtn.clicked.connect(self.searchcartao)

        layout = QVBoxLayout()

        self.searchinput = QLineEdit()
        self.searchinput.setPlaceholderText("Validade (DD/MM/AAAA)")
        layout.addWidget(self.searchinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def searchcartao(self):
        searchval = ""
        searchval = self.searchinput.text()

class DeleteDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(DeleteDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Deletar")

        self.setWindowTitle("Deletar cartão")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        self.QBtn.clicked.connect(self.deletecartao)

        layout = QVBoxLayout()

        self.deleteinput = QLineEdit()
        self.deleteinput.setPlaceholderText("Nome")
        layout.addWidget(self.deleteinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deletecartao(self):
        deleterow = ""
        deleterow = self.deleteinput.text()


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon('icon/pagamento-com-cartao-de-credito.png'))

        file_menu = self.menuBar().addMenu("&File")
        self.setWindowTitle("Cadastro de Cartões")
        self.setMinimumSize(800,600)

        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)

        self.tableWidget.setHorizontalHeaderLabels(("ID", "Nome", "Nro do cartão", "Validade"))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        btn_ac_adduser = QAction(QIcon("icon/adicionar.svg"), "Adicionar Cartão", self)
        btn_ac_adduser.triggered.connect(self.insert)
        btn_ac_adduser.setStatusTip("Adicionar")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_view = QAction(QIcon("icon/olho.png"), "Visualizar todos os Cartões", self)
        btn_ac_view.setStatusTip("Visualizar")
        toolbar.addAction(btn_ac_view)

        btn_ac_search = QAction(QIcon("icon/local-na-rede-internet.png"), "Pesquisar Cartão", self)
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Pesquisar")
        toolbar.addAction(btn_ac_search)

        btn_ac_delete = QAction(QIcon("icon/lixo.png"), "Deletar Cartão", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Deletar")
        toolbar.addAction(btn_ac_delete)

    def insert(self):
        dlg = InsertDialog()
        dlg.exec_()


    def search(self):
        dlg = SearchDialog()
        dlg.exec_()

    def delete(self):
        dlg = DeleteDialog()
        dlg.exec_()

app = QApplication(sys.argv)
if(QDialog.Accepted == True):
    window = MainWindow()
    window.show()
sys.exit(app.exec_())
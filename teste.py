# Caroline F. Pettarelli
# Python test

# run the following commands to up the sistem using PyQt5:

# pip install pyqt5
# pip install pyQtwebEngine
# python3 teste.py

# initially the SQLite database was used and in the research class we used the api developed

from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtPrintSupport import*
import sys
import sqlite3
import time
import os
import json, requests

# setting insertion options
class InsertDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(InsertDialog, self).__init__(*args, **kwargs)

        # button to confirm insert new records
        self.QBtn = QPushButton()  
        self.QBtn.setText("Registrar")

        # title and window option
        self.setWindowTitle("Add cartão")
        self.setFixedWidth(300) #setting menu window size
        self.setFixedHeight(300)

        self.setWindowTitle("dados do cartão")
        self.setFixedWidth(300) #setting window size for adding cards
        self.setFixedHeight(300)

        self.QBtn.clicked.connect(self.card) # when clicked call function 'card'

        layout = QVBoxLayout()

        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("Nome") # first input text option
        layout.addWidget(self.nameinput)

        self.branchinput = QComboBox() # need to select a option
        self.branchinput.addItem("Banco do Brasil")
        self.branchinput.addItem("Santander")
        self.branchinput.addItem("Bradesco")
        self.branchinput.addItem("Itau")
        self.branchinput.addItem("Nubank")
        layout.addWidget(self.branchinput)

        self.dateinput = QLineEdit()
        self.dateinput.setPlaceholderText("Validade (MM-AA)")  # second input text option
        layout.addWidget(self.dateinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def card(self):
        name= ""
        branch=""
        date=""

        name= self.nameinput.text()
        branch= self.branchinput.itemText(self.branchinput.currentIndex())
        date= self.dateinput.text()

# setting search options
class SearchDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchDialog, self).__init__(*args, **kwargs)

        # button to confirm search records
        self.QBtn = QPushButton() 
        self.QBtn.setText("Pesquisar")

        # title and window option
        self.setWindowTitle("Pesquisar cartão")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        self.QBtn.clicked.connect(self.searchcard) # when clicked call function 'searchcard'

        layout = QVBoxLayout()

        self.searchinput = QLineEdit()
        self.searchinput.setPlaceholderText("Validade (MM-AA)")  # serach by validity data
        layout.addWidget(self.searchinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def searchcard(self):
        searchval = ""
        searchval = self.searchinput.text()

        try:
            # other way to do, but don't using the api

            # self.conn = sqlite3.connect("database.db") #criando o banco de dados
            # self.c = self.conn.cursor() #iniciando conexão
            # result = self.c.execute("SELECT * from cart WHERE date ="+str(searchval))
            # row = result.fetchmany()
            # searchresult = "ID: "+str(row[0])+'\n'+"Nome: "+str(row[1])+'\n'+"Banco: "+str(row[2])+'\n'+"Validade: "+str(row[3])
            # QMessageBox.information(QMessageBox(),'Pesquisa realizada com sucesso',searchresult)
            # self.conn.commit()
            # self.c.close() #fechando conexão
            # self.conn.close()

            # need to up the api in localhost
            response = requests.get("http://127.0.0.1:5000/cards/"+str(searchval))
            row = response.fetchmany()
            searchresult = "ID: "+str(row[0])+'\n'+"Nome: "+str(row[1])+'\n'+"Banco: "+str(row[2])+'\n'+"Validade: "+str(row[3])  # show the results in a window
            QMessageBox.information(QMessageBox(),'Pesquisa realizada com sucesso',searchresult)

        except Exception:
            QMessageBox.warning(QMessageBox(), 'caroline.pettarelli@usp.br', 'Cartão não encontrado') # error menssage

# setting deletion options
class DeleteDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(DeleteDialog, self).__init__(*args, **kwargs)

        # button to confirm delete records
        self.QBtn = QPushButton()
        self.QBtn.setText("Deletar")

        # title and window option
        self.setWindowTitle("Deletar cartão")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        self.QBtn.clicked.connect(self.deletecard) # when clicked call function 'deletecard'

        layout = QVBoxLayout()

        self.deleteinput = QLineEdit()
        self.deleteinput.setPlaceholderText("Nome")
        layout.addWidget(self.deleteinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deletecard(self):
        deleterow = ""
        deleterow = self.deleteinput.text()

# setting main window options - menu
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon('icon/pagamento-com-card-de-credito.png'))

        self.conn = sqlite3.connect("database.db") #criando o banco de dados
        self.c = self.conn.cursor() #iniciando conexão
        self.c.execute("CREATE TABLE IF NOT EXISTS cart(roll INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, branch TEXT, date TEXT)")
        self.c.close() #fechando conexão

        file_menu = self.menuBar().addMenu("&File")
        self.setWindowTitle("Cadastro de Cartões")
        self.setMinimumSize(800,600)

        # setting viewing table options for all cards
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

        self.tableWidget.setHorizontalHeaderLabels(("ID", "Nome do Cliente", "Nro do cartão", "Validade")) # name of the columns

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # setting a status Bar
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        btn_ac_addcard = QAction(QIcon("icon/adicionar.svg"), "Adicionar Cartão", self) # insserting a image to option add card
        btn_ac_addcard.triggered.connect(self.insert) #linking with insert function
        btn_ac_addcard.setStatusTip("Adicionar")
        toolbar.addAction(btn_ac_addcard) # adding option on toolbar

        btn_ac_view = QAction(QIcon("icon/olho.png"), "Visualizar todos os Cartões", self) # insserting a image to option view cards
        btn_ac_view.setStatusTip("Visualizar")
        toolbar.addAction(btn_ac_view) # adding option on toolbar

        btn_ac_search = QAction(QIcon("icon/local-na-rede-internet.png"), "Pesquisar Cartão", self) # insserting a image to option search card
        btn_ac_search.triggered.connect(self.search) #linking with search function
        btn_ac_search.setStatusTip("Pesquisar")
        toolbar.addAction(btn_ac_search) # adding option on toolbar

        btn_ac_delete = QAction(QIcon("icon/lixo.png"), "Deletar Cartão", self) # insserting a image to option delete card
        btn_ac_delete.triggered.connect(self.delete) #linking with delete function
        btn_ac_delete.setStatusTip("Deletar")
        toolbar.addAction(btn_ac_delete) # adding option on toolbar

    def loaddata(self): # function to load database data - need to switch to api
        self.connection = sqlite3.connect("database.db")
        query = "SELECT * FROM cart"
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number,row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.tableWidget.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        self.connection.close()
        

    def insert(self): # call the class to insert options
        dlg = InsertDialog()
        dlg.exec_()


    def search(self): # call the class to search options
        dlg = SearchDialog()
        dlg.exec_()

    def delete(self): # call the class to delete options
        dlg = DeleteDialog()
        dlg.exec_()

app = QApplication(sys.argv)
if(QDialog.Accepted == True):
    window = MainWindow()
    window.show()
    window.loaddata()
sys.exit(app.exec_())
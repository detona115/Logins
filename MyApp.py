'''
Created on 10 de mar de 2019

@author: ANDY
'''
import sqlite3
from sqlite3 import Error
from PyQt5.QtWidgets import QApplication, QStatusBar, QMainWindow, qApp, QStatusBar,\
    QTableWidgetItem, QSizePolicy, QHBoxLayout
from loginsPrincipal import *

class MyApp(QMainWindow):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #self.ui.actionSair.triggered.connect(qApp.quit) 
        
        query = "CREATE TABLE IF NOT EXISTS Logins (Site_Name varchar(150),\
        Username varchar(75), Password varchar(75), Link varchar(200), Inscription_Date date,\
        Id INT NOT NULL PRIMARY KEY AUTOINCREMENT);"
        
        try:
            conn = sqlite3.connect("database.db")
            with conn:
                cur = conn.cursor()
                cur.execute(query)
                self.statusBar().showMessage("Database connection successfull!", 2000)
        
        except Error as e:
            self.statusBar().showMessage("ocorreu o erro "+str(e)+" na criação da base de dados", 2000)
        
        finally:
            conn.close()
        
        self.ui.ButtonSave.clicked.connect(self.salvar)
        
        self.ui.ButtonLogins.clicked.connect(self.allLogins)        
        
        self.ui.ButtonSubmit.clicked.connect(self.submit)
        
        self.ui.ButtonClear.clicked.connect(self.clear)
        
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
                
        self.date = QtCore.QDate.currentDate().toString('dd-MM-yyyy')
        
        self.ui.lineEditLink.setFocus()
        
        #self.ui.centralwidget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        
        self.show()
        
    def salvar(self):
        """ Esta função salva dados novos na base de dados """
        
        if self.ui.lineEditLink.text() == "" or self.ui.lineEditUsername.text() == "" or self.ui.lineEditPassword.text() == "" or self.ui.lineEditSiteName.text() == "":
                
            self.statusBar().showMessage("Datas incomplete!", 2000)
            self.statusBar().setStyleSheet("color: red")
            
            if self.ui.lineEditLink.text() == "":
                self.ui.lineEditLink.setStyleSheet("border: 2px solid red;\
                                                    border-radius: 10px;\
                                                    padding: 0 8px;\
                                                    selection-background-color: darkgray;")
            else:
                self.ui.lineEditLink.setStyleSheet("border: 2px solid gray;\
                                                    border-radius: 10px;\
                                                    padding: 0 8px;\
                                                    selection-background-color: darkgray;")
                
            if self.ui.lineEditUsername.text() == "":
                self.ui.lineEditUsername.setStyleSheet("border: 2px solid red;\
                                                    border-radius: 10px;\
                                                    padding: 0 8px;\
                                                    selection-background-color: darkgray;")
            else:
                self.ui.lineEditUsername.setStyleSheet("border: 2px solid gray;\
                                                    border-radius: 10px;\
                                                    padding: 0 8px;\
                                                    selection-background-color: darkgray;")
                
            if self.ui.lineEditPassword.text() == "":
                self.ui.lineEditPassword.setStyleSheet("border: 2px solid red;\
                                                    border-radius: 10px;\
                                                    padding: 0 8px;\
                                                    selection-background-color: darkgray;")
            else:
                self.ui.lineEditPassword.setStyleSheet("border: 2px solid gray;\
                                                    border-radius: 10px;\
                                                    padding: 0 8px;\
                                                    selection-background-color: darkgray;")
                
            if self.ui.lineEditSiteName.text() == "":
                self.ui.lineEditSiteName.setStyleSheet("border: 2px solid red;\
                                                    border-radius: 10px;\
                                                    padding: 0 8px;\
                                                    selection-background-color: darkgray;")
            else:
                self.ui.lineEditSiteName.setStyleSheet("border: 2px solid gray;\
                                                    border-radius: 10px;\
                                                    padding: 0 8px;\
                                                    selection-background-color: darkgray;")
        else:                
                
            val = (self.ui.lineEditSiteName.text(), self.ui.lineEditUsername.text(), \
                   self.ui.lineEditPassword.text(), self.ui.lineEditLink.text(), self.date )
            sql = "INSERT INTO Logins (Site_Name , Username, Password, Link, Inscription_Date) VALUES\
             ('"+val[0]+"', '"+val[1]+"', '"+val[2]+"', '"+val[3]+"', '"+val[4]+"')"
             
            try:
                conn = sqlite3.connect("database.db")
                self.statusBar().setStyleSheet("color: black")
                self.statusBar().showMessage("connection to database ok!", 2000)
                
                with conn:
                    cur = conn.cursor()
                    cur.execute(sql)
                    conn.commit()
                    self.statusBar().setStyleSheet("color: green")
                    self.statusBar().showMessage("New Logins saved successfully!", 2000)                    
                    
            except Error as e:
                self.statusBar().setStyleSheet("color: red")
                self.statusBar().showMessage("Can´t insert data (you probably already have login in this link)!", 5000)
                print("ocorreu o erro: "+str(e)+" na inserção na base de dados")
                
            finally:
                self.ui.lineEditLink.clear()
                self.ui.lineEditUsername.clear()
                self.ui.lineEditPassword.clear()
                self.ui.lineEditSiteName.clear()
                conn.close()
                
    def clear(self):
        
        if self.ui.tableWidget.rowCount() == 0:
            self.statusBar().setStyleSheet("color: red")
            self.statusBar().showMessage("There is nothing to be cleared!", 2000)
        else:
            self.ui.tableWidget.clearContents()
            self.ui.tableWidget.setRowCount(0)
    
    def allLogins(self):
        """ Esta função retorna todos os logins da base de dados """
        
        sql = "SELECT * FROM Logins"
        try:
            conn = sqlite3.connect("database.db")
                        
            with conn:
                cur = conn.cursor()
                cur.execute(sql)
                rows = cur.fetchall()
                self.ui.tableWidget.setRowCount(0)
                for rowNo, x in enumerate(rows):
                    self.ui.tableWidget.insertRow(rowNo)
                    
                    for col, data in enumerate(x):
                        
                        oneColumn = QTableWidgetItem(str(data))
                        
                        self.ui.tableWidget.setItem(rowNo, col, oneColumn)
        except Error as e:
            print("erro em carregar : "+e)
            
        finally:
            conn.close()
            
    def submit(self):
        """ Esta função busca um determinado login dentro da base de dado """
        
        sql = " SELECT * FROM Logins WHERE Site_Name LIKE '"+self.ui.lineEditSearch.text()+"%'"  
        
        if self.ui.lineEditSearch.text() == "":            
            self.statusBar().setStyleSheet("color: red")
            self.statusBar().showMessage("Nothing to be searched", 2000)  
            
        else:        
            try:
                conn = sqlite3.connect("database.db")
                                
                with conn:
                    cur = conn.cursor()
                    cur.execute(sql)
                    rows = cur.fetchall()
                    
                    if len(rows) == 0:                        
                        self.statusBar().setStyleSheet("color: red")
                        self.statusBar().showMessage("Name site not found!", 2000)
                        
                    else:
                        self.ui.tableWidget.setRowCount(0)
                        for rowNo, x in enumerate(rows):
                            self.ui.tableWidget.insertRow(rowNo)
                            
                            for col, data in enumerate(x):
                                
                                oneColumn = QTableWidgetItem(str(data))
                                
                                self.ui.tableWidget.setItem(rowNo, col, oneColumn)
                        self.statusBar().setStyleSheet("color: green")
                        self.statusBar().showMessage("Login(s) found!", 2000)
            except Error as e:
                print("erro em carregar submit : "+e)
                
            finally:
                conn.close()
        

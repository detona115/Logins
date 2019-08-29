'''
Created on 26 de ago de 2019

@author: ANDY
'''

import sys 
from MyApp import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyApp()
    w.show()
    sys.exit(app.exec_())
from PyQt5 import QtWidgets
from GUI.FacadeGui import Facade

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Facade()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

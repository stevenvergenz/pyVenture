import sys

from PyQt4 import QtGui
from mainwindow import MainWindow

def main():

	app = QtGui.QApplication(sys.argv)
	window = MainWindow()
	window.show()

	app.exec_()


if __name__ == '__main__':
	main()

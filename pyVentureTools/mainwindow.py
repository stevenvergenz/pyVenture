from window import Ui_MainWindow
from PyQt4.QtGui import QMainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

	def __init__(self):

		QMainWindow.__init__(self)
		self.setupUi(self)


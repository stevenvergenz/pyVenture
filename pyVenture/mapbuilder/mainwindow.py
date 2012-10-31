from window import Ui_MainWindow
from PyQt4 import QtGui
from common import types
from common import events

import json
import gzip


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

	def __init__(self):

		QtGui.QMainWindow.__init__(self)
		self.setupUi(self)
		self.mainSplitter.setSizes([400,200])

		# connect menu items
		self.actionE_xit.triggered.connect( self.close )

		self.load('sample.pvm')

	def load(self, filename):

		dump = {}
		if filename[-2:] == 'gz':
			with gzip.open(filename, 'r') as file:
				try:
					tempstr = file.read()
					dump = json.loads(tempstr)
				except:
					print 'There was a problem loading', filename

		else:
			with open(filename, 'r') as file:
				try:
					tempstr = file.read()
					dump = json.loads(tempstr)
				except:
					print 'There was a problem loading', filename

		# populate tree
		world = types.World.deserialize(dump)
		print 'Parse successful'
			

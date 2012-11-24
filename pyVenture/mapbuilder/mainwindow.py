from window import Ui_MainWindow
from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from common import types
from common import events

import json
import gzip


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

	def __init__(self):

		QtGui.QMainWindow.__init__(self)
		self.setupUi(self)
		self.mainSplitter.setSizes([400,200])
		self.filename = ''

		# connect menu items
		self.actionE_xit.triggered.connect( self.close )
		self.hierarchyTree.itemSelectionChanged.connect( self.updatePropertyTable )
		self.actionOpen.triggered.connect( self.loadFileDialog )
		self.propertyTable.cellChanged.connect( self.editProperty )
		self.actionSave.triggered.connect( self.saveFileDialog )
		self.actionSave_As.triggered.connect( self.saveAsFileDialog )
		#self.load('sample.pvm')


	def loadFileDialog(self):

		filename = QtGui.QFileDialog.getOpenFileName(parent = self, caption = 'Open Map File',
			filter = 'Map files (*.pvm *.pvm.gz)')
		if filename != '':
			self.load(filename)
			self.filename = str(filename)


	def saveFileDialog(self):
		
		if self.filename == '':
			self.saveAsFileDialog()
			return

		if self.filename[-2:] == 'gz':
			outfile = gzip.open(self.filename, 'w')
		else:
			outfile = open(self.filename, 'w')

		#try:
		outfile.write( json.dumps(self.world.serialize(), indent=4) )
		print 'Dump to file',self.filename,'successful'
		#except:
		print 'Failed to convert world to JSON, save failed.'

		outfile.close()


	def saveAsFileDialog(self):

		filename = QtGui.QFileDialog.getSaveFileName(parent = self, caption = 'Save Map File',
			filter = 'Compressed map files (*.pvm.gz);;Map files (*.pvm)')
		if filename != '':
			self.filename = str(filename)
			self.saveFileDialog()


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
		self.world = types.World.deserialize(dump)
		print 'Parse successful'

		self.hierarchyTree.clear()

		for key, area in self.world.areas.items():
			areaItem = QtGui.QTreeWidgetItem(self.hierarchyTree, [ area.id, 'Area' ])
			areaItem.ventureObject = area
			self.hierarchyTree.addTopLevelItem(areaItem)

			for feature in area.features:
				featureItem = QtGui.QTreeWidgetItem(areaItem, [feature.name, 'Feature'])
				featureItem.ventureObject = feature
				areaItem.addChild(featureItem)

				for action in feature.actions:
					actionItem = QtGui.QTreeWidgetItem(featureItem, [action.description, 'Action'])
					actionItem.ventureObject = action
					featureItem.addChild(actionItem)

					for event in action.events:
						eventItem = QtGui.QTreeWidgetItem(actionItem, [event.type, 'Event'])
						eventItem.ventureObject = event
						actionItem.addChild(eventItem)

				featureItem.sortChildren(0, Qt.AscendingOrder)
			areaItem.sortChildren(0, Qt.AscendingOrder)
		self.hierarchyTree.sortItems(0, Qt.AscendingOrder)


	def updatePropertyTable(self):

		self.propertyTable.clear()
		self.propertyTable.setHorizontalHeaderLabels( ['Property', 'Value'] )
		treeItem = self.hierarchyTree.selectedItems()[0]
		self.propertyTable.ventureObject = treeItem.ventureObject

		if treeItem.text(1) == 'Area':

			self.propertyTable.setRowCount(3)

			self.propertyTable.setItem( 0,0, QtGui.QTableWidgetItem('id') )
			self.propertyTable.setItem( 0,1, QtGui.QTableWidgetItem( treeItem.ventureObject.id ) )

			self.propertyTable.setItem( 1,0, QtGui.QTableWidgetItem('name') )
			self.propertyTable.setItem( 1,1, QtGui.QTableWidgetItem( treeItem.ventureObject.name ) )

			self.propertyTable.setItem( 2,0, QtGui.QTableWidgetItem('entranceText') )
			self.propertyTable.setItem( 2,1, QtGui.QTableWidgetItem( treeItem.ventureObject.entranceText ) )

		elif treeItem.text(1) == 'Feature':
			
			self.propertyTable.setRowCount(2)

			self.propertyTable.setItem( 0,0, QtGui.QTableWidgetItem('name') )
			self.propertyTable.setItem( 0,1, QtGui.QTableWidgetItem( treeItem.ventureObject.name ) )

			self.propertyTable.setItem( 1,0, QtGui.QTableWidgetItem('description') )
			self.propertyTable.setItem( 1,1, QtGui.QTableWidgetItem( treeItem.ventureObject.description ) )

		elif treeItem.text(1) == 'Action':

			self.propertyTable.setRowCount(1)

			self.propertyTable.setItem( 0,0, QtGui.QTableWidgetItem('description') )
			self.propertyTable.setItem( 0,1, QtGui.QTableWidgetItem( treeItem.ventureObject.description ) )

		else:

			self.propertyTable.setRowCount( len(treeItem.ventureObject.properties) )

			i = 0
			for name, value in treeItem.ventureObject.properties.items():
				self.propertyTable.setItem( i,0, QtGui.QTableWidgetItem(name) )
				self.propertyTable.setItem( i,1, QtGui.QTableWidgetItem(value) )


		# set all cells in col 0 read-only
		for index in range(0, self.propertyTable.rowCount()):
			item = self.propertyTable.item(index, 0).setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)


	def editProperty(self, row, column):

		if( column != 1 ): return

		key = self.propertyTable.item(row,0).text()
		value = self.propertyTable.item(row,column).text()
		setattr( self.propertyTable.ventureObject, str(key), value)
		print 'The value of',key,'is now',value



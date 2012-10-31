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

		# connect menu items
		self.actionE_xit.triggered.connect( self.close )
		self.hierarchyTree.itemSelectionChanged.connect( self.updatePropertyTable )

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
		self.world = types.World.deserialize(dump)
		print 'Parse successful'

		self.hierarchyTree.clear()

		for key, area in self.world.areas.items():
			areaItem = QtGui.QTreeWidgetItem(self.hierarchyTree, [ area.id, 'Area' ])
			self.hierarchyTree.addTopLevelItem(areaItem)

			for feature in area.features:
				featureItem = QtGui.QTreeWidgetItem(areaItem, [feature.name, 'Feature'])
				areaItem.addChild(featureItem)

				for action in feature.actions:
					actionItem = QtGui.QTreeWidgetItem(featureItem, [action.description, 'Action'])
					featureItem.addChild(actionItem)

					for event in action.events:
						eventItem = QtGui.QTreeWidgetItem(actionItem, [event.type, event.type])
						actionItem.addChild(eventItem)

				featureItem.sortChildren(0, Qt.AscendingOrder)
			areaItem.sortChildren(0, Qt.AscendingOrder)
		self.hierarchyTree.sortItems(0, Qt.AscendingOrder)


	def updatePropertyTable(self):

		self.propertyTable.clear()
		self.propertyTable.setHorizontalHeaderLabels( ['Property', 'Value'] )
		treeItem = self.hierarchyTree.selectedItems()[0]

		if treeItem.text(1) == 'Area':

			item = self.world.areas[treeItem.text(0).__str__()]
			self.propertyTable.setRowCount(3)

			self.propertyTable.setItem( 0,0, QtGui.QTableWidgetItem('id') )
			self.propertyTable.setItem( 0,1, QtGui.QTableWidgetItem( item.id ) )

			self.propertyTable.setItem( 1,0, QtGui.QTableWidgetItem('name') )
			self.propertyTable.setItem( 1,1, QtGui.QTableWidgetItem( item.name ) )

			self.propertyTable.setItem( 2,0, QtGui.QTableWidgetItem('entranceText') )
			self.propertyTable.setItem( 2,1, QtGui.QTableWidgetItem( item.entranceText ) )

		elif treeItem.text(1) == 'Feature':
			
			parentTreeArea = treeItem.parent()
			parentArea = self.world.areas[ treeItem.parent().text(0).__str__() ]
			item = parentArea.features[ parentTreeArea.indexOfChild(treeItem) ]

			self.propertyTable.setRowCount(2)

			self.propertyTable.setItem( 0,0, QtGui.QTableWidgetItem('name') )
			self.propertyTable.setItem( 0,1, QtGui.QTableWidgetItem( item.name ) )

			self.propertyTable.setItem( 1,0, QtGui.QTableWidgetItem('description') )
			self.propertyTable.setItem( 1,1, QtGui.QTableWidgetItem( item.description ) )


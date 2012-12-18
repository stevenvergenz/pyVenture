from window import Ui_MainWindow
from PyQt4 import QtGui, QtCore, QtSvg
from PyQt4.QtCore import Qt

from common import types
from common import events

import json
import gzip
import pydot


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

	def __init__(self):

		QtGui.QMainWindow.__init__(self)
		self.setupUi(self)
		self.mainSplitter.setSizes([400,200])

		self.filename = ''
		self.world = types.World()
		self.oldWorld = types.World()

		self.graphicsScene = QtGui.QGraphicsScene()
		self.graphicsView.setScene( self.graphicsScene )

		# connect toolbar buttons
		self.actionNew.setIcon( QtGui.QIcon(':/trolltech/styles/commonstyle/images/file-32.png') )
		self.actionOpen.setIcon( QtGui.QIcon(':/trolltech/styles/commonstyle/images/diropen-32.png') )
		self.actionSave.setIcon( QtGui.QIcon(':/trolltech/styles/commonstyle/images/standardbutton-save-32.png') )
		self.toolBar.addAction(self.actionNew)
		self.toolBar.addAction(self.actionOpen)
		self.toolBar.addAction(self.actionSave)

		# connect menu items
		self.actionE_xit.triggered.connect( self.close )
		self.actionOpen.triggered.connect( self.loadFileDialog )
		self.actionSave.triggered.connect( self.saveFileDialog )
		self.actionSave_As.triggered.connect( self.saveAsFileDialog )
		self.actionNew.triggered.connect( self.newFileDialog )

		# connect property listing to the tree widget
		self.hierarchyTree.itemSelectionChanged.connect( self.updatePropertyTable )
		self.propertyTable.cellChanged.connect( self.editProperty )

		#self.load('sample.pvm')

	def newFileDialog(self):

		if self.world != self.oldWorld:
			result = QtGui.QMessageBox.warning( self, 'Save changes',
				'The active world has changed since last saved, would you like to save it now?',
				QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel, 
				QtGui.QMessageBox.Yes )
			if result == QtGui.QMessageBox.Yes:
				self.saveFileDialog()
			elif result == QtGui.QMessageBox.Cancel:
				return

		self.oldWorld = types.World()
		self.world = types.World()
		self.hierarchyTree.clear()
		self.graphicsScene.clear()
		self.propertyTable.setRowCount(0)
		

	def loadFileDialog(self):

		if self.world != self.oldWorld:
			result = QtGui.QMessageBox.warning( self, 'Save Changes',
				'The active world has changed since last saved, would you like to save it now?',
				QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel, 
				QtGui.QMessageBox.Yes )
			if result == QtGui.QMessageBox.Yes:
				self.saveFileDialog()
			elif result == QtGui.QMessageBox.Cancel:
				return

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

		try:
			outfile.write( json.dumps(self.world.serialize(), indent=4) )
			self.oldWorld = types.World.deserialize( self.world.serialize() )
			print 'Dump to file',self.filename,'successful'
		except Exception as e:
			print 'Failed to convert world to JSON, save failed.'
			print str(e)

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
		self.oldWorld = types.World.deserialize( self.world.serialize() )
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

		#		featureItem.sortChildren(0, Qt.AscendingOrder)
		#	areaItem.sortChildren(0, Qt.AscendingOrder)
		#self.hierarchyTree.sortItems(0, Qt.AscendingOrder)

		self.updateMapWidget()


	def updateMapWidget(self):

		graph = pydot.Dot()

		# build adjacency graph from world
		for area in self.world.areas.values():
		
			# create node for each room
			node = pydot.Node(area.id)
			node.set( 'label', area.name )
			graph.add_node(node)

			# link to adjacent rooms
			breakFlag = False
			for feature in area.features:
				for action in feature.actions:
					for event in action.events:
						if type(event) == events.PlayerMoveEvent:
							graph.add_edge( pydot.Edge( src=area.id, dst=event.properties['destination'] ) )
							breakFlag = True
							break
					if breakFlag:
						break
				
		ps = graph.create_svg(prog='neato')
		psBytes = QtCore.QByteArray(ps)
		renderer = QtSvg.QSvgRenderer(psBytes)
		svgItem = QtSvg.QGraphicsSvgItem()
		svgItem.setSharedRenderer(renderer)
		self.graphicsScene = QtGui.QGraphicsScene()
		self.graphicsScene.addItem(svgItem)

		self.graphicsView.setScene(self.graphicsScene)
		self.graphicsView.setInteractive(True)
		self.graphicsView.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
	


	def updatePropertyTable(self):

		self.propertyTable.setHorizontalHeaderLabels( ['Property', 'Value'] )
		if len( self.hierarchyTree.selectedItems() ) == 0:
			self.propertyTable.setRowCount(0)
			return
		
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
		value = str(self.propertyTable.item(row,column).text())
		setattr( self.propertyTable.ventureObject, str(key), value)
		#print 'The value of',key,'is now',value



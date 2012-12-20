from window import Ui_MainWindow
from PyQt4 import QtGui, QtCore, QtSvg
from PyQt4.QtCore import Qt

from common import types
from common import events

import json
import gzip
import traceback
import pydot


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
	'''The root class of the GUI that manages the widgets'''

	def __init__(self):
		'''Initialize all the GUI-related items that could not be done in the WYSIWYG editor'''

		QtGui.QMainWindow.__init__(self)
		self.setupUi(self)
		self.mainSplitter.setSizes([400,200])

		# set icons
		style = QtGui.QCommonStyle()
		self.actionNew.setIcon( style.standardIcon( QtGui.QStyle.SP_FileIcon ) )
		self.actionOpen.setIcon( style.standardIcon( QtGui.QStyle.SP_DirOpenIcon ) )
		self.actionSave.setIcon( style.standardIcon( QtGui.QStyle.SP_DialogSaveButton ) )
		self.pushMoveUp.setIcon( style.standardIcon( QtGui.QStyle.SP_ArrowUp ) )
		self.pushMoveDown.setIcon( style.standardIcon( QtGui.QStyle.SP_ArrowDown ) )
		self.pushDeleteItem.setIcon(style.standardIcon(QtGui.QStyle.SP_TrashIcon))
		self.pushNewSibling.setIcon(style.standardIcon(QtGui.QStyle.SP_FileDialogNewFolder))
		self.pushNewChild.setIcon(style.standardIcon(QtGui.QStyle.SP_FileIcon))

		self.filename = ''
		self.world = types.World()
		self.oldWorld = types.World()

		self.graphicsScene = QtGui.QGraphicsScene()
		self.graphicsView.setScene( self.graphicsScene )

		# connect toolbar buttons
		self.toolBar.addAction(self.actionNew)
		self.toolBar.addAction(self.actionOpen)
		self.toolBar.addAction(self.actionSave)

	
		# connect File menu items
		self.actionE_xit.triggered.connect( self.close )
		self.actionOpen.triggered.connect( self.loadFileDialog )
		self.actionSave.triggered.connect( self.saveFileDialog )
		self.actionSave_As.triggered.connect( self.saveAsFileDialog )
		self.actionNew.triggered.connect( self.newFileDialog )

		# connect Player menu items


		# connect Help menu items
		def aboutQt(): QtGui.QMessageBox.aboutQt(self)
		self.actionAbout_Qt.triggered.connect( aboutQt )

		# connect property listing to the tree widget
		self.hierarchyTree.itemSelectionChanged.connect( self.updatePropertyTable )
		self.hierarchyTree.itemSelectionChanged.connect( self.updateButtonAvailability )
		self.propertyTable.cellChanged.connect( self.editProperty )
		self.updateButtonAvailability()

		# connect object tree manipulation buttons
		self.pushNewSibling.clicked.connect( self.addSibling )
		self.pushNewChild.clicked.connect( self.addChild )
		self.pushDeleteItem.clicked.connect( self.deleteItem )
		self.pushMoveUp.clicked.connect( self.moveItemUp )
		self.pushMoveDown.clicked.connect( self.moveItemDown )

		#self.load('sample.pvm')


	#################################################
	### Open/Save Functions
	#################################################

	def newFileDialog(self):
		'''Prompt for save if appropriate, and load an empty map'''

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
		'''Prompt for save if appropriate, and load chosen map'''

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

		if filename == '': return

		dump = {}
		with gzip.open(filename, 'r') if filename[-2:] == 'gz' else open(filename, 'r') as file:
			try:
				tempstr = file.read()
				dump = json.loads(tempstr)
			except:
				print 'There was a problem loading', filename


		# populate tree
		self.world = types.World.deserialize(dump)
		self.oldWorld = types.World.deserialize( self.world.serialize() )
		print 'Parse successful'

		# update widgets
		self.buildHierarchyTree()
		self.updateMapWidget()

		# use given file as save target
		self.filename = str(filename)


	def saveFileDialog(self):
		'''Save if filename is known, prompt otherwise'''

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
			traceback.print_exc(e)

		outfile.close()


	def saveAsFileDialog(self):
		'''Prompt for filename and save'''

		filename = QtGui.QFileDialog.getSaveFileName(parent = self, caption = 'Save Map File',
			filter = 'Compressed map files (*.pvm.gz);;Map files (*.pvm)')
		if filename != '':
			self.filename = str(filename)
			self.saveFileDialog()


	########################################################
	### Object browser handling
	########################################################

	def buildHierarchyTree(self):
		'''Build object hierarchy from scratch'''

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
			self.propertyTable.item(0,1).setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)

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

			self.propertyTable.setRowCount( len(treeItem.ventureObject.properties)+1 )

			# construct the event type combo box
			comboBox = QtGui.QComboBox()
			currentType = 0
			for t in events.itersubclasses( events.Event ):
				comboBox.addItem( t.__name__ )
				if t.__name__ == treeItem.ventureObject.type:
					currentType = len(comboBox)-1

			comboBox.setCurrentIndex(currentType)
			comboBox.currentIndexChanged[str].connect( self.editEventType )
			self.propertyTable.setItem( 0,0, QtGui.QTableWidgetItem('type') )
			self.propertyTable.setCellWidget( 0,1, comboBox )

			i = 1
			for name, value in treeItem.ventureObject.properties.items():
				self.propertyTable.setItem( i,0, QtGui.QTableWidgetItem(name) )
				self.propertyTable.setItem( i,1, QtGui.QTableWidgetItem(value) )


		# set all cells in col 0 read-only
		for index in range(0, self.propertyTable.rowCount()):
			item = self.propertyTable.item(index, 0).setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)


	##################################################
	### Modifying the tree and the table
	##################################################

	def updateButtonAvailability(self):

		active = {'newSibling': True, 'newChild': False, 'delete': False, 'moveUp': False, 'moveDown': False}
		hierarchy = ['area','feature','action','event', 'nothing']

		# determine selection status
		items = self.hierarchyTree.selectedItems()
		item = items[0] if len(items)>0 else None
		if item is None:
			index = -1
			maxIndex = -1
		elif item.parent() is not None:
			index = item.parent().indexOfChild(item)
			maxIndex = item.parent().childCount()-1
		else:
			index = self.hierarchyTree.indexOfTopLevelItem(item)
			maxIndex = self.hierarchyTree.topLevelItemCount()-1

		# test depth
		depth = 0
		temp = item.parent() if item is not None else None
		while temp is not None:
			depth += 1
			temp = temp.parent()

		# determine button state
		if len(items) == 0:
			# default state
			pass

		else:
			active['delete'] = True
			if not isinstance(item.ventureObject, events.Event):
				active['newChild'] = True
			if index > 0:
				active['moveUp'] = True
			if index >= 0 and index < maxIndex:
				active['moveDown'] = True

		# set button status
		self.pushNewSibling.setDisabled( not active['newSibling'] )
		self.pushNewSibling.setStatusTip( 'Add a new {0} after the selected {0}.'.format(hierarchy[depth]) )
		self.pushNewChild.setDisabled( not active['newChild'] )
		self.pushNewChild.setStatusTip( 'Add a new {0} to the selected {1}.'.format(hierarchy[depth+1],hierarchy[depth]) )
		self.pushDeleteItem.setDisabled( not active['delete'] )
		self.pushDeleteItem.setStatusTip( 'Delete the selected {0} from the world.'.format(hierarchy[depth]) )
		self.pushMoveUp.setDisabled( not active['moveUp'] )
		self.pushMoveDown.setDisabled( not active['moveDown'] )


	def addSibling(self):

		try:
			item = self.hierarchyTree.selectedItems()[0]
		except IndexError:
			item = None

		if item is None:
			newVentureObj = types.Area('New area', 'You enter an unremarkable room.')
			newVentureObj.parentWorld = self.world
			self.world.addArea(newVentureObj)
			newTreeItem = QtGui.QTreeWidgetItem(self.hierarchyTree, [newVentureObj.id, 'Area'])
			newTreeItem.ventureObject = newVentureObj
			self.updateMapWidget()

		elif isinstance(item.ventureObject, types.Area):
			newVentureObject = types.Area('New area', 'You enter an unremarkable room.')
			newVentureObject.parentWorld = self.world
			self.world.addArea(newVentureObject)
			newTreeItem = QtGui.QTreeWidgetItem(self.hierarchyTree, item)
			newTreeItem.ventureObject = newVentureObject
			newTreeItem.setText(0, newVentureObject.id)
			newTreeItem.setText(1, 'Area')

		elif isinstance(item.ventureObject, types.Feature):
			newVentureObject = types.Feature('unknown object', 'A vague and undefined object')
			newVentureObject.parentArea = item.ventureObject.parentArea
			newVentureObject.parentArea.features.append(newVentureObject)
			newTreeItem = QtGui.QTreeWidgetItem(item.parent(), item)
			newTreeItem.ventureObject = newVentureObject
			newTreeItem.setText(0, newVentureObject.name)
			newTreeItem.setText(1, 'Feature')
		
		elif isinstance(item.ventureObject, types.Action):
			newVentureObject = types.Action('Do something')
			newVentureObject.parentFeature = item.ventureObject.parentFeature
			newVentureObject.parentFeature.actions.append(newVentureObject)
			newTreeItem = QtGui.QTreeWidgetItem(item.parent(), item)
			newTreeItem.ventureObject = newVentureObject
			newTreeItem.setText(0, newVentureObject.description)
			newTreeItem.setText(1, 'Action')

		elif isinstance(item.ventureObject, events.Event):
			newVentureObject = events.TextEvent({'text': 'Nothing happens'})
			newVentureObject.parentAction = item.ventureObject.parentAction
			newVentureObject.parentAction.events.append(newVentureObject)
			newTreeItem = QtGui.QTreeWidgetItem(item.parent(), item)
			newTreeItem.ventureObject = newVentureObject
			newTreeItem.setText(0, newVentureObject.type)
			newTreeItem.setText(1, 'Event')


	def addChild(self):

		try:
			item = self.hierarchyTree.selectedItems()[0]
		except IndexError:
			return

		if isinstance(item.ventureObject, types.Area):
			newVentureObject = types.Feature('unknown object', 'A vague and undefined object')
			newVentureObject.parentArea = item.ventureObject
			item.ventureObject.features.append(newVentureObject)
			newTreeItem = QtGui.QTreeWidgetItem(item, [newVentureObject.name, 'Feature'])
			newTreeItem.ventureObject = newVentureObject

		elif isinstance(item.ventureObject, types.Feature):
			newVentureObject = types.Action('Do something')
			newVentureObject.parentFeature = item.ventureObject
			item.ventureObject.actions.append(newVentureObject)
			newTreeItem = QtGui.QTreeWidgetItem(item, [newVentureObject.description, 'Action'])
			newTreeItem.ventureObject = newVentureObject

		elif isinstance(item.ventureObject, types.Action):
			newVentureObject = events.TextEvent({'text': 'Nothing happens'})
			newVentureObject.parentAction = item.ventureObject
			item.ventureObject.events.append(newVentureObject)
			newTreeItem = QtGui.QTreeWidgetItem(item, [newVentureObject.type, 'Event'])
			newTreeItem.ventureObject = newVentureObject

		self.hierarchyTree.expandItem(item)

	def deleteItem(self):

		pass


	def moveItemUp(self):

		pass


	def moveItemDown(self):

		pass


	def editProperty(self, row, column):

		if( column != 1 ): return
		
		key = self.propertyTable.item(row,0).text()
		value = str(self.propertyTable.item(row,column).text())
		if not isinstance(self.propertyTable.ventureObject, events.Event):
			setattr( self.propertyTable.ventureObject, str(key), value)

		if isinstance(self.propertyTable.ventureObject, types.Area) and key == 'name':
			self.world.updateArea(self.propertyTable.ventureObject)
			self.hierarchyTree.selectedItems()[0].setText(0, self.propertyTable.ventureObject.id)
			self.propertyTable.item(0,1).setText( self.propertyTable.ventureObject.id )
			self.updateMapWidget()
		
		elif isinstance(self.propertyTable.ventureObject, types.Feature) and key == 'name':
			self.hierarchyTree.selectedItems()[0].setText(0, value)
		
		elif isinstance(self.propertyTable.ventureObject, types.Action) and key == 'description':
			self.hierarchyTree.selectedItems()[0].setText(0, value)
		
		elif isinstance(self.propertyTable.ventureObject, events.Event) and key == 'destination':
			self.propertyTable.ventureObject.properties['destination'] = value
			self.updateMapWidget()

		#print 'The value of',key,'is now',value

	def editEventType(self, newType):

		oldEvent = self.propertyTable.ventureObject
		newEvent = None

		for t in events.itersubclasses(events.Event):
			if t.__name__ == newType:
				newEvent = t()
		
		if newEvent is None:
			return
		
		# replace old class with new class
		newEvent.parentAction = oldEvent.parentAction
		index = oldEvent.parentAction.events.index(oldEvent)
		oldEvent.parentAction.events[index] = newEvent
		
		self.propertyTable.ventureObject = newEvent
		self.hierarchyTree.selectedItems()[0].ventureObject = newEvent
		self.hierarchyTree.selectedItems()[0].setText(0, newEvent.type)
		
		self.updatePropertyTable()


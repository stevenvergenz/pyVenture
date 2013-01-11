from PyQt4.QtGui import QAbstractItemModel, QModelIndex
from PyQt4.QtCore import QString, QVariant, Qt
from common import types


class WorldModel(QAbstractItemModel):

	def __init__(self, world, parent = None):
		'''Stock constructor, plus World data object'''

		QAbstractItemModel.__init__(self, parent)
		self.world = world

	def index(self, row, column, parent = QModelIndex()):
		
		if not self.hasIndex(row, column, parent):
			return QModelIndex()

		if not parent.isValid():
			parentItem = self.world
		else:
			parentItem = parent.internalPointer()

		try:
			if isinstance(parentItem, types.World):
				childItem = parentItem.areas[row]
			elif isinstance(parentItem, types.Area):
				childItem = parentItem.features[row]
			elif isinstance(parentItem, types.Feature):
				childItem = parentItem.actions[row]
			elif isinstance(parentItem, types.Action):
				childItem = parentItem.events[row]
		except IndexError:
			return QModelIndex()
		else:
			return createIndex(row, column, childItem)


	def parent(self, child):

		if not child.isValid():
			return QModelIndex()

		childItem = child.internalPointer()
		parentRow = 0

		if isinstance(childItem, types.Area):
			return QModelIndex()

		elif isinstance(childItem, types.Feature):
			parentItem = childItem.parentArea
			parentRow = parentItem.parentArea.features.index(parentItem)

		elif isinstance(childItem, types.Action):
			parentItem = childItem.parentFeature
			parentRow = parentItem.parentFeature.actions.index(parentItem)

		elif isinstance(childItem, types.Event):
			parentItem = childItem.parentAction
			parentRow = parentItem.parentAction.events.index(parentItem)

		return self.createIndex(parentRow, 0, parentItem)


	def rowCount(self, parent = QModelIndex()):
		pass

	def columnCount(self, parent = QModelIndex()):
		pass

	def data(self, index, role = Qt.DisplayRole):
		pass

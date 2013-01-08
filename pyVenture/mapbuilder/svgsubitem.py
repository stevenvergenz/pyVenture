from PyQt4 import QtGui
from lxml import etree

class SvgSubItem(QtGui.QGraphicsItemGroup):

	def __init__(self, svgText):

		QtGui.QGraphicsItemGroup.__init__(self)
		self.generateItemsFromSvg(svgText)
		

	def generateItemsFromSvg(self, svgText):

		# generate sample item
		node = QtGui.QGraphicsEllipseItem( 38.4983, -81.3313, 38.4949, 18.0, self)
		#cx="38.4983" cy="-81.3313" rx="38.4949" ry="18"

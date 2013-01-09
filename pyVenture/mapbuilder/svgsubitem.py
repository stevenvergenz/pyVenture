from PyQt4.QtGui import QGraphicsPolygonItem, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsItemGroup, QPolygonF, QColor, QFont
from PyQt4.QtCore import QString, QRectF, QPointF
from lxml import etree as ET

class SvgSubItem(QGraphicsPolygonItem):

	def __init__(self, svgText):

		QGraphicsPolygonItem.__init__(self)
		self.generateItemsFromSvg(svgText)
		

	def generateItemsFromSvg(self, svgText):

		# build xml tree
		ns = {'svg': 'http://www.w3.org/2000/svg'}
		doc = ET.fromstring(svgText)

		# grab the root node properties
		rootNode = doc.xpath('/svg:svg/svg:g[1]', namespaces=ns)[0]
		polygon = rootNode.xpath('./svg:polygon', namespaces=ns)[0]
		pointStr = polygon.xpath('./@points', namespaces=ns)[0]
		penColor = QString(polygon.xpath('./@stroke', namespaces=ns)[0])
		fillColor = QString(polygon.xpath('./@fill', namespaces=ns)[0])

		# parse root polygon path
		path = QPolygonF()
		for pair in pointStr.split(' '):
			dims = pair.split(',')
			point = QPointF( float(dims[0]), float(dims[1]) )
			path.append(point)
		self.setPolygon(path)

		# fill in root node colors
		if QColor.isValidColor(penColor):
			self.setPen( QColor(penColor) )
		if QColor.isValidColor(fillColor):
			self.setBrush( QColor(fillColor) )

		# build each graph node
		for xmlNode in rootNode.xpath('./svg:g', namespaces=ns):

			group = QGraphicsItemGroup(self)

			if xmlNode.attrib['class'] == 'node':
				
				# get the ellipse info
				ellipseNode = xmlNode.xpath('./svg:ellipse', namespaces=ns)[0]
				elProps = { k: float(ellipseNode.attrib[k]) for k in ['cx', 'cy', 'rx', 'ry']}
				rect = QRectF( elProps['cx']-elProps['rx'], elProps['cy']-elProps['ry'], 2*elProps['rx'], 2*elProps['ry'])
				penColor = QString(ellipseNode.attrib['stroke'])
				ellipseItem = QGraphicsEllipseItem(rect, group)
				if QColor.isValidColor(penColor):
					ellipseItem.setPen( QColor(penColor) )

				# get the text info
				textNode = xmlNode.xpath('./svg:text', namespaces=ns)[0]
				text = textNode.text
				textItem = QGraphicsTextItem(text, group)
				penColor = textNode.attrib.get('fill', 'black')
				nodePoint = QPointF(float(textNode.attrib['x']), float(textNode.attrib['y']))
				textItem.setPos( nodePoint - textItem.boundingRect().center() + QPointF(0.0,-4.0))
				if QColor.isValidColor(penColor):
					textItem.setDefaultTextColor( QColor(penColor) )

			elif xmlNode.attrib['class'] == 'edge':
				pass

    	#<g id="node1" class="node">
    	#  <title>Armory 1</title>
    	#  <ellipse fill="none" stroke="black" cx="38.4983" cy="-81.3313" rx="38.4949" ry="18"/>
    	#  <text text-anchor="middle" x="38.4983" y="-77.6313" font-family="Times,serif" font-size="14.00">Armory</text>
		#</g>

		# generate sample item
		#node = QtGui.QGraphicsEllipseItem( 38.4983, -81.3313, 38.4949, 18.0, self)
		#cx="38.4983" cy="-81.3313" rx="38.4949" ry="18"

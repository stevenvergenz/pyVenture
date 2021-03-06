import sys

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtSvg
import pydot

def main():

	app = QtGui.QApplication(sys.argv)

	# build dot graph
	graph = pydot.Dot()
	node1 = pydot.Node('node1')
	node2 = pydot.Node('node2')
	edge = pydot.Edge(src='node1', dst='node2')
	graph.add_node( node1 )
	graph.add_node( node2 )
	graph.add_edge( edge )


	ps = graph.create_svg()
	byteArray = QtCore.QByteArray(ps)

	renderer = QtSvg.QSvgRenderer(byteArray)
	svgItem = QtSvg.QGraphicsSvgItem()
	svgItem.setSharedRenderer(renderer)
	scene = QtGui.QGraphicsScene()
	scene.addItem(svgItem)

	view = QtGui.QGraphicsView(scene)
	view.setInteractive(True)
	view.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
	view.show()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created: Fri Dec 21 08:58:27 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.mainSplitter = QtGui.QSplitter(self.centralwidget)
        self.mainSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.mainSplitter.setObjectName(_fromUtf8("mainSplitter"))
        self.graphicsView = QtGui.QGraphicsView(self.mainSplitter)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.propertySplitter = QtGui.QSplitter(self.mainSplitter)
        self.propertySplitter.setFrameShape(QtGui.QFrame.NoFrame)
        self.propertySplitter.setMidLineWidth(0)
        self.propertySplitter.setOrientation(QtCore.Qt.Vertical)
        self.propertySplitter.setHandleWidth(3)
        self.propertySplitter.setObjectName(_fromUtf8("propertySplitter"))
        self.frame = QtGui.QFrame(self.propertySplitter)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.hierarchyTree = QtGui.QTreeWidget(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hierarchyTree.sizePolicy().hasHeightForWidth())
        self.hierarchyTree.setSizePolicy(sizePolicy)
        self.hierarchyTree.setAlternatingRowColors(True)
        self.hierarchyTree.setAnimated(True)
        self.hierarchyTree.setColumnCount(2)
        self.hierarchyTree.setObjectName(_fromUtf8("hierarchyTree"))
        self.hierarchyTree.header().setDefaultSectionSize(200)
        self.verticalLayout.addWidget(self.hierarchyTree)
        self.frame_2 = QtGui.QFrame(self.frame)
        self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushNewSibling = QtGui.QPushButton(self.frame_2)
        self.pushNewSibling.setText(_fromUtf8(""))
        self.pushNewSibling.setObjectName(_fromUtf8("pushNewSibling"))
        self.horizontalLayout.addWidget(self.pushNewSibling)
        self.pushNewChild = QtGui.QPushButton(self.frame_2)
        self.pushNewChild.setText(_fromUtf8(""))
        self.pushNewChild.setObjectName(_fromUtf8("pushNewChild"))
        self.horizontalLayout.addWidget(self.pushNewChild)
        self.pushDeleteItem = QtGui.QPushButton(self.frame_2)
        self.pushDeleteItem.setText(_fromUtf8(""))
        self.pushDeleteItem.setObjectName(_fromUtf8("pushDeleteItem"))
        self.horizontalLayout.addWidget(self.pushDeleteItem)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushMoveUp = QtGui.QPushButton(self.frame_2)
        self.pushMoveUp.setText(_fromUtf8(""))
        self.pushMoveUp.setObjectName(_fromUtf8("pushMoveUp"))
        self.horizontalLayout.addWidget(self.pushMoveUp)
        self.pushMoveDown = QtGui.QPushButton(self.frame_2)
        self.pushMoveDown.setText(_fromUtf8(""))
        self.pushMoveDown.setObjectName(_fromUtf8("pushMoveDown"))
        self.horizontalLayout.addWidget(self.pushMoveDown)
        self.verticalLayout.addWidget(self.frame_2)
        self.propertyTable = QtGui.QTableWidget(self.propertySplitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.propertyTable.sizePolicy().hasHeightForWidth())
        self.propertyTable.setSizePolicy(sizePolicy)
        self.propertyTable.setAlternatingRowColors(True)
        self.propertyTable.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.propertyTable.setGridStyle(QtCore.Qt.DotLine)
        self.propertyTable.setWordWrap(False)
        self.propertyTable.setCornerButtonEnabled(False)
        self.propertyTable.setObjectName(_fromUtf8("propertyTable"))
        self.propertyTable.setColumnCount(2)
        self.propertyTable.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.propertyTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.propertyTable.setHorizontalHeaderItem(1, item)
        self.propertyTable.horizontalHeader().setDefaultSectionSize(120)
        self.propertyTable.horizontalHeader().setStretchLastSection(True)
        self.propertyTable.verticalHeader().setVisible(False)
        self.horizontalLayout_2.addWidget(self.mainSplitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName(_fromUtf8("menu_File"))
        self.menu_Player = QtGui.QMenu(self.menubar)
        self.menu_Player.setObjectName(_fromUtf8("menu_Player"))
        self.menu_Help = QtGui.QMenu(self.menubar)
        self.menu_Help.setObjectName(_fromUtf8("menu_Help"))
        self.menu_Tools = QtGui.QMenu(self.menubar)
        self.menu_Tools.setObjectName(_fromUtf8("menu_Tools"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setAllowedAreas(QtCore.Qt.AllToolBarAreas)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSave_As = QtGui.QAction(MainWindow)
        self.actionSave_As.setObjectName(_fromUtf8("actionSave_As"))
        self.actionE_xit = QtGui.QAction(MainWindow)
        self.actionE_xit.setObjectName(_fromUtf8("actionE_xit"))
        self.actionSet_spawnpoint_here = QtGui.QAction(MainWindow)
        self.actionSet_spawnpoint_here.setObjectName(_fromUtf8("actionSet_spawnpoint_here"))
        self.actionSet_location_here = QtGui.QAction(MainWindow)
        self.actionSet_location_here.setObjectName(_fromUtf8("actionSet_location_here"))
        self.actionManage_inventory = QtGui.QAction(MainWindow)
        self.actionManage_inventory.setObjectName(_fromUtf8("actionManage_inventory"))
        self.actionAbout_pyVenture = QtGui.QAction(MainWindow)
        self.actionAbout_pyVenture.setObjectName(_fromUtf8("actionAbout_pyVenture"))
        self.actionAbout_Qt = QtGui.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName(_fromUtf8("actionAbout_Qt"))
        self.actionView_JSON = QtGui.QAction(MainWindow)
        self.actionView_JSON.setObjectName(_fromUtf8("actionView_JSON"))
        self.menu_File.addAction(self.actionNew)
        self.menu_File.addAction(self.actionOpen)
        self.menu_File.addAction(self.actionSave)
        self.menu_File.addAction(self.actionSave_As)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionE_xit)
        self.menu_Player.addAction(self.actionSet_spawnpoint_here)
        self.menu_Player.addAction(self.actionSet_location_here)
        self.menu_Player.addAction(self.actionManage_inventory)
        self.menu_Help.addAction(self.actionAbout_pyVenture)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menu_Tools.addAction(self.actionView_JSON)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Player.menuAction())
        self.menubar.addAction(self.menu_Tools.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "pyVenture Map Builder", None, QtGui.QApplication.UnicodeUTF8))
        self.hierarchyTree.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.hierarchyTree.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.pushNewSibling.setToolTip(QtGui.QApplication.translate("MainWindow", "New Sibling", None, QtGui.QApplication.UnicodeUTF8))
        self.pushNewSibling.setStatusTip(QtGui.QApplication.translate("MainWindow", "Add a new area to the world.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushNewChild.setToolTip(QtGui.QApplication.translate("MainWindow", "New Child", None, QtGui.QApplication.UnicodeUTF8))
        self.pushNewChild.setStatusTip(QtGui.QApplication.translate("MainWindow", "Add a new feature to the selected area.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushDeleteItem.setToolTip(QtGui.QApplication.translate("MainWindow", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.pushDeleteItem.setStatusTip(QtGui.QApplication.translate("MainWindow", "Remove the selected item from the world.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushMoveUp.setToolTip(QtGui.QApplication.translate("MainWindow", "Move Up", None, QtGui.QApplication.UnicodeUTF8))
        self.pushMoveUp.setStatusTip(QtGui.QApplication.translate("MainWindow", "Move the selected item up relative to its siblings.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushMoveDown.setToolTip(QtGui.QApplication.translate("MainWindow", "Move Down", None, QtGui.QApplication.UnicodeUTF8))
        self.pushMoveDown.setStatusTip(QtGui.QApplication.translate("MainWindow", "Move the selected item down relative to its siblings.", None, QtGui.QApplication.UnicodeUTF8))
        item = self.propertyTable.horizontalHeaderItem(0)
        item.setText(QtGui.QApplication.translate("MainWindow", "Property", None, QtGui.QApplication.UnicodeUTF8))
        item = self.propertyTable.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("MainWindow", "Value", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Player.setTitle(QtGui.QApplication.translate("MainWindow", "&Player", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Help.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Tools.setTitle(QtGui.QApplication.translate("MainWindow", "&Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setText(QtGui.QApplication.translate("MainWindow", "&New...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "&Open...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("MainWindow", "&Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_As.setText(QtGui.QApplication.translate("MainWindow", "Save &As...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionE_xit.setText(QtGui.QApplication.translate("MainWindow", "E&xit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSet_spawnpoint_here.setText(QtGui.QApplication.translate("MainWindow", "Set &spawnpoint here", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSet_location_here.setText(QtGui.QApplication.translate("MainWindow", "Set &location here", None, QtGui.QApplication.UnicodeUTF8))
        self.actionManage_inventory.setText(QtGui.QApplication.translate("MainWindow", "Manage &inventory...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout_pyVenture.setText(QtGui.QApplication.translate("MainWindow", "About &pyVenture...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout_Qt.setText(QtGui.QApplication.translate("MainWindow", "About Qt...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionView_JSON.setText(QtGui.QApplication.translate("MainWindow", "View &JSON...", None, QtGui.QApplication.UnicodeUTF8))

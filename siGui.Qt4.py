#!/usr/bin/python
try:
	from PyQt4 import QtGui, QtCore
except ImportError:
	from PySide import QtGui, QtCore
import httplib, urllib
from siSession import siSession
from siCore import *
import sys, time, os
import tempfile


class siWidget(QtGui.QWidget):
	"""
	Main class of SaveIt Qt-based GUI.
	It wraps SaveIt app and is similar to web version.
	"""
	def __init__(self, *args, **kargs):
		if kargs.get('SaveIt', False):
			if kargs.get('authHeader'):
				self.saveIt(authHeader = kargs.get('authHeader'), remember = kargs.get('remember', False))
				
			else:
				self.saveIt(login = kargs.get('login'), password = kargs.get('password'), 
				remember = kargs.get('remember', False))
		QtGui.QWidget.__init__(self, parent = kargs.get("parent"))
		self.RO = QtCore.Qt.ItemFlags(61) # it equals to next 6 strings
		#self.RO = QtCore.Qt.NoItemFlags
		#self.RO |= QtCore.Qt.ItemIsSelectable
		#self.RO |= QtCore.Qt.ItemIsDropEnabled
		#self.RO |= QtCore.Qt.ItemIsDragEnabled
		#self.RO |= QtCore.Qt.ItemIsUserCheckable
		#self.RO |= QtCore.Qt.ItemIsEnabled
		self.orSet = set()
		self.andSet = set()
		self.findSet = set()
		#some decor
		self.putIn()

	def putIn(self):
		self.setLayout(QtGui.QHBoxLayout(self))
		self.tagLayout = QtGui.QVBoxLayout()
		self.fileLayout = QtGui.QHBoxLayout()
		self.infoLayout = QtGui.QVBoxLayout()
		self.layout().addLayout(self.tagLayout)
		self.layout().addLayout(self.fileLayout)
		self.layout().addLayout(self.infoLayout)
		self.fileTable = QtGui.QTableWidget(0, 2, self)
		self.info = QtGui.QVBoxLayout()
		self.fileLayout.addWidget(self.fileTable)
		self.fileLayout.addLayout(self.info)
		self.customizeTagList()
		self.customizeFileTable()
		self.customizeInfoList()

	def customizeTagList(self):
		self.tagLabel = QtGui.QLabel('Tag List', self)
		self.tagLayout.addWidget(self.tagLabel)
		self.tagLabel.setAlignment(QtCore.Qt.AlignHCenter)
		self.tagTabber = QtGui.QTabWidget(self)
		self.tagLayout.addWidget(self.tagTabber)
		self.tagTabber.setFixedWidth(200)
		self.tagOrTab = QtGui.QTableWidget(0, 2, self)
		self.tagAndTab = QtGui.QTableWidget(0, 2, self)
		self.tagTabber.addTab(self.tagOrTab, 'OR')
		self.tagTabber.addTab(self.tagAndTab, 'AND')
		self.tagOrTab.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
		self.tagOrTab.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
		self.tagOrTab.setHorizontalHeaderLabels(['',''])
		self.tagOrTab.verticalHeader().hide()
		self.tagOrTab.horizontalHeader().setClickable(True)
		self.tagOrTab.hideColumn(0)
		##
		self.tagAndTab.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
		self.tagAndTab.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
		self.tagAndTab.setHorizontalHeaderLabels(['',''])
		self.tagAndTab.verticalHeader().hide()
		self.tagAndTab.horizontalHeader().setClickable(True)
		self.tagAndTab.hideColumn(0)
		self.updateTagSets()
		#connections
		QtCore.QObject.connect(self.tagOrTab, QtCore.SIGNAL("cellPressed(int, int)"), 
			lambda x: self.tagOrTableElems[str(self.tagOrTab.item(x, 0).text())][0].setCheckState(
			2 - self.tagOrTableElems[str(self.tagOrTab.item(x, 0).text())][0].checkState()))
		QtCore.QObject.connect(self.tagOrTab.horizontalHeader(), QtCore.SIGNAL("sectionClicked(int)"),
			lambda x : [cb[0].setCheckState(2 - cb[0].checkState()) for cb in self.tagOrTableElems.values()])
		QtCore.QObject.connect(self.tagAndTab, QtCore.SIGNAL("cellPressed(int, int)"), 
			lambda x: self.tagAndTableElems[str(self.tagAndTab.item(x, 0).text())][0].setCheckState(
			2 - self.tagAndTableElems[str(self.tagAndTab.item(x, 0).text())][0].checkState()))
		QtCore.QObject.connect(self.tagAndTab.horizontalHeader(), QtCore.SIGNAL("sectionClicked(int)"),
			lambda x : [cb[0].setCheckState(2 - cb[0].checkState()) for cb in self.tagAndTableElems.values()])

	def customizeFileTable(self):
		self.fileTable.setMinimumSize(QtCore.QSize(200, 200))
		self.fileTable.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)
		self.fileTable.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
		self.fileTable.horizontalHeader().setSortIndicatorShown(True)
		self.fileTable.horizontalHeader().setClickable(True)
		self.fileTable.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
		self.fileTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.fileTable.setHorizontalHeaderLabels(['ID', 'TYPE'])
		self.changeFileSet()	
		#connections
		QtCore.QObject.connect(self.fileTable, QtCore.SIGNAL("cellPressed(int, int)"), self.selectFile)
		QtCore.QObject.connect(self.fileTable, QtCore.SIGNAL("cellDoubleClicked(int, int)"), self.openFile)
		QtCore.QObject.connect(self.fileTable.horizontalHeader(), QtCore.SIGNAL("sectionClicked(int)"),
			self.fileTable.sortByColumn)
		QtCore.QObject.connect(self.fileTable, QtCore.SIGNAL("itemSelectionChanged()"), 
			lambda : self.selectFile(self.fileTable.currentItem().row()) if self.fileTable.columnCount() > 0 else None)

	def customizeInfoList(self):
		self.nameOfChoice = QtGui.QLabel(self)
		self.info.addWidget(self.nameOfChoice)
		self.nameOfChoice.setFixedWidth(300)
		self.tagsOfChoice = QtGui.QListWidget(self)
		self.info.addWidget(self.tagsOfChoice)
		self.tagsOfChoice.setFixedWidth(300)

	def selectFile(self, x):
		self.nameOfChoice.setText(self.fileTable.item(x, 0).text())
		self.tagsOfChoice.clear()
		self.tagsOfChoice.addItems(self.siSes.listTags(file = str(self.fileTable.item(x, 0).text())))

	def openFile(self, x):
		print 'open: %s\n' % x
		name = str(self.fileTable.item(x, 0).text())
		self.siSes.download('SaveItDir/' + name, tempfile.gettempdir())
		print 'Done'

	def changeFileSet(self):
		self.orSet = set()
		for tag in self.tagOrTableElems.keys():
			if self.tagOrTableElems[tag][0].checkState():
				self.orSet.update(set(self.siSes.listFiles(tag = tag)))
		self.andSet = set()
		amount = 0
		for tag in self.tagAndTableElems.keys():
			if self.tagAndTableElems[tag][0].checkState():
				if amount:
					self.andSet.intersection_update(set(self.siSes.listFiles(tag = tag)))
				else:
					self.andSet = set(self.siSes.listFiles(tag = tag))
				amount += 1
		self.findSet = self.orSet.union(self.andSet)
		self.updateFileSet()

	def updateFileSet(self):
		print 'a\n'
		amount = 0
		self.fileTable.setRowCount(amount)
		for f in self.findSet:
			amount += 1
			self.fileTable.setRowCount(amount)
			self.fileTable.setItem(amount - 1, 0, QtGui.QTableWidgetItem(self.siSes.files.elems[f].id))
			self.fileTable.setItem(amount - 1, 1, QtGui.QTableWidgetItem(self.siSes.files.elems[f].type))
			self.fileTable.item(amount - 1, 0).setFlags(self.RO)
			self.fileTable.item(amount - 1, 1).setFlags(self.RO)
			self.fileTable.setVerticalHeaderItem(amount - 1, QtGui.QTableWidgetItem(''))
		self.fileTable.sortByColumn(0, QtCore.Qt.AscendingOrder)

	def updateTagSets(self):
		amount = 0
		self.tagOrSet = set()
		self.tagOrTableElems = {}
		self.tagAndSet = set()
		self.tagAndTableElems = {}
		for tag in self.siSes.tags.elems:
			w = QtGui.QWidget(self)
			lay = QtGui.QHBoxLayout()
			w.setLayout(lay)
			w.setAccessibleName(tag)
			self.tagOrTableElems[tag] = [QtGui.QCheckBox(tag), QtGui.QPushButton('', w)]
			self.tagOrTableElems[tag][1].setIcon(
				self.tagOrTableElems[tag][1].style().standardIcon(QtGui.QStyle.SP_DialogCloseButton))
			self.tagOrTableElems[tag][1].setFlat(True)
			self.tagOrTableElems[tag][1].setFixedWidth(
				max(self.tagOrTableElems[tag][1].iconSize().width(), self.tagOrTableElems[tag][1].height()))
			lay.addWidget(self.tagOrTableElems[tag][0])
			lay.addWidget(self.tagOrTableElems[tag][1])
			amount += 1
			self.tagOrTab.setRowCount(amount)
			self.tagOrTab.setItem(amount - 1, 0, QtGui.QTableWidgetItem(tag))
			self.tagOrTab.item(amount - 1, 0).setFlags(self.RO)
			self.tagOrTab.setCellWidget(amount - 1, 1, w)
			self.tagOrTab.setVerticalHeaderItem(amount - 1, QtGui.QTableWidgetItem(''))
			##
			w = QtGui.QWidget(self)
			lay = QtGui.QHBoxLayout()
			w.setLayout(lay)
			w.setAccessibleName(tag)
			self.tagAndTableElems[tag] = [QtGui.QCheckBox(tag), QtGui.QPushButton('', w)]
			self.tagAndTableElems[tag][1].setIcon(
				self.tagAndTableElems[tag][1].style().standardIcon(QtGui.QStyle.SP_DialogCloseButton))
			self.tagAndTableElems[tag][1].setFlat(True)
			self.tagAndTableElems[tag][1].setFixedWidth(
				max(self.tagAndTableElems[tag][1].iconSize().width(), self.tagAndTableElems[tag][1].height()))
			lay.addWidget(self.tagAndTableElems[tag][0])
			lay.addWidget(self.tagAndTableElems[tag][1])
			self.tagAndTab.setRowCount(amount)
			self.tagAndTab.setItem(amount - 1, 0, QtGui.QTableWidgetItem(tag))
			self.tagAndTab.item(amount - 1, 0).setFlags(self.RO)
			self.tagAndTab.setCellWidget(amount - 1, 1, w)
			self.tagAndTab.setVerticalHeaderItem(amount - 1, QtGui.QTableWidgetItem(''))
			self.tagOrTableElems[tag][0].setCheckState(QtCore.Qt.Checked)
			self.tagAndTableElems[tag][0].setCheckState(QtCore.Qt.Unchecked)
			#connections
			QtCore.QObject.connect(self.tagOrTableElems[tag][0], QtCore.SIGNAL("stateChanged(int)"), 
				self.changeFileSet)
			QtCore.QObject.connect(self.tagOrTableElems[tag][1], QtCore.SIGNAL("clicked()"),
				lambda : self.delTag(tags = [str(self.sender().parent().accessibleName())]))
			QtCore.QObject.connect(self.tagAndTableElems[tag][0], QtCore.SIGNAL("stateChanged(int)"), 
				self.changeFileSet)
			QtCore.QObject.connect(self.tagAndTableElems[tag][1], QtCore.SIGNAL("clicked()"),
				lambda : self.delTag(tags = [str(self.sender().parent().accessibleName())]))
		self.tagOrTab.sortByColumn(0, QtCore.Qt.AscendingOrder)
		self.tagAndTab.sortByColumn(0, QtCore.Qt.AscendingOrder)

	def nullOr(self):
		self.orStr = ""

	def nullAnd(self):
		self.andStr = ""

	def saveIt(self, **kargs):
		kargs['verbose'] = False
		kargs['SaveIt'] = False
		self.siSes = siSession(**kargs)
		if kargs.get('remember'):
			settings = QtCore.QSettings()
			settings.beginGroup("auth")
			settings.setValue("authHeader", self.siSes.authHeader)
			settings.endGroup()

	def upload(self):
		fd = QtGui.QFileDialog(self)
		#print fd.directory().path() 
		fd.setDirectory(os.path.curdir)
		fd.setFileMode(QtGui.QFileDialog.ExistingFiles)
		for f in list(map(str, fd.getOpenFileNames())):
			self.siSes.addFile(f)
		self.updateTagSets()

	def addTag(self):
		response = QtGui.QInputDialog.getText(self, "Add Tag", "Add new tag:")
		if response[1] and response[0]:
			self.siSes.addTag(str(response[0]))
			self.updateTagSets()

	def tagFile(self, **kargs):
		files = kargs.get('files', [str(QtGui.QInputDialog.getText(self, "Tag File", "File for tagging:"))][0])
		tags = kargs.get('tags', [str(QtGui.QInputDialog.getText(self, "Tag File", "Tag for tagging:"))][0])
		for f in files:
			for tag in tags:
				self.siSes.tagFile(f, tag, group = True)
		self.siSes.update()
		self.updateTagSets()

	def untagFile(self, **kargs):
		files = kargs.get('files', [str(QtGui.QInputDialog.getText(self, "Untag File", "File for untagging:")[0])])
		tags = kargs.get('tags', [str(QtGui.QInputDialog.getText(self, "untag File", "Tag for untagging:")[0])])
		for f in files:
			for tag in tags:
				self.siSes.untagFile(f, tag, group = True)
		self.siSes.update()
		self.updateTagSets()

	def download(self):
		pass

	def delTag(self, **kargs):
		tags = kargs.get('tags', [str(QtGui.QInputDialog.getText(self, "Delete Tag", "Tag for deleting:")[0])])
		for tag in tags:
			self.siSes.delTag(tag, group = False)
		self.siSes.update()
		self.updateTagSets()


class siMainWindow(QtGui.QMainWindow):
	"""
	Main class of SaveIt Qt-based GUI
	"""
	def __init__(self, *args):
		QtGui.QMainWindow.__init__(self, *args)
		#some decor
		#self.show()
		self.showMaximized()
		self.setWindowTitle(self.tr("SaveIt Application"))
		self.setStatusBar(QtGui.QStatusBar(parent = self))
		self.statusBar().resize(self.statusBar().width(), 30)
		#main viewer
		self.decorCentral()
		#self.saveIt()
		#self.show()
		self.statusBar().showMessage('Done')

	def decorCentral(self):
		settings = QtCore.QSettings()
		settings.beginGroup("auth")
		header = settings.value("authHeader")
		settings.endGroup()
		if (hasattr(header, "toString") and  not header.toString()) or not header:
			self.decorLogin()
		else:
			self.saveIt(authHeader = header.toString() if hasattr(header, "toString") else header)

	def saveIt(self, **kargs):
		self.setCentralWidget(QtGui.QTabWidget(parent = self))
		if kargs.get('authHeader'):
			self.siWidget = siWidget(parent = self, SaveIt = True,
				authHeader = kargs.get('authHeader'), remember = kargs.get('remember', False))
		else:
			self.siWidget = siWidget(parent = self, SaveIt = True, 
				login = kargs.get('login'), password = kargs.get('password'), remember = kargs.get('remember', False))
		self.centralWidget().addTab(self.siWidget, "SaveIt")
		#Menu
		self.setMenu()
		#Toolbar
		self.setTools()

	def decorLogin(self):
		self.setCentralWidget(QtGui.QWidget(self))
		loginLayout = QtGui.QVBoxLayout()
		preLoginLayout = QtGui.QHBoxLayout()
		self.centralWidget().setLayout(preLoginLayout)
		#self.centralWidget().setFixedWidth()
		preLoginLayout.addStretch()
		preLoginLayout.addLayout(loginLayout)
		preLoginLayout.addStretch()
		loginLayout.addStretch()
		loginLayout.addWidget(QtGui.QLabel("Login"))
		login = QtGui.QLineEdit(self)
		loginLayout.addWidget(login)
		loginLayout.addWidget(QtGui.QLabel("Password"))
		password = QtGui.QLineEdit(self)
		password.setEchoMode(QtGui.QLineEdit.Password)
		loginLayout.addWidget(password)
		showPass = QtGui.QCheckBox("Show password")
		loginLayout.addWidget(showPass)
		remember = QtGui.QCheckBox("Remember me")
		loginLayout.addWidget(remember)
		loginBut = QtGui.QPushButton("Login")
		loginLayout.addWidget(loginBut)
		loginLayout.addStretch()
		#connetcions
		QtCore.QObject.connect(showPass, QtCore.SIGNAL("stateChanged(int)"),
			lambda x: password.setEchoMode(QtGui.QLineEdit.EchoMode(2 - x)))
		QtCore.QObject.connect(loginBut, QtCore.SIGNAL("clicked()"),
			lambda : self.saveIt(login = str(login.text()), password = str(password.text()), remember = remember.checkState()))

	def setMenu(self):
		quit = QtGui.QAction(self.style().standardIcon(self.style().SP_DialogCloseButton), self.tr("Quit"), self)
		QtCore.QObject.connect(quit, QtCore.SIGNAL("triggered()"), self, QtCore.SLOT("close()"))

		self.fileMenu = self.menuBar().addMenu(self.tr("&File"))
		self.fileMenu.addAction(quit)
		##
		update = QtGui.QAction(self.style().standardIcon(self.style().SP_BrowserReload), self.tr("Reload"), self) 
		QtCore.QObject.connect(update, QtCore.SIGNAL("triggered()"), self.siWidget.updateTagSets)

		self.viewMenu = self.menuBar().addMenu(self.tr("&View"))
		self.viewMenu.addAction(update)

	def setTools(self):
		self.siTools = self.addToolBar(self.tr("siTools"))
		self.siUpTool = self.siTools.addAction(self.tr("Upload File"))
		#self.siAddTool = self.siTools.addAction(self.tr("Add File"))
		#self.siDownTool = self.siTools.addAction(self.tr("Download File"))
		self.siTagTool = self.siTools.addAction(self.tr("Tag File"))
		self.siUnTagTool = self.siTools.addAction(self.tr("Untag File"))
		self.siAddTool = self.siTools.addAction(self.tr("Add Tag"))
		self.siDelTool = self.siTools.addAction(self.tr("Delete Tag"))
		#self.siCopyTool = self.siTools.addAction(self.tr("Copy"))
		#self.siPasteTool = self.siTools.addAction(self.tr("Paste"))
		##
		QtCore.QObject.connect(self.siUpTool, QtCore.SIGNAL("triggered()"),
			self.siWidget.upload)
		QtCore.QObject.connect(self.siAddTool, QtCore.SIGNAL("triggered()"),
			self.siWidget.addTag)
		#QtCore.QObject.connect(self.siDownTool, QtCore.SIGNAL("triggered()"),
		#	self.siWidget.download)
		QtCore.QObject.connect(self.siTagTool, QtCore.SIGNAL("triggered()"),
			self.siWidget.tagFile)
		QtCore.QObject.connect(self.siUnTagTool, QtCore.SIGNAL("triggered()"),
			self.siWidget.untagFile)
		QtCore.QObject.connect(self.siDelTool, QtCore.SIGNAL("triggered()"),
			self.siWidget.delTag)


def main():
	siApp = QtGui.QApplication(sys.argv)
	siApp.setOrganizationName('GUANACO.Team')
	siApp.setApplicationName('SaveIt')
	s = QtCore.QSettings()
	s.beginGroup("main")
	s.setValue("Larik", "lalka")
	s.endGroup()
	#starts siMainWindow
	siWin = siMainWindow()
	siWin.show()
	return siApp.exec_()
	

if __name__ == '__main__':
	main()

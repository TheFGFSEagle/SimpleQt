#!/usr/bin/python3
#-*-coding: utf-8-*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from .box import VBox
from .toolbar import ToolBar

class MainWindow(QMainWindow):
	"""Simplified QMainWindow"""
	def __init__(self, *args, title="Qt main window", iconFile=None, qIcon=None, themeIconId=None, widget=None, maximize=True, **kwargs):
		QMainWindow.__init__(self, *args, **kwargs)
		
		self.setWindowTitle(title)
		if qIcon:
			self.setWindowIcon(qIcon)
		elif themeIconId:
			self.setWindowThemeIconId(themeIconId)
		elif iconFile:
			self.setWindowIconFile(file=iconFile)
		self.setWidget(widget)
		
		if maximize:
			self.maximize()
	
	def addToolBar(self, name, movable=True, floatable=True, area=Qt.TopToolBarArea):
		toolBar = ToolBar(name, parent=self, movable=movable, floatable=floatable)
		QMainWindow.addToolBar(self, area, toolBar)
		return toolBar
	
	def maximize(self):
		screen = qApp.desktop()
		screensize = screen.availableGeometry(screen.primaryScreen())
		titleBarHeight = qApp.style().pixelMetric(QStyle.PM_TitleBarHeight) + 6
		self.resize(screensize.width(), screensize.height() - titleBarHeight);

	def setWindowIconFile(self, file=""):
		"""set the icon of self to the image at file or to empty QIcon"""
		icon = QIcon(file)
		self.setWindowIcon(icon)
		self._iconFile = file
	
	def setWindowThemeIconId(self, themeIconId=""):
		""""set the icon of self to the theme icon with name themeIcon or empty QIcon"""
		icon = QIcon.fromTheme(themeIconId)
		self.setWindowIcon(icon)
		self._themeIconId = themeIconId

	def setWidget(self, widget=None):
		"""set the central widget of self to widget or to the default SimpleQt.VBox"""
		if widget == None:
			widget = VBox()
		self.setCentralWidget(widget)	
	
	def widget(self):
		return self.centralWidget()
	
	def windowIconFile(self):
		"""return the file path of the window icon previously set with setWindowIconFile or None,  if it hasn't been set"""
		try:
			return self._iconFile
		except NameError:
			return None
	
	def windowThemeIconId(self):
		"""return the theme icon name of the window icon previously set with setWindowThemeIconId or None, if it hasn't been set"""
		try:
			return self._themeIconId
		except NameError:
			return None
	
	def toggle(self, *args):
		if self.isVisible():
			self.setVisible(False)
		else:
			self.setVisible(True)

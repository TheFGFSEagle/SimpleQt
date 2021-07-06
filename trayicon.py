#!/usr/bin/python3
#-*-coding: utf-8-*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class TrayIcon(QSystemTrayIcon):
	clicked = pyqtSignal()
	middleClicked = pyqtSignal()
	doubleClicked = pyqtSignal()
	rightClicked = pyqtSignal()
	def __init__(self, iconFile=None, themeIconId=None, qIcon=None, contextMenu=None, toolTip=""):
		QSystemTrayIcon.__init__(self, qIcon)
		
		icon = qIcon
		if iconFile:
			self._iconFile = iconFile
			icon = QIcon(iconFile)
		elif themeIconId:
			self._themeIconId = themeIconId
			icon = QIcon.fromTheme(themeIconId)
		self.setIcon(icon)
		
		if contextMenu:
			self.setContextMenu(contextMenu)
		
		self.setToolTip(toolTip)
		self.activated.connect(self.onActivate)
	
	def onActivate(self, reason):
		if reason == QSystemTrayIcon.Trigger:
			self.clicked.emit()
		elif reason == QSystemTrayIcon.MiddleClick:
			self.middleClicked.emit()
		elif reason == QSystemTrayIcon.Context:
			self.rightClicked.emit()
		elif reason == QSystemTrayIcon.DoubleClick:
			self.doubleClicked.emit()
	
	def showMenu(self):
		self.contextMenu().exec_()

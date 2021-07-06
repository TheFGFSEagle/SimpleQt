#!/usr/bin/python3
#-*-coding: utf-8-*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ToolBar(QToolBar):
	def __init__(self, name, parent=None, floatable=True, movable=True, orientation=Qt.Horizontal):
		QToolBar.__init__(self, name, parent)
		
		self.setFloatable(floatable)
		self.setMovable(movable)
		self.setOrientation(orientation)
	
	def addAction(self, text="", themeIconId=None, qIcon=None, iconFile=None, action=None, actionArgs=(), actionKWArgs=None, shortcut=""):
		icon = qIcon
		if iconFile:
			icon = QIcon(iconFile)
		elif themeIconId:
			icon = QIcon.fromTheme(themeIconId)
		action = QToolBar.addAction(self, icon, text)
		action.setShortcut(shortcut)
		action.triggered.connect(lambda: action(*actionArgs, **actionKWArgs))
		return action

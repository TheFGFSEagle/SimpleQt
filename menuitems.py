#!/usr/bin/python3
#-*-coding: utf-8-*-

import colprint
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class MenuItem(QAction):
	def __init__(self, *args, parent=None, text="", action=None, actionArgs=(), actionKWArgs={}, shortcut="", toolTip="", **kwargs):
		QAction.__init__(self, parent, *args, **kwargs)
		self.actionOnTriggered = action
		self.actionOnTriggeredArgs = actionArgs
		self.actionOnTriggeredKWArgs = actionKWArgs
		
		self.setText(str(text))
		self.triggered.connect(self.onTriggered)
		
		
		self.setToolTip(toolTip)
		if toolTip == "":
			self.setToolTip(self.text())
		
		self.setShortcut(shortcut)

		if parent:
			parent.addAction(self)		
	
	def onTriggered(self, selfChecked):
		if callable(self.actionOnTriggered):
			self.actionOnTriggered(selfChecked, *self.actionOnTriggeredArgs, **self.actionOnTriggeredKWArgs)
		else:
			print(colprint.Color.Yellow + "note : MenuItem with text '%s' has no action connected" % self.text() + colprint.Format.Reset)

class ImageMenuItem(MenuItem):
	def __init__(self, *args, themeIconId=None, iconFile=None, qIcon=None, **kwargs):
		MenuItem.__init__(self, *args, **kwargs)
		self._themeIconId = None
		self._iconFile = None
		
		if qIcon:
			self.setIcon(qIcon)
		elif themeIconId:
			self.setThemeIconId(themeIconId)
		elif iconFile:
			self.setIconFile(iconFile)
	
	def themeIconId(self):
		return self._themeIconId
	
	def iconFile(self):
		return self._iconFile
	
	def setThemeIconId(self, themeIconId : str =None):
		"""
		Sets the icon of the ImageMenuItem to the standard icon with name themeIconId, or to an empty QIcon
		@type themeIconId str
		@param themeIconId String containing the name of a standar iconFile
		"""
		if themeIconId:
			self._themeIconId = themeIconId
			self.setIcon(QIcon.fromTheme(themeIconId))
		else:
			self._themeIconId = None
			self.setIcon(QIcon())
	
	def setIconFile(self, iconFile=None):
		"""
		Sets the icon of the ImageMenuItem to the image file specified with iconFile or to an empty QIcon
		@param iconFile str containing the path to an image file, or None"""
		if iconFile:
			self._iconFile = iconFile
			self.setIcon(QIcon(iconFile))
		else:
			self._iconFile = None
			self.setIcon(QICon())

#!/usr/bin/python3
#-*-coding: utf-8-*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import colprint

class Button(QPushButton):
	def __init__(self, *args, text="", checkable=False, action=None, actionArgs=(), actionKWArgs={}, **kwargs):
		QPushButton.__init__(self, *args, **kwargs)
		
		self.action = action
		self.actionArgs = actionArgs
		self.actionKWArgs = actionKWArgs
		
		self.setText(text)
		self.setCheckable(checkable)
		self.clicked.connect(self.onClicked)
	
	def onClicked(self, checked):
		if callable(self.action):
			self.action(checked, *self.actionArgs, **self.actionKWArgs)
		else:
			print(colprint.Color.Yellow + "note : Button with text %s has no action connected" % self.text() + colprint.Format.Reset)

class ImageButton(Button):
	def __init__(self, *args, qIcon=None, iconFile=None, themeIconId=None, **kwargs):
		Button.__init__(self, *args, **kwargs)
		
		self._iconFile = None
		self._themeIconId = None
		
		if qIcon != None:
			self.setIcon(qIcon)
		elif iconFile != None:
			self.setIconFile(iconFile)
		elif themeIconId != None:
			self.setThemeIconId(themeIconId)
	
	def themeIconId(self):
		return self._themeIconId
	
	def iconFile(self):
		return self._iconFile
	
	def setThemeIconId(self, themeIconId=None):
		"""set icon of self to the standard icon with id iconThemeId, or to empty QIcon"""
		if themeIconId != None:
			self._themeIconId = themeIconId
			self.setIcon(QIcon.fromTheme(themeIconId))
		else:
			self._iconThemeId = None
			self.setIcon(QIcon())
	
	def setIconFile(self, iconFile):
		"""set icon of self to the image at iconFile or to empty QIcon"""
		if iconFile != None:
			self._iconFile = iconFile
			self.setIcon(QIcon(iconFile))
		else:
			self._iconFile = None
			self.setIcon(QICon())
	
	def onClicked(self, checked):
		if callable(self.action):
			self.action(checked, *self.actionArgs, **self.actionKWArgs)
		else:
			print(colprint.Color.Yellow + "note : ImageButton with text %s and icon %s has no action connected" % (self.text(), self._iconFile or self._iconThemeId) + colprint.Format.Reset)


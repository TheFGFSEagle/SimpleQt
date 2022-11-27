#!/usr/bin/python3
#-*-coding: utf-8-*-

import enum

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class BoxType(enum.Enum):
	Vertical = "vertical"
	Horizontal = "horizontal"
	Flow = "flow"
	Grid = "grid"

class FlowLayout(QLayout):
	def __init__(self, parent=None, margin=-1, spacing=-1):
		QLayout.__init__(self, parent)

		if parent is not None:
			self.setContentsMargins(margin, margin, margin, margin)

		self.setSpacing(spacing)

		self.itemList = []

	def __del__(self):
		item = self.takeAt(0)
		while item:
			item = self.takeAt(0)

	def addItem(self, item):
		self.itemList.append(item)

	def count(self):
		return len(self.itemList)

	def itemAt(self, index):
		if index >= 0 and index < len(self.itemList):
			return self.itemList[index]

		return None

	def takeAt(self, index):
		if index >= 0 and index < len(self.itemList):
			return self.itemList.pop(index)

		return None

	def expandingDirections(self):
		return Qt.Orientations(Qt.Orientation(0))

	def hasHeightForWidth(self):
		return True

	def heightForWidth(self, width):
		height = self.doLayout(QRect(0, 0, width, 0), True)
		return height

	def setGeometry(self, rect):
		QLayout.setGeometry(self, rect)
		self.doLayout(rect, False)

	def sizeHint(self):
		return self.minimumSize()

	def minimumSize(self):
		size = QSize()

		for item in self.itemList:
			size = size.expandedTo(item.minimumSize())

		margin, _, _, _ = self.getContentsMargins()

		size += QSize(2 * margin, 2 * margin)
		return size

	def doLayout(self, rect, testOnly=False):
		x = rect.x()
		y = rect.y()
		lineHeight = 0

		for item in self.itemList:
			wid = item.widget()
			spaceX = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
			spaceY = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)
			nextX = x + item.sizeHint().width() + spaceX
			if nextX - spaceX > rect.right() and lineHeight > 0:
				x = rect.x()
				y = y + lineHeight + spaceY
				nextX = x + item.sizeHint().width() + spaceX
				lineHeight = 0

			if not testOnly:
				item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

			x = nextX
			lineHeight = max(lineHeight, item.sizeHint().height())

		return y + lineHeight - rect.y()

class Box(QWidget):
	def __init__(self, *args, bType=BoxType.Vertical, scrollingEnabled=False, **kwargs):
		QWidget.__init__(self, *args, **kwargs)
		
		self.scrollingEnabled = scrollingEnabled
		self.bType = bType
		
		if scrollingEnabled:
			self.scrollLay = QVBoxLayout(self)
			
			self.scroll = QScrollArea(self)
			self.scroll.setWidgetResizable(True)
			
			self.scrollwid = QWidget(self.scroll)
			
			if bType == BoxType.Vertical:
				self.lay = QVBoxLayout(self.scrollwid)
			elif bType == BoxType.Horizontal:
				self.lay = QHBoxLayout(self.scrollwid)
			elif bType == BoxType.Flow:
				self.lay = FlowLayout(parent=self.scrollwid)
			elif bType == BoxType.Grid:
				self.lay = QGridLayout(self.scrollwid)
			else:
				raise ValueError("property 'bType' must be SimpleQt.BoxType.*")
			self.scrollwid.setLayout(self.lay)
		
			self.scroll.setWidget(self.scrollwid)
			self.scrollLay.addWidget(self.scroll)
			self.setLayout(self.scrollLay)
		else:
			if bType == BoxType.Vertical:
				self.lay = QVBoxLayout(self)
			elif bType == BoxType.Horizontal:
				self.lay = QHBoxLayout(self)
			elif bType == BoxType.Flow:
				self.lay = FlowLayout(parent=self)
			elif bType == BoxOrient.Grid:
				self.lay = QGridLayout(self)
			else:
				raise ValueError("property 'bType' must be SimpleQt.BoxType.*")
			self.setLayout(self.lay)

	
	def clearChildren(self):
		item = self.lay.takeAt(0)
		while item:
			item = self.lay.takeAt(0)

	def addWidget(self, widget, *args, **kwargs):
		self.lay.addWidget(widget, *args, **kwargs)
	
	def addLayout(self, widget, *args, **kwargs):
		self.lay.addLayout(layout, *args, **kwargs)

class VBox(Box):
	def __init__(self, *args, **kwargs):
		Box.__init__(self, *args, bType=BoxType.Vertical, **kwargs)

class HBox(Box):
	def __init__(self, *args, **kwargs):
		Box.__init__(self, *args, bType=BoxType.Horizontal, **kwargs)

class FlowBox(Box):
	def __init__(self, *args, **kwargs):
		Box.__init__(self, *args, bType=BoxType.Flow, **kwargs)

class GridBox(Box):
	def __init__(self, *args, **kwargs):
		Box.__init__(self, *args, bType=BoxType.Grid, **kwargs)

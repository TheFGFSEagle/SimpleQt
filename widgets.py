#!/usr/bin/python3
#-*-coding: utf-8-*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from .box import BoxType, Box, FlowBox

class DockWidget(QDockWidget):
	Movable = QDockWidget.DockWidgetMovable
	Closable = QDockWidget.DockWidgetClosable
	Floatable = QDockWidget.DockWidgetFloatable
	VerticalTitleBar = QDockWidget.DockWidgetVerticalTitleBar
	AllFeatures = QDockWidget.AllDockWidgetFeatures
	NoFeatures = QDockWidget.NoDockWidgetFeatures
	
	def __init__(self, *args, bType=BoxType.Vertical, title="Dock widget", dockFeatures=NoFeatures, scrollingEnabled=True, **kwargs):
		QDockWidget.__init__(self, *args, **kwargs)
		
		self.setWindowTitle(title)
		self.contents = Box(bType=bType, scrollingEnabled=scrollingEnabled)
		self.setWidget(self.contents)
		self.setFeatures(dockFeatures)
	
	def addWidget(self, widget, *args, **kwargs):
		self.contents.addWidget(widget, *args, **kwargs)
	
	def addLayout(self, layout, *args, **kwargs):
		self.contents.addLayout(layout, *args, **kwargs)

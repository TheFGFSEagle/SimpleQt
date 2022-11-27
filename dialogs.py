#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt

from SimpleQt.box import HBox, VBox
from SimpleQt.settings import settings

class Dialog(QDialog):
	def __init__(self, *args, buttons=QDialogButtonBox.Ok, title="Dialog", **kwargs):
		QDialog.__init__(self, *args, **kwargs)
		
		self.setWindowTitle(title)
		self.buttons = buttons
		
		self.lay = QVBoxLayout()
		self.setLayout(self.lay)
		
		self.main = QVBoxLayout()
		self.lay.addLayout(self.main)
		
		self.addButtonBox()
	
	def addWidget(self, widget):
		self.main.addWidget(widget)
	
	def addLayout(self, layout):
		self.main.addLayout(layout)
	
	def addButtonBox(self):
		self.buttonBox = QDialogButtonBox(self.buttons)
		self.buttonBox.clicked.connect(self.clicked)
		self.lay.addWidget(self.buttonBox)
	
	def clicked(self, button):
		self.destroy()

class Setting(HBox):
	changed = pyqtSignal(HBox)
	
	def __init__(self, text, path, default):
		HBox.__init__(self)
		
		self.default = default
		self.path = path
		self.unsaved = False
		
		self.label = QLabel(text)
		self.addWidget(self.label)
		
		self.changed.connect(self.onChanged)
		
	@pyqtSlot(HBox)
	def onChanged(self, setting):
		if self.value() != settings.get(self.path, self.default):
			self.unsaved = True
		else:
			self.unsaved = False
	
	def value(self):
		return self.widget.value()
	
	def setValue(self, value):
		self.widget.setValue(value)
	
	def resetToSaved(self):
		self.setValue(settings.get(self.path, self.default))
	
	def save(self):
		settings.set(self.path, self.value())

class IntegerSetting(Setting):
	def __init__(self, text, path, default):
		Setting.__init__(self, text, path, default)
		
		self.widget = QLineEdit()
		self.widget.setValidator(QIntValidator())
		self.setValue(settings.get(path, default))
		self.addWidget(self.widget)
	
		self.widget.textChanged.connect(lambda text: self.changed.emit(self))
	
	def value(self):
		return int(self.widget.text())
	
	def setValue(self, value):
		self.widget.setText(str(value))

class DoubleSetting(Setting):
	def __init__(self, text, path, default):
		Setting.__init__(self, text, path, default)
		
		self.widget = QLineEdit()
		self.widget.setValidator(QDoubleValidator())
		self.setValue(settings.get(path, default))
		self.addWidget(self.widget)
	
		self.widget.textChanged.connect(lambda text: self.changed.emit(self))
	
	def value(self):
		return float(self.widget.text())
	
	def setValue(self, value):
		self.widget.setText(str(value))

class StringSetting(Setting):
	def __init__(self, text, path, default):
		Setting.__init__(self, text, path, default)
		
		self.widget = QLineEdit()
		self.setValue(settings.get(path, default))
		self.addWidget(self.widget)
		
		self.widget.textChanged.connect(lambda text: self.changed.emit(self))
	
	def value(self):
		return str(self.widget.text())
	
	def setValue(self, value):
		self.widget.setText(str(value))

class BoolSetting(Setting):
	def __init__(self, text, path, default):
		Setting.__init__(self, text, path, default)
		
		self.widget = QCheckBox()
		self.setValue(settings.get(path, default))
		self.addWidget(self.widget)
		
		self.widget.toggled.connect(lambda checked: self.changed.emit(self))
	
	def value(self):
		return self.widget.isChecked()
	
	def setValue(self, value):
		self.widget.setChecked(bool(value))

class IntegerRangeSetting(Setting):
	def __init__(self, text, path, min, max, step, default):
		Setting.__init__(self, text, path, default)
		
		self.widget = QSpinBox()
		self.widget.setRange(min, max)
		self.widget.setSingleStep(step)
		self.setValue(settings.get(path, default))
		self.addWidget(self.widget)
	
		self.widget.valueChanged.connect(lambda value: self.changed.emit(self))
	
	def value(self):
		return int(self.widget.value())
	
	def setValue(self, value):
		self.widget.setValue(int(value))

class DoubleRangeSetting(Setting):
	def __init__(self, text, path, min, max, step, default):
		Setting.__init__(self, text, path, default)
		
		self.widget = QDoubleSpinBox()
		self.widget.setRange(min, max)
		self.widget.setSingleStep(step)
		self.setValue(settings.get(path, default))
		self.addWidget(self.widget)
	
		self.widget.valueChanged.connect(lambda value: self.changed.emit(self))
	
	def value(self):
		return float(self.widget.value())
	
	def setValue(self, value):
		self.widget.setValue(float(value))

class ChoicesSetting(Setting):
	def __init__(self, text, path, choices, default):
		Setting.__init__(self, text, path, default)
		
		self.widget = QComboBox()
		self.widget.addItems(choices)
		self.widget.setEditable(False)
		self.setValue(settings.get(path, default))
		self.addWidget(self.widget)
	
		self.widget.currentTextChanged.connect(lambda text: self.changed.emit(self))
	
	def value(self):
		return self.widget.currentText()
	
	def setValue(self, value):
		self.widget.addItem(value)
		self.widget.setCurrentText(value)

class ListSetting(Setting):
	def __init__(self, text, path, items, selectionMode, itemFlags, default=None):
		Setting.__init__(self, text, path, default)
		
		self.widget = QListWidget()
		self.widget.setSelectionMode(selectionMode)
		for item in items:
			self.widget.addItem(item)
		for i in range(self.widget.count()):
			item = self.widget.item(i)
			item.setFlags(item.flags() | itemFlags)
		self.setValue(settings.get(path, default))
		self.addWidget(self.widget)
		
		self.widget.currentRowChanged.connect(lambda text: self.changed.emit(self))
	
	def value(self):
		return self.widget.currentItem().text()
	
	def setValue(self, value):
		found = self.widget.findItems(value, Qt.MatchFixedString | Qt.MatchCaseSensitive)
		if not len(found):
			self.widget.addItem(value)
			self.widget.setCurrentRow(self.widget.count() - 1)
		else:
			self.widget.setCurrentRow(self.widget.row(found[0]))

class SettingsDialog(Dialog):
	def __init__(self, *args, **kwargs):
		Dialog.__init__(self, *args, buttons=(QDialogButtonBox.Apply | QDialogButtonBox.Ok |
											QDialogButtonBox.Reset | QDialogButtonBox.Cancel),
						title="Preferences", **kwargs)
		
		self.unsavedSettings = False
		self.buttonBox.button(QDialogButtonBox.Reset).setDisabled(True)
		
		self.items = []
	
	def onSettingChanged(self, setting):
		if setting.unsaved:
			self.unsavedSettings = True
		else:
			self.unsavedSettings = all(setting.unsaved for setting in self.items)
		self.buttonBox.button(QDialogButtonBox.Reset).setDisabled(not self.unsavedSettings)
	
	def addSetting(self, text, path, typ, default=None, **kwargs):
		setting = None
		if typ == int:
			if default == None:
				default = 0
			setting = IntegerSetting(text, path, default)
		elif typ == float:
			if default == None:
				default = 0.0
			setting = DoubleSetting(text, path, default)
		elif typ == str:
			if default == None:
				default = ""
			setting = StringSetting(text, path, default)
		elif typ == bool:
			if default == None:
				default = False
			setting = BoolSetting(text, path, default)
		elif typ == range:
			if "max" not in kwargs:
				raise TypeError("'max' keyword argument is mandatory when adding a setting with type range")
			
			min = kwargs.get("min", 0)
			max = kwargs["max"]
			step = kwargs.get("step", 1)
			
			if default == None:
				default = 0
			if type(min) == int and type(step) == int:
				setting = IntegerRangeSetting(text, path, min, int(max), step, default)
			else:
				setting = DoubleRangeSetting(text, path, float(min), float(max), float(step), float(default))
		elif typ == tuple:
			if "choices" not in kwargs:
				raise TypeError("'choices' keyword argument is mandatory when adding a setting with type tuple")
			
			if default == None:
				default = ""
			setting = ChoicesSetting(text, path, kwargs["choices"], default)
		elif typ == list:
			if "items" not in kwargs:
				raise TypeError("'items' keyword argument is mandatory when adding a setting with type list")
			items = kwargs["items"]
			selectionMode = kwargs.get("selectionMode", QListWidget.SingleSelection)
			itemFlags = kwargs.get("itemFlags", Qt.ItemIsEditable)
			setting = ListSetting(text, path, items, selectionMode, itemFlags)
		else:
			raise NotImplementedError(f"setting type {typ} is not implemented")
		
		setting.changed.connect(self.onSettingChanged)
		self.items.append(setting)
		self.addWidget(setting)
	
	def saveSettings(self):
		for setting in self.items:
			setting.save()
		self.unsavedSettings = False
		self.buttonBox.button(QDialogButtonBox.Reset).setDisabled(True)
	
	def resetSettingsToSaved(self):
		for setting in self.items:
			setting.resetToSaved()
		self.unsavedSettings = False
		self.buttonBox.button(QDialogButtonBox.Reset).setDisabled(True)
		
	def clicked(self, button):
		button = self.buttonBox.standardButton(button)
		if button in (QDialogButtonBox.Cancel, QDialogButtonBox.Reset):
			self.resetSettingsToSaved()
		elif button in (QDialogButtonBox.Apply, QDialogButtonBox.Ok):
			self.saveSettings()
		
		if button in (QDialogButtonBox.Ok, QDialogButtonBox.Cancel):
			self.destroy()


#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json
import os

class Settings:
	def __init__(self, path=None):
		self.path = path
		self.json = {}
	
	def load(self):
		if not os.path.isfile(self.path):
			self.save()
		with open(self.path, "r") as f:
			try:
				self.json = json.load(f)
			except json.decoder.JSONDecodeError:
				self.json = {}
	
	def save(self):
		with open(self.path, "w") as f:
			json.dump(self.json, f)
	
	def _pathToDirsName(self, path):
		dirs = list(filter(None, path.split("/")))
		if len(dirs) > 1:
			dirs, name = dirs[:-1], dirs[-1]
		else:
			dirs, name = [], dirs[0]
		return dirs, name
	
	def _getDirName(self, path):
		d = self.json
		dirs, name = self._pathToDirsName(path)
		i = 0
		while i < len(dirs):
			new_d = d.get(dirs[i], None)
			if new_d == None:
				d[dirs[i]] = {}
			d = d[dirs[i]]
			i += 1
		
		return d, name
	
	def get(self, path, default=None):
		d, name = self._getDirName(path)
		value = d.get(name, None)
		if value == None:
			value = d[name] = default
		return value
	
	def set(self, path, value):
		d, name = self._getDirName(path)
		d[name] = value
	
	def remove(self, path):
		d, name = self._getDirName(path)
		d.pop(name, None)

settings = Settings()


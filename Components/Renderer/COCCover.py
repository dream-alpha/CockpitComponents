#!/usr/bin/python
# encoding: utf-8
#
# Copyright (C) 2018-2022 by dream-alpha
#
# In case of reuse of this source code please do not remove this copyright.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# For more information on the GNU General Public License see:
# <http://www.gnu.org/licenses/>.


from enigma import ePixmap, gPixmapPtr
from Components.Renderer.Renderer import Renderer


class COCCover(Renderer):
	GUI_WIDGET = ePixmap

	def __init__(self):
		self.skinAttributes = None
		Renderer.__init__(self)
		self.type = "cover"

	def destroy(self):
		Renderer.destroy(self)

	def applySkin(self, desktop, parent):
		attribs = self.skinAttributes
		for (attrib, value) in self.skinAttributes:
			if attrib == "type":
				self.type = value
				attribs.remove((attrib, value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	def changed(self, what):
		if self.instance is not None:
			if what[0] != self.CHANGED_CLEAR:
				self.instance.setPixmap(self.source.cover)
			else:
				self.instance.setPixmap(gPixmapPtr())

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


import os
from enigma import ePixmap
from enigma import eServiceReference
from Components.config import config
from Components.Renderer.Renderer import Renderer
from Components.Sources.CurrentService import CurrentService
from Plugins.Extensions.MovieCockpit.MovieCoverUtils import getCoverPath
from Plugins.Extensions.MovieCockpit.SkinUtils import getSkinPath


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

	def getServicePath(self):
		path = None
		service_reference = self.source.service
		if isinstance(self.source, CurrentService):
			service_reference = self.source.navcore.getCurrentlyPlayingServiceReference()
		if isinstance(service_reference, eServiceReference):
			path = service_reference.getPath()
		return path

	def changed(self, what):
		if config.plugins.moviecockpit.cover_show.value and self.instance is not None:
			if what[0] != self.CHANGED_CLEAR:
				service_path = self.getServicePath()
				if service_path:
					cover_path, backdrop_path, _info_path = getCoverPath(service_path)
					if not os.path.exists(cover_path) and config.plugins.moviecockpit.cover_fallback.value:
						cover_path = getSkinPath("images/no_cover.png")
					if self.type == "backdrop":
						pixmap_path = backdrop_path
					else:
						pixmap_path = cover_path
					self.instance.setPixmapFromFile(pixmap_path)
					if os.path.exists(pixmap_path) and os.path.isfile(service_path):
						self.instance.show()
					else:
						self.instance.hide()

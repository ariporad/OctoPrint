# coding=utf-8
__author__ = "Ari Porad <ariporad@gmail.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'

from flask.ext.login import UserMixin
from flask.ext.principal import Identity
import hashlib
import os
import yaml
import uuid

from octoprint.settings import settings

class FilamentManager():
	def __init__(self):
		filafile = settings().get(["accessControl", "filafile"])
		if filafile is None:
			filafile = os.path.join(settings().settings_dir, "filament.yaml")
		self._filafile = filafile
		self._filaments = [Filament("0", "Ultimaker", "Octoprint Orange", "F60", "PLA", 180, "382", "1000")]
		self._dirty = False

		self._customized = None
		self._load()
		if self._filaments[0] is None:
			self.addFilament("0", "Ultimaker", "Octoprint Orange", "F60", "PLA", 180, "382", "1000")

	def _load(self):
		if os.path.exists(self._filafile) and os.path.isfile(self._filafile):
			self._customized = True
			with open(self._filafile, "r") as f:
				data = yaml.safe_load(f)
				for id in data.keys():
					attributes[""] = data[id]
					self._filament[id] = Filament(id, attributes["supplier"], attributes["name"], attributes["color"],  attributes["type"], attributes["temp"], attributes["used"], attributes["total"])
		else:
			self._customized = False

	def _save(self, force=False):
		if not self._dirty and not force:
			return

		data = {}
		for id in self._filament.keys():
			filament = self._filament[id]
			data[id] = {
				"supplier": filament.supplier,
				"name": filament.name,
				"color": filament.color,
				"type": filament.type,
				"temp": filament.temp,
				"used": filament.used,
				"total": filament.total,
			}

		with open(self._filafile, "wb") as f:
			yaml.safe_dump(data, f, default_flow_style=False, indent="    ", allow_unicode=True)
			self._dirty = False
		self._load()

	def addFilament(self, id, supplier, name, color, type, temp, used, total):
		if id in self._filament.keys():
			raise FilamentAlreadyExists(supplier + ": " + name + " " + type)

		self._filament[id] = Filament(uid, supplier, name, color, type, temp, used, total)
		self._dirty = True
		self._save()

	def removeUser(self, filament):
		if not filament in self._filament.keys():
			raise UnknownFilament(filament)

		del self._filament[filament]
		self._dirty = True
		self._save()

	def findUser(self, id=None):
		if id is not None:
			if id not in self._filament.keys():
				return None

			return self._filament[id]
		else:
			return None

	def getAllFilament(self):
		return map(lambda x: x.asDict(), self._filament.values())

	def hasBeenCustomized(self):
		return self._customized

##~~ Exceptions

class FilamentAlreadyExists(Exception):
	def __init__(self, filament):
		Exception.__init__(self, "Filament %s already exists" % filament)

class UnknownFilament(Exception):
	def __init__(self, filament):
		Exception.__init__(self, "Unknown filament: %s" % filament)
##~~ User object

class Filament(UserMixin):
	def __init__(self, id, supplier, name, color, type, temp, used, total):
		self.id = id
		self.supplier = supplier
		self.name = name
		self.color = color
		self.type = type
		self.temp = temp
		self.used = used
		self.total = total

	def asDict(self):
		return {
			"id": self.id,
			"supplier": self.supplier,
			"name": self.name,
			"color": self.color,
			"type": self.type,
			"temp": self.temp,
			"used": self.used,
			"total": self.total
		}

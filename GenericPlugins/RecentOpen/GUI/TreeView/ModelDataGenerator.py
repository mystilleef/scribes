from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager

TEMPLATE = "<big><b>%s</b></big>\n<span foreground='dark grey'><i>in</i></span> <span stretch='expanded'>%s</span>\n<small><span foreground='dark grey'><i>modified</i></span>  <span foreground='brown'><b>%s</b></span>  <span foreground='navy blue'><b>%s %s file</b></span></small>"

class Generator(SignalManager):

	def __init__(self, manager, editor):
		editor.refresh()
		SignalManager.__init__(self, editor)
		self.__init_attributes(editor, manager)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "filtered-data", self.__data_cb)
		editor.refresh()

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		self.__data = []
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __format(self, data):
		self.__editor.refresh(False)
		file_path, icon, display_name, display_path, modified, location, filetype, uri = data
		display_info = TEMPLATE % (display_name, display_path, modified, location, filetype)
		return icon, display_info, uri

	def __process(self, filtered_data):
		try:
			if filtered_data == self.__data: raise ValueError
			from copy import copy
			self.__data = copy(filtered_data)
			data = (self.__format(data) for data in filtered_data)
			self.__manager.emit("model-data", data)
		except ValueError:
			self.__manager.emit("selected-row")
		return False

	def __process_timeout(self, filtered_data):
		from gobject import idle_add
		self.__timer = idle_add(self.__process, filtered_data)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __data_cb(self, manager, filtered_data):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = idle_add(self.__process, filtered_data)
		return False

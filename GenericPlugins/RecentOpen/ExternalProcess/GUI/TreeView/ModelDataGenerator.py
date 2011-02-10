from SCRIBES.SignalConnectionManager import SignalManager

TEMPLATE = "<big><b>%s</b></big>\n<span foreground='dark grey'><i>in</i></span> <span stretch='expanded'>%s</span>\n<small><span foreground='dark grey'><i>modified</i></span>  <span foreground='brown'><b>%s</b></span>  <span foreground='navy blue'><b>%s %s file</b></span></small>"

class Generator(SignalManager):

	def __init__(self, manager):
		SignalManager.__init__(self)
		self.__init_attributes(manager)
		self.connect(manager, "filtered-data", self.__data_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__data = []
		return

	def __format(self, data):
		self.__manager.response()
		file_path, icon, display_name, display_path, modified, location, filetype, uri = data
		display_info = TEMPLATE % (display_name, display_path, modified, location, filetype)
		self.__manager.response()
		return icon, display_info, uri

	def __process(self, filtered_data):
		try:
			self.__manager.response()
			if filtered_data == self.__data: raise ValueError
			self.__data = filtered_data
			data = (self.__format(data) for data in filtered_data)
			self.__manager.emit("model-data", data)
		except ValueError:
			self.__manager.emit("selected-row")
		return False

	def __process_timeout(self, filtered_data):
		from gobject import idle_add
		idle_add(self.__process, filtered_data)
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

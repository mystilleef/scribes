class Updater(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("model-data", self.__data_cb)
		self.__sigid3 = manager.connect("filtered-files", self.__files_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = manager.gui.get_object("TreeView")
		self.__model = self.__view.get_model()
		self.__column1 = self.__view.get_column(0)
		self.__column2 = self.__view.get_column(1)
		self.__data = []
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return False

	def __populate(self, data):
		if self.__data == data: return False
		from copy import copy
		self.__data = copy(data)
		self.__view.set_model(None)
		self.__model.clear()
		for name, path in data:
			self.__model.append([name, path])
		self.__column1.queue_resize()
		self.__column2.queue_resize()
		self.__view.set_model(self.__model)
		self.__manager.emit("updated-model")
		return False

	def __clear(self):
		self.__view.set_model(None)
		self.__model.clear()
		self.__view.set_model(self.__model)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __data_cb(self, manager, data):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = idle_add(self.__populate, data)
		return False

	def __files_cb(self, manager, files):
		if not files: self.__clear()
		return False

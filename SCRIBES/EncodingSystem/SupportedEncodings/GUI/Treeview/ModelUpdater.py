class Updater(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("model-data", self.__model_cb)
		self.__sigid3 = manager.connect("encoding-list", self.__encodings_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = manager.gui.get_widget("TreeView")
		self.__model = self.__view.get_model()
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __populate(self, data):
		self.__view.set_model(None)
		for active, encoding, language in data:
			self.__editor.response()
			self.__model.append([False, encoding, language])
		self.__view.set_model(self.__model)
		return False

	def __update(self, encodings):
		self.__view.set_model(None)
		for row in xrange(len(self.__model)):
			self.__editor.response()
			treemodelrow = self.__model[row]
			value = True if treemodelrow[1] in encodings else False
			treemodelrow[0] = value
		self.__view.set_model(self.__model)
		self.__manager.emit("updated-model")
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __model_cb(self, manager, data):
		self.__populate(data)
		return False

	def __encodings_cb(self, manager, encodings):
		from gobject import idle_add
		idle_add(self.__update, encodings)
		return False

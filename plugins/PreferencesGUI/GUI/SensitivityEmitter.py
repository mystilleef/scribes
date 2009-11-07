class Emitter(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("selected-language", self.__selected_cb)
		self.__sigid3 = self.__combo.connect("changed", self.__changed_cb)
		self.__sigid4 = manager.connect("reset", self.__changed_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__combo = manager.gui.get_object("LanguageComboBox")
		return

	def __destroy(self):
		signals_data = (
			(self.__sigid1, self.__manager),
			(self.__sigid2, self.__manager),
			(self.__sigid3, self.__combo),
			(self.__sigid4, self.__manager),
		)
		self.__editor.disconnect_signals(signals_data)
		del self
		self = None
		return False

	def __sensitive(self, sensitive=True):
		self.__manager.emit("sensitive", sensitive)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		self.__sensitive(False)
		return False

	def __selected_cb(self, *args):
		self.__sensitive()
		return False

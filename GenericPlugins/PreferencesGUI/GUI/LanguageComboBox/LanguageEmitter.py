class Emitter(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__combo.connect_after("changed", self.__changed_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__combo = manager.gui.get_object("LanguageComboBox")
		self.__model = self.__combo.get_model()
		return

	def __destroy(self):
		signals_data = (
			(self.__sigid1, self.__manager),
			(self.__sigid2, self.__combo),
		)
		self.__editor.disconnect_signals(signals_data)
		del self
		self = None
		return False

	def __emit(self):
		iterator = self.__combo.get_active_iter()
		language = self.__model.get_value(iterator, 1)
		self.__manager.emit("selected-language", language)
		return False

	def __delayed_emit(self):
		try:
			from gobject import timeout_add, source_remove
			source_remove(self.__timer1)
		except AttributeError:
			pass
		finally:
			self.__timer1 = timeout_add(250, self.__emit, priority=9999)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = idle_add(self.__delayed_emit, priority=9999)
		return False

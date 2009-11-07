class Selector(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("updated-language-combobox", self.__updated_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__combo = manager.gui.get_object("LanguageComboBox")
		self.__model = self.__combo.get_model()
		return

	def __destroy(self):
		signals_data = (
			(self.__sigid1, self.__manager),
			(self.__sigid2, self.__manager),
		)
		self.__editor.disconnect_signals(signals_data)
		del self
		self = None
		return False

	def __select(self):
		language = self.__editor.language if self.__editor.language else "plain text"
		_row = -1
		for row in self.__model:
			self.__editor.response()
			_row += 1
			if language == row[1]: break
		self.__combo.set_active(_row)
		self.__combo.set_property("sensitive", True)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __updated_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__select)
		return False

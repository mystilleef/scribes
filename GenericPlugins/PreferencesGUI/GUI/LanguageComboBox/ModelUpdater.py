from gettext import gettext as _

class Updater(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("language-combobox-data", self.__data_cb)

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

	def __update(self, data):
		self.__combo.set_model(None)
		self.__model.clear()
		self.__model.append([_("Plain Text"), "plain text"])
		for language_name, language_id in data:
			self.__model.append([language_name, language_id])
		self.__combo.set_model(self.__model)
		self.__manager.emit("updated-language-combobox")
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __data_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__update, data, priority=9999)
		return False

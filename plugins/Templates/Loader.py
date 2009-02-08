class Loader(object):

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__signal_id_1 = manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_2 = editor.connect("loaded-file", self.__loaded_document_cb)
		self.__signal_id_3 = editor.connect("renamed-file", self.__loaded_document_cb)
		self.__signal_id_4 = manager.connect("database-update", self.__changed_cb)
		self.__load_templates()

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		from Metadata import get_value
		self.__dictionary = get_value()
		return

	def __load_general_templates(self):
		general = {}
		for element in self.__dictionary.keys():
			if not element.startswith("General|"): continue
			nelement = "General" + element[len("General|"):]
			general[nelement] = self.__dictionary[element][1]
		self.__manager.emit("loaded-general-templates", general)
		return

	def __load_language_templates(self):
		self.__manager.emit("loaded-language-templates", {})
		if self.__editor.uri is None: return
		language = self.__editor.language
		if not language: return
		language_id = language
		string = language_id + "|"
		language = {}
		for element in self.__dictionary.keys():
			if not element.startswith(string): continue
			nelement = language_id + element[len(string):]
			language[nelement] = self.__dictionary[element][1]
		self.__manager.emit("loaded-language-templates", language)
		return

	def __load_templates(self):
		from Metadata import get_value
		self.__dictionary = get_value()
		self.__load_general_templates()
		self.__load_language_templates()
		return

	def __destroy_cb(self, manager):
		self.__editor.disconnect_signal(self.__signal_id_1, manager)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_4, manager)
		del self
		self = None
		return

	def __loaded_document_cb(self, *args):
		self.__load_language_templates()
		return

	def __changed_cb(self, *args):
		self.__load_templates()
		return

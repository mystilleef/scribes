class Generator(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("show-add-template-editor", self.__add_cb)
		self.__sigid3 = manager.connect("show-edit-template-editor", self.__edit_cb)
		self.__sigid4 = manager.connect("selected-language-id", self.__language_id_cb)
		self.__sigid5 = manager.connect("selected-templates-dictionary-key", self.__dictionary_key_cb)
		self.__sigid6 = manager.connect("templates-dictionary", self.__templates_dictionary_cb)
		editor.response()
		
	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__language = None
		self.__key = None
		self.__dictionary = {}
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		del self
		self = None
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __send_triggers(self, edit=False):
		try:
			if not self.__dictionary: raise ValueError
			language = self.__language + "|"
			triggers = [key[len(language):] for key in self.__dictionary.keys() if key.startswith(language)]
			if edit: triggers.remove(self.__key[len(language):])
			self.__manager.emit("template-triggers", triggers)
		except ValueError:
			self.__manager.emit("template-triggers", [])
		return False

	def __add_cb(self, *args):
		self.__send_triggers()
		return False

	def __edit_cb(self, *args):
		self.__send_triggers(True)
		return False

	def __language_id_cb(self, manager, language):
		self.__language = language
		return False

	def __dictionary_key_cb(self, manager, key):
		self.__key = key
		return False

	def __templates_dictionary_cb(self, manager, dictionary):
		self.__dictionary = dictionary
		return False

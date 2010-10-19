class Generator(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("show-add-template-editor", self.__add_cb)
		self.__sigid3 = manager.connect("show-edit-template-editor", self.__edit_cb)
		self.__sigid4 = manager.connect("selected-language-id", self.__language_id_cb)
		self.__sigid5 = manager.connect("selected-templates-dictionary-key", self.__dictionary_key_cb)
		self.__sigid6 = manager.connect("gui-template-editor-data", self.__data_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__language = None
		self.__key = None
		self.__should_remove_old_key = False
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

	def __generate_template(self, data):
		trigger, description, template = data
		new_key = self.__language + "|" + trigger
		old_key = self.__key if self.__should_remove_old_key else None
		template_data = old_key, new_key, description, template
		self.__manager.emit("new-template-data", template_data)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __add_cb(self, *args):
		self.__should_remove_old_key = False
		return False

	def __edit_cb(self, *args):
		self.__should_remove_old_key = True
		return False

	def __language_id_cb(self, manager, language):
		self.__language = language
		return False

	def __dictionary_key_cb(self, manager, key):
		self.__key = key
		return False

	def __data_cb(self, manager, data):
		self.__generate_template(data)
		return False

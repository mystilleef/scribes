class Initializer(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("show-add-template-editor", self.__add_cb)
		self.__sigid3 = manager.connect("show-edit-template-editor", self.__edit_cb)
		self.__sigid4 = manager.connect_after("validator-is-ready", self.__is_ready_cb)
		self.__sigid5 = manager.connect("templates-dictionary", self.__dictionary_cb)
		self.__sigid6 = manager.connect("selected-templates-dictionary-key", self.__key_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__name_entry = manager.editor_gui.get_widget("NameEntry")
		self.__description_entry = manager.editor_gui.get_widget("DescriptionEntry")
		self.__buffer = manager.editor_gui.get_widget("ScrolledWindow").get_child().get_buffer()
		self.__show = None
		self.__dictionary = {}
		self.__key = ""
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

	def __initialize_widgets_for_adding(self):
		self.__set_widget()
		return False

	def __initialize_widgets_for_editing(self):
		description, template = self.__dictionary[self.__key]
		trigger = self.__key.split("|")[-1]
		self.__set_widget(trigger, description, template)
		return False

	def __set_widget(self, trigger="", description="", template=""):
		self.__name_entry.set_text(trigger)
		self.__description_entry.set_text(description)
		self.__buffer.set_text(template)
		self.__name_entry.grab_focus()
		self.__manager.emit("ready")
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __add_cb(self, *args):
		self.__show = self.__initialize_widgets_for_adding
		return False

	def __edit_cb(self, *args):
		self.__show = self.__initialize_widgets_for_editing
		return False

	def __is_ready_cb(self, *args):
		self.__show()
		return False

	def __dictionary_cb(self, manager, dictionary):
		self.__dictionary = dictionary
		return False

	def __key_cb(self, manager, key):
		self.__key = key
		return False

class Updater(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("new-template-data", self.__data_cb)
		self.__sigid3 = manager.connect("database-update", self.__updated_cb)
		self.__sigid4 = manager.connect("remove-template-data", self.__remove_data_cb)
		self.__sigid5 = manager.connect("new-imported-templates", self.__imported_cb)
		self.__emit_new_dictionary_signal()
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__dictionary = {}
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return False
	
	def __emit_new_dictionary_signal(self):
		from Metadata import get_value
		self.__dictionary = get_value()
		self.__manager.emit("templates-dictionary", self.__dictionary)
		return False

	def __add_template_to_database(self, template_data):
		old_key, new_key, description, template = template_data
		if old_key: del self.__dictionary[old_key]
		self.__dictionary[new_key] = description, template
		from Metadata import set_value
		set_value(self.__dictionary)
		return False

	def __add_new_templates(self, templates_data):
		for data in templates_data: self.__dictionary[data[0]] = data[1], data[2]
		from Metadata import set_value
		set_value(self.__dictionary)
		return False

	def __remove(self, data):
		for key in data: del self.__dictionary[key]
		from Metadata import set_value
		set_value(self.__dictionary)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __data_cb(self, manager, template_data):
		self.__add_template_to_database(template_data)
		return False

	def __updated_cb(self, *args):
		self.__emit_new_dictionary_signal()
		return False

	def __remove_data_cb(self, manager, data):
		self.__remove(data)
		return False

	def __imported_cb(self, manager, data):
		self.__add_new_templates(data)
		return False

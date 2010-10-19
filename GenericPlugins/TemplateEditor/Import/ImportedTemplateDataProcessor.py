class Processor(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("templates-dictionary", self.__dictionary_cb)
		self.__sigid3 = manager.connect("imported-templates-data", self.__imported_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__dictionary = {}
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return False

	def __modify_template_key(self, data):
		if data[-1] == self.__dictionary[data[0]][-1]: return data
		key = data[0]
		new_key = data[0]
		count = 0
		keys = self.__dictionary.keys()
		while new_key in keys:
			count += 1
			new_key = key + "-" + str(count)
		data = new_key, data[1], data[2]
		return data

	def __create_new_data(self, templates_data):
		keys = self.__dictionary.keys()
		templates_data = reduce(lambda x,y: x+y, templates_data)
		new_templates_data = [data for data in templates_data if not (data[0] in keys)]
		duplicate_templates_data = [self.__modify_template_key(data) for data in templates_data if (data[0] in keys)]
		templates_data = new_templates_data + duplicate_templates_data
		self.__manager.emit("validate-imported-templates", templates_data)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __dictionary_cb(self, manager, dictionary):
		self.__dictionary = dictionary
		return

	def __imported_cb(self, manager, data):
		self.__create_new_data(data)
		return False

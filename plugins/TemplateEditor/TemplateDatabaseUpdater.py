class Updater(object):
	"""
	This class updates the template database with data imported from the
	template xml file.
	"""

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("template-data", self.__update_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __insert_data(self, database, data):
		key, description, template = data
		if database.has_key(key):
			if database[key][1] == template: return False
			count = 0
			while True:
				count += 1
				key_ = key + "-" + str(count)
				if database.has_key(key_): continue
				break
			key = key_
		database[key] = description, template
		return False

	def __update_database(self, data):
		from Metadata import open_template_database
		database = open_template_database("w")
		for data_ in data:
			self.__insert_data(database, data_)
		database.close()
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __update_cb(self, manager, data):
		self.__update_database(data)
		language_id = data[-1][0].split("|")[0]
		self.__manager.emit("select-langauge", language_id)
		return False

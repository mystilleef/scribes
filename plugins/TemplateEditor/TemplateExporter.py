class Exporter(object):
	"""
	This class collects and formats template information to be exported.

	Template data format:

		[(language, trigger, description, template), ...]
	"""

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("process-templates-for-export", self.__process_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __update_data(self, database, append, key):
		try:
			data = key.split("|")
			language, trigger = data[0], data[1]
			description, template = database[key]
			data = language, trigger, description, template
			append(data)
		except:
			pass
		return False

	def __send_template_data(self, keys):
		from Metadata import open_template_database
		database = open_template_database("r")
		data = []
		append = data.append
		for key in keys:
			self.__update_data(database, append, key)
		database.close()
		self.__manager.emit("processed-template-data", data)
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __process_cb(self, manager, keys):
		self.__send_template_data(keys)
		return False

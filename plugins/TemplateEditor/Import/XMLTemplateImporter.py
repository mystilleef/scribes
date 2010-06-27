class Importer(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("valid-template-files", self.__process_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		return

	def __get_data(self, entry):
		try:
			nodes = entry.getchildren()
			id_ = nodes[0].attrib.values()[0]
			trigger = nodes[0].text
			description = nodes[1].text
			template = nodes[2].text
			key = id_ + "|" + trigger
			data = key, description, template
		except:
			return None
		return data

	def __get_entries(self, file_):
		from xml.etree.ElementTree import parse
		xmlobj = parse(file_)
		node = xmlobj.getroot()
		nodes = node.getchildren()
		entries = nodes[0].getchildren()
		return entries

	def __get_template_data(self, file_):
		entries = self.__get_entries(file_)
		data = [self.__get_data(entry) for entry in entries]
		return data

	def __send_template_data(self, files):
		import_data = [self.__get_template_data(_file) for _file in files]
		self.__manager.emit("imported-templates-data", import_data)
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

	def __process_cb(self, manager, files):
		self.__send_template_data(files)
		return False

class Importer(object):
	"""
	This class is responsible for converting the xml template data into a
	convenient format that will be used to update the template database.
	"""

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("valid-xml-templates", self.__process_cb)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		return

	def __get_id_from_entry(self, nodes):
		return nodes[0].attrib.values()[0]

	def __get_trigger_from_entry(self, nodes):
		return nodes[0].text

	def __get_description_from_entry(self, nodes):
		return nodes[1].text

	def __get_template_from_entry(self, nodes):
		return nodes[2].text

	def __get_data_from_entry(self, entry):
		try:
			nodes = entry.getchildren()
			id_ = self.__get_id_from_entry(nodes)
			trigger = self.__get_trigger_from_entry(nodes)
			description = self.__get_description_from_entry(nodes)
			template = self.__get_template_from_entry(nodes)
			key = id_ + "|" + trigger
			data = key, description, template
		except:
			return None
		return data

	def __get_data_from_entries(self, data, entries):
		for entry in entries:
			data_ = self.__get_data_from_entry(entry)
			if data_: data.append(data_)
		return data

	def __get_entries(self, file_):
		from xml.etree.ElementTree import parse
		xmlobj = parse(file_)
		node = xmlobj.getroot()
		nodes = node.getchildren()
		entries = nodes[0].getchildren()
		return entries

	def __get_template_data(self, data, file_):
		entries = self.__get_entries(file_)
		data = self.__get_data_from_entries(data, entries)
		return data

	def __convert(self, files):
		template_data = []
		for file_ in files:
			template_data = self.__get_template_data(template_data, file_)
		if not template_data: return False
		self.__manager.emit("template-data", template_data)
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
		self.__convert(files)
		return False

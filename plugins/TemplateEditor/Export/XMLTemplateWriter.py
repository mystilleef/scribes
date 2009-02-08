class Writer(object):

	def __init__(self, manager, editor):
		self.__init_attribute(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("export-template-data", self.__process_cb)
		self.__sigid3 = manager.connect("create-export-template-filename", self.__filename_cb)

	def __init_attribute(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__filename = None
		return

	def __add(self, snippet, data, SubElement):
		entry = SubElement(snippet, "entry")
		SubElement(entry, "trigger", id=data[0]).text = data[1]
		SubElement(entry, "description").text = data[2]
		SubElement(entry, "template").text = data[3]
		return

	def __create_xml_template_file(self, template_data):
		from xml.etree.ElementTree import Element, SubElement, ElementTree
		root = Element("scribes", version="0.1")
		snippet = SubElement(root, "snippet")
		[self.__add(snippet, data, SubElement) for data in template_data]
		ElementTree(root).write(self.__filename, "UTF-8")
		self.__manager.emit("created-xml-template-file")
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __process_cb(self, manager, template_data):
		self.__create_xml_template_file(template_data)
		return False

	def __filename_cb(self, manager, filename):
		self.__filename = filename
		return False

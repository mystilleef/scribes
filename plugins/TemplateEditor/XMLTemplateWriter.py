class Writer(object):
	"""
	This is terminal
	responsible for creating xml template file
	"processed-template-data"
	"destroy"
	"export-template-filename"
	"""

	def __init__(self, manager, editor):
		self.__init_attribute(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("processed-template-data", self.__process_cb)
		self.__sigid3 = manager.connect("export-template-filename", self.__filename_cb)

	def __init_attribute(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__filename = None
		return

	def __add_entry_element(self, snippet, data_, SubElement):
		entry = SubElement(snippet, "entry")
		SubElement(entry, "trigger", id=data_[0]).text = data_[1]
		SubElement(entry, "description").text = data_[2]
		SubElement(entry, "template").text = data_[3]
		return

	def __create_xml_template_file(self, data):
		from xml.etree.ElementTree import Element, SubElement, ElementTree
		root = Element("scribes", version="0.1")
		snippet = SubElement(root, "snippet")
		for data_ in data:
			self.__add_entry_element(snippet, data_, SubElement)
		ElementTree(root).write(self.__filename)
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

	def __process_cb(self, manager, data):
		self.__create_xml_template_file(data)
		return False

	def __filename_cb(self, manager, filename):
		self.__filename = filename
		return False

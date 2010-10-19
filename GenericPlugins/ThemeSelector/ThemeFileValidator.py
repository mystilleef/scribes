from SCRIBES.SignalConnectionManager import SignalManager

class Validator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(editor, manager)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "process-xml-files", self.__process_cb)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __validate(self, filenames):
		try:
			from os.path import isfile
			filenames = filter(isfile, filenames)
			if not filenames: raise ValueError
			filenames = filter(self.__is_xml, filenames)
			if not filenames: raise ValueError
			filenames = filter(self.__is_color_scheme, filenames)
			if not filenames: raise ValueError
			self.__manager.emit("valid-scheme-files", filenames)
		except ValueError:
			self.__manager.emit("invalid-scheme-files")
		return False

	def __is_xml(self, _file):
		xml_mime_types = ("application/xml", "text/xml")
		return self.__editor.get_mimetype(_file) in xml_mime_types

	def __is_color_scheme(self, file_):
		root_node = self.__get_xml_root_node(file_)
		if root_node.tag != "style-scheme": return False
		attribute_names = root_node.keys()
		if not ("id" in attribute_names): return False
		if not ("_name" in attribute_names): return False
		return True

	def __get_xml_root_node(self, file_):
		try:
			from xml.parsers.expat import ExpatError
			from xml.etree.ElementTree import parse
			xmlobj = parse(file_)
			node = xmlobj.getroot()
		except ExpatError:
			raise ValueError
		return node

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __process_cb(self, manager, filenames):
		from gobject import idle_add
		idle_add(self.__validate, filenames, priority=9999)
		return False

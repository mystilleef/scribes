class Validator(object):
	"""
	This class creates an instance that validates XML template files for
	Scribes. The "valid-xml-templates" signal is emitted if there are any
	valid xml template files. The "invalid-xml-templates" signal is emitted
	if there are any invalid xml template files.
	"""

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("process-imported-files", self.__process_cb)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		return

	def __is_xml(self, file_):
		from gnomevfs import get_mime_type
		xml_mime_types = ("application/xml", "text/xml")
		return get_mime_type(file_) in xml_mime_types

	def __get_xml_root_node(self, file_):
		try:
			from xml.parsers.expat import ExpatError
			from xml.etree.ElementTree import parse
			xmlobj = parse(file_)
			node = xmlobj.getroot()
		except ExpatError:
			raise ValueError
		return node

	def __is_scribes_template(self, file_):
		if not self.__is_xml(file_): return False
		root_node = self.__get_xml_root_node(file_)
		if root_node.tag != "scribes": return False
		attribute_names = root_node.keys()
		if not ("version" in attribute_names): return False
		nodes = root_node.getchildren()
		if len(nodes) != 1: return False
		if nodes[0].tag != "snippet": return False
		if not nodes[0].getchildren(): return False
		return True

	def __is_valid_template_file(self, file_):
		try:
			if not self.__is_scribes_template(file_): return False
		except ValueError:
			return False
		return True

	def __validate(self, files):
		valid_files = []
		invalid_files = []
		for file_ in files:
			valid = self.__is_valid_template_file(file_)
			valid_files.append(file_) if valid else invalid_files.append(file_)
		if valid_files: self.__manager.emit("valid-xml-templates", valid_files)
		if invalid_files: self.__manager.emit("invalid-xml-templates", invalid_files)
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

	def __process_cb(self, manager, files):
		self.__validate(files)
		return False

from gettext import gettext as _
ERROR_MESSAGE = _("ERROR: No valid template files found")

class Validator(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("process-imported-files", self.__process_cb)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		return

	def __is_xml(self, file_):
		xml_mime_types = ("application/xml", "text/xml")
		return self.__editor.get_mimetype(file_) in xml_mime_types

	def __get_xml_root_node(self, file_):
		try:
			from xml.parsers.expat import ExpatError
			from xml.etree.ElementTree import parse
			xmlobj = parse(file_)
			node = xmlobj.getroot()
		except ExpatError:
			return None
		return node

	def __is_valid(self, _file):
		if not self.__is_xml(_file): return False
		root_node = self.__get_xml_root_node(_file)
		if root_node.tag != "scribes": return False
		attribute_names = root_node.keys()
		if not ("version" in attribute_names): return False
		nodes = root_node.getchildren()
		if len(nodes) != 1: return False
		if nodes[0].tag != "snippet": return False
		if not nodes[0].getchildren(): return False
		return True

	def __validate(self, files):
		valid_files = [_file for _file in files if self.__is_valid(_file)]
		if valid_files: self.__manager.emit("valid-template-files", valid_files)
		if not valid_files: self.__manager.emit("error", ERROR_MESSAGE)
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

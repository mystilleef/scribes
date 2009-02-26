class Validator(object):

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("process-xml-files", self.__process_cb)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
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
			from gettext import gettext as _
			message = _("No valid scheme file found")
			self.__manager.emit("error-message", message)
		return False

	def __is_xml(self, _file):
		from gnomevfs import get_mime_type
		xml_mime_types = ("application/xml", "text/xml")
		return get_mime_type(_file) in xml_mime_types

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
		idle_add(self.__validate, filenames)
		return False

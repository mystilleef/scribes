from gettext import gettext as _
ERROR_MESSAGE = _("ERROR: No valid templates found")

class Validator(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("validate-imported-templates", self.__validate_cb)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __is_valid(self, string):
		string = string.strip()
		if not string: return False
		chars = (" ", "\t", "(", "{", "<", "[", "=", ")", "}", ">", "]")
		for char in string:
			if char in chars: return False
		return True

	def __validate(self, data):
		templates_data = [_data for _data in data if self.__is_valid(_data[0])]
		if templates_data: self.__manager.emit("new-imported-templates", templates_data)
		if not templates_data: self.__manager.emit("error", ERROR_MESSAGE)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __validate_cb(self, manager, data):
		self.__validate(data)
		return False

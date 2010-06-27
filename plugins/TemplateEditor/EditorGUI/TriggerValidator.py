class Validator(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("name-entry-string", self.__string_cb)
		self.__sigid3 = manager.connect("template-triggers", self.__template_triggers_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__triggers = []
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return False

	def __is_valid(self, string):
		string = string.strip()
		if not string: return False
		chars = (" ", "\t", "(", "{", "<", "[", "=", ")", "}", ">", "]", "|")
		for char in string:
			if char in chars: return False
		return True

	def __is_duplicate(self, string):
		return string in self.__triggers

	def __validate(self, string):
		try:
			if self.__is_duplicate(string): raise ValueError
			if self.__is_valid(string) is False: raise ValueError
			self.__manager.emit("valid-trigger", True)
		except ValueError:
			self.__manager.emit("valid-trigger", False)
		return True

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __string_cb(self, manager, string):
		self.__validate(string)
		return False

	def __template_triggers_cb(self, manager, triggers):
		self.__triggers = triggers
		self.__manager.emit("validator-is-ready")
		return False

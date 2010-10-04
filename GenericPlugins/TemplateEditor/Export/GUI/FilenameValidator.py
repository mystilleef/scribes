class Validator(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("validate-export-template-path", self.__validate_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __validate(self, filename):
		try:
			from os.path import split
			folder, name = split(filename)
			if not name: raise ValueError
			if not name.endswith(".xml"): raise ValueError
			if not name[:-4]: raise ValueError
			if " " in name: raise ValueError
			from os import access, W_OK
			if not access(folder, W_OK): raise ValueError
			self.__manager.emit("hide-export-window")
			self.__manager.emit("create-export-template-filename", filename)
		except ValueError:
			print "Validation error"
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __validate_cb(self, manager, filename):
		self.__validate(filename)
		return False

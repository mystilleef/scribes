class Validator(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("validate", self.__validate_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__chooser = manager.gui.get_object("FileChooser")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __validate(self):
		uri = self.__chooser.get_uri()
		if not uri: return False
		from gio import File 
		text = File(uri).get_basename()
		if not text: return False
		if "/" in text: return False
		if len(text) > 256: return False
		if self.__editor.uri_is_folder(uri): return False
		self.__manager.emit("rename")
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __validate_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__validate)
		return False

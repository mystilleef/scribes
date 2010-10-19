from gettext import gettext as _

class Creator(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("create-file", self.__create_file_cb)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return

	def __create_file(self, name):
		try:
			from Utils import get_new_uri
			uri = get_new_uri(self.__editor, name)
			self.__editor.create_uri(uri)
			self.__manager.emit("hide-newfile-dialog-window")
			self.__manager.emit("open-files", [uri], "utf8")
			self.__manager.emit("creation-pass")
		except:
			self.__manager.emit("creation-error", _("Error: Cannot create new file."))
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __create_file_cb(self, manager, name):
		self.__create_file(name)
		return False

class Enumerator(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("get-fileinfos", self.__fileinfos_cb)

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

	def __get_fileinfos(self, folder):
		attributes = "standard::*"
		from gio import File
		enumerator = File(folder).enumerate_children(attributes)
		fileinfos = []
		while True:
			self.__editor.response()
			fileinfo = enumerator.next_file()
			if not fileinfo: break
			fileinfos.append(fileinfo)
		return fileinfos

	def __send(self, folder):
		fileinfos = self.__get_fileinfos(folder)
		self.__manager.emit("filter-fileinfos", (folder, fileinfos))
#		self.__manager.emit("folder-and-fileinfos", (folder, fileinfos))
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __fileinfos_cb(self, manager, folder):
		from gobject import idle_add
		idle_add(self.__send, folder)
		return False

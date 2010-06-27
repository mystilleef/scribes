class Enumerator(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("get-fileinfos", self.__fileinfos_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from Cancellable import GCancellable
		self.__cancellable = GCancellable(manager, editor)
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __send(self, folder):
		attributes = "standard::*"
		from gio import File
		File(folder).enumerate_children_async(attributes, self.__children_async_cb, cancellable=self.__cancellable, user_data=folder)
		return False

	def __children_async_cb(self, gfile, result, folder):
		try:
			from gio import Error
			enumerator = gfile.enumerate_children_finish(result)
			from gobject import idle_add
			idle_add(self.__get_fileinfos, (enumerator, folder))
		except Error, e:
			self.__manager.emit("enumeration-error")
		return False

	def __get_fileinfos(self, data):
		enumerator, folder = data
		enumerator.next_files_async(999999, self.__next_async_cb, cancellable=self.__cancellable, user_data=folder)
		return False

	def __next_async_cb(self, enumerator, result, folder):
		fileinfos = enumerator.next_files_finish(result)
		self.__manager.emit("filter-fileinfos", (folder, fileinfos))
		enumerator.close(self.__cancellable)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __fileinfos_cb(self, manager, folder):
		from gobject import idle_add
		idle_add(self.__send, folder)
		return False

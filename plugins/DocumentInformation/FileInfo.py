class FileInfo(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("process-fileinfo", self.__process_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __send_fileinfo(self):
		try:
			fileinfo = self.__editor.fileinfo
		except:
			fileinfo = None
		finally:
			self.__manager.emit("fileinfo", fileinfo)
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __process_cb(self, *args):
		self.__send_fileinfo()
		return

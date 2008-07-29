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
			if self.__editor.uri in ("", None): raise Exception
			from gnomevfs import get_file_info, FILE_INFO_DEFAULT
			from gnomevfs import FILE_INFO_GET_MIME_TYPE
			from gnomevfs import FILE_INFO_FORCE_SLOW_MIME_TYPE
			from gnomevfs import FILE_INFO_FOLLOW_LINKS
			FILE_INFO_ACCESS_RIGHTS = 1 << 4
			fileinfo = get_file_info(self.__editor.uri, FILE_INFO_DEFAULT |
										FILE_INFO_GET_MIME_TYPE |
										FILE_INFO_FORCE_SLOW_MIME_TYPE |
										FILE_INFO_FOLLOW_LINKS |
										FILE_INFO_ACCESS_RIGHTS)
		except:
			fileinfo = None
		finally:
			self.__manager.emit("fileinfo", fileinfo)
		return

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

class Checker(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("check-remote-uri", self.__check_cb)

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

	def __check(self, uri):
		try:
			FILE_INFO_ACCESS_RIGHTS = 1 << 4
			from gnomevfs import AccessDeniedError, NotFoundError
			from gnomevfs import get_file_info, FILE_INFO_DEFAULT
			fileinfo = get_file_info(uri, FILE_INFO_DEFAULT |
									FILE_INFO_ACCESS_RIGHTS)
			if not fileinfo: raise ValueError
			self.__manager.emit("read-uri", uri)
		except AccessDeniedError:
			# Error code 2 signifies an access error.
			self.__manager.emit("error", uri, 2)
		except NotFoundError:
			# Error code 4 signifies a file does not exist.
			self.__manager.emit("error", uri, 4)
		except ValueError:
			# Error code 3 signifies a fileinfo error.
			self.__manager.emit("error", uri, 3)
		except:
			# Error code 3 signifies a fileinfo error.
			self.__manager.emit("error", uri, 3)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __check_cb(self, manager, uri):
		from gobject import idle_add
		idle_add(self.__check, uri)
		return False

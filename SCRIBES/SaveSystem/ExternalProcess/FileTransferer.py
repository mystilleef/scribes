from gettext import gettext as _
PRIORITY = 10

class Transferer(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		manager.connect("transfer", self.__transfer_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__data = ()
		return

	def __transfer(self, data):
		try:
			# data = (session_id, uri, encoding, swapfile, fileinfo)
			self.__data = data
			uri, swapfile = data[1], data[-2]
			from gnomevfs import XFER_OVERWRITE_MODE_REPLACE
			from gnomevfs import XFER_ERROR_MODE_QUERY, URI
			from gnomevfs.async import xfer
			XFER_TARGET_DEFAULT_PERMS = 1 << 12
			xfer(source_uri_list=[URI(swapfile)],
					target_uri_list=[URI(uri)],
					xfer_options=XFER_TARGET_DEFAULT_PERMS,
					error_mode=XFER_ERROR_MODE_QUERY,
					priority = PRIORITY,
					overwrite_mode=XFER_OVERWRITE_MODE_REPLACE,
					progress_update_callback=self.__update_cb,
					update_callback_data=None,
					progress_sync_callback=self.__sync_cb)
		except:
			message = _("Error while transfering fail to save location")
			self.__error(message)
		return False

	def __sync_cb(self, info):
		if info.vfs_status: return False
		return  True

	def __update_cb(self, handle, info, data):
		try:
			if info.vfs_status: raise Exception
			from gnomevfs import XFER_PHASE_COMPLETED
			if info.phase != XFER_PHASE_COMPLETED: return True
			self.__finish()
		except:
			handle.cancel()
			message = _("Error while transfering file to save location")
			self.__error(message)
		return True

	def __finish(self):
		self.__set_file_info()
		self.__manager.emit("finished", self.__data)
		return

	def __set_file_info(self):
		try:
			uri, fileinfo = self.__data[1], self.__data[-1]
			if not fileinfo: return
			from gnomevfs import set_file_info, SET_FILE_INFO_PERMISSIONS
			from gnomevfs import URI
			set_file_info(URI(uri), fileinfo, SET_FILE_INFO_PERMISSIONS)
		except:
			pass
		return

	def __transfer_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__transfer, data)
		return False

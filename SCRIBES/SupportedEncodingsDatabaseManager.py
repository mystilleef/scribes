class Manager(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("new-encoding", self.__new_encoding_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monid1 = monitor_add(self.__database_uri, MONITOR_FILE, self.__encoding_cb)
		self.__emit_encoding_list()
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from os.path import join
		preference_folder = join(editor.metadata_folder, "Preferences")
		database_path = join(preference_folder, "Encoding.gdb")
		from gnomevfs import get_uri_from_local_path
		self.__database_uri = get_uri_from_local_path(database_path)
		return

	def __destroy(self):
		from gnomevfs import monitor_cancel
		monitor_cancel(self.__monid1)
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return

	def __emit_encoding_list(self):
		from EncodingMetadata import get_value
		self.__manager.emit("encoding-list", get_value())
		return False

	def __update_encoding(self, encoding, add):
		from EncodingMetadata import get_value, set_value
		encodings = get_value()
		encodings.append(encoding) if add else encodings.remove(encoding)
		set_value(encodings)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __new_encoding_cb(self, manager, encoding, add):
		self.__update_encoding(encoding, add)
		return False

	def __encoding_cb(self, *args):
		self.__emit_encoding_list()
		return False

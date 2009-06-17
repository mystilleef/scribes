class Manager(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("new-encoding", self.__new_encoding_cb)
		self.__monitor.connect("changed", self.__encoding_cb)
		self.__emit_encoding_list()
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from os.path import join
		preference_folder = join(editor.metadata_folder, "Preferences")
		database_path = join(preference_folder, "Encoding.gdb")
		from gio import File, FILE_MONITOR_NONE
		self.__monitor = File(database_path).monitor_file(FILE_MONITOR_NONE, None)
		return

	def __destroy(self):
		self.__monitor.cancel
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return

	def __emit_encoding_list(self):
		from EncodingSystem.EncodingListMetadata import get_value
		self.__manager.emit("encoding-list", get_value())
		return False

	def __update_encoding(self, encoding, add):
		from EncodingSystem.EncodingListMetadata import get_value, set_value
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
		monitor, gfile, otherfile, event = args
		if not (event in (0, 3)): return False
		self.__emit_encoding_list()
		return False

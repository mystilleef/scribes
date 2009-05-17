from gettext import gettext as _

class Manager(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("combobox-encoding-data?", self.__encoding_data_cb)
		self.__monitor.connect("changed", self.__encoding_cb)
		editor.register_object(self)
		self.__emit_encoding_data()
		editor.response()
		
	def __init_attributes(self, editor):
		self.__editor = editor
		self.__supported_encodings = editor.supported_encodings
		from os.path import join
		preference_folder = join(editor.metadata_folder, "Preferences")
		database_path = join(preference_folder, "Encoding.gdb")
		from gio import File, FILE_MONITOR_NONE
		self.__monitor = File(database_path).monitor_file(FILE_MONITOR_NONE, None)
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__monitor.cancel()
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __emit_encoding_data(self):
		from EncodingMetadata import get_value
		encoding_list = get_value()
		data = self.__reformat_data_for_display(encoding_list)
		data.insert(0, (_("Recommended") + " (UTF-8)", "utf-8"))
		self.__editor.emit("combobox-encoding-data", data)
		return False

	def __reformat_data_for_display(self, encodings):
		return [self.__extract_data(encoding) for encoding in encodings]

	def __extract_data(self, encoding):
		for codec, alias, language in self.__supported_encodings:
			if codec != encoding: continue
			data = self.__construct_data(codec, alias, language)
			break
		return data

	def __construct_data(self, codec, alias, language):
		return language + " (" + codec + ")", alias

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __encoding_cb(self, *args):
		monitor, gfile, otherfile, event = args
		if not (event in (0, 3)): return False
		self.__emit_encoding_data()
		return False

	def __encoding_data_cb(self, *args):
		self.__emit_encoding_data()
		return False

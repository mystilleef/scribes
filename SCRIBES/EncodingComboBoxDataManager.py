from gettext import gettext as _

class Manager(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("combobox-encoding-data?", self.__encoding_data_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monid1 = monitor_add(self.__database_uri, MONITOR_FILE, self.__encoding_cb)
		editor.register_object(self)
		self.__emit_encoding_data()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__supported_encodings = editor.supported_encodings
		from os.path import join
		preference_folder = join(editor.metadata_folder, "Preferences")
		database_path = join(preference_folder, "Encoding.gdb")
		from gnomevfs import get_uri_from_local_path
		self.__database_uri = get_uri_from_local_path(database_path)
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		from gnomevfs import monitor_cancel
		monitor_cancel(self.__monid1)
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
		self.__emit_encoding_data()
		return False

	def __encoding_data_cb(self, *args):
		self.__emit_encoding_data()
		return False

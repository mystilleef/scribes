from gettext import gettext as _

class Generator(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("combobox-encoding-data?", self.__query_cb)
		self.__sigid3 = manager.connect("encoding-list", self.__encoding_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__supported_encodings = editor.supported_encodings
		self.__manager = manager
		self.__encoding_data = []
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __generate_and_send_encoding_data(self, encodings):
		data = self.__reformat_data_for_display(encodings)
		data.insert(0, (_("Recommended") + " (UTF-8)", "utf-8"))
		self.__data = data
		self.__send_combobox_encoding_data()
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

	def __send_combobox_encoding_data(self):
		self.__editor.emit("combobox-encoding-data", self.__data)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __query_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__send_combobox_encoding_data)
		return False

	def __encoding_cb(self, manager, encodings):
		from gobject import idle_add
		idle_add(self.__generate_and_send_encoding_data, encodings)
		return False

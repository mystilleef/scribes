class Manager(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("loaded-file", self.__loaded_file_cb)
		self.__sigid3 = editor.connect("renamed-file", self.__renamed_file_cb)
		self.__sigid4 = editor.connect("quit", self.__quit_cb)
		self.__sigid5 = editor.connect("update-encoding-guess-list", self.__update_guess_list_cb)
		self.__sigid6 = editor.connect("new-encoding-list", self.__new_encoding_list_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__utf8_encodings = ["utf-8", "utf8", "UTF8", "UTF-8", "Utf-8"]
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.disconnect_signal(self.__sigid6, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

########################################################################
#
#							Helper Methods
#
########################################################################

	def __set_guess_list(self, encoding):
		if encoding in [None, "utf-8"]: return False
		from EncodingGuessListMetadata import get_value, set_value
		encoding_list = get_value()
		if encoding_list:
			if encoding in encoding_list: return False
			encoding_list.append(encoding)
			set_value(encoding_list)
		else:
			set_value([encoding])
		return False

	def __set_encoding_list(self, new_encoding_list):
		from EncodingMetadata import set_value
		set_value(new_encoding_list)
		return False

	def __format_encoding(self, encoding):
		# Remove white spaces. Convert to lower case.
		if encoding in self.__utf8_encodings: return "utf-8"
		return encoding.strip().lower()

########################################################################
#
#						Signal and Event Handlers
#
########################################################################

	def __quit_cb(self, *args):
		self.__destroy()
		return

	def __loaded_file_cb(self, editor, uri, encoding):
		if encoding is None: return
		encoding = self.__format_encoding(encoding)
		if encoding == "utf-8": return
		from thread import start_new_thread
		start_new_thread(self.__set_guess_list, (encoding,))
#		self.__set_guess_list(encoding)
		return

	def __renamed_file_cb(self, editor, uri, encoding):
		encoding = "utf-8" if encoding is None else self.__format_encoding(encoding)
		start_new_thread(self.__set_guess_list, (encoding,))
		return

	def __update_guess_list_cb(self, editor, encoding):
		self.__set_guess_list(encoding)
		return False

	def __new_encoding_list_cb(self, editor, new_encoding_list):
		self.__set_encoding_list(new_encoding_list)
		return False

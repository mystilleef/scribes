# Save file 7 seconds after modification.
SAVE_TIMER = 7000  # units in milliseconds (1000th of a second)

class Manager(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("close", self.__close_cb)
		self.__sigid2 = editor.connect("save-file", self.__save_file_cb)
		self.__sigid3 = editor.connect("saved-file", self.__saved_file_cb)
		self.__sigid4 = editor.connect("save-error", self.__save_error_cb)
		self.__sigid5 = editor.connect("modified-file", self.__modified_file_cb)
		self.__sigid6 = editor.connect("window-focus-out", self.__focus_out_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__quit = False
		self.__error = False
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.disconnect_signal(self.__sigid6, self.__editor)
		self.__editor.unregister_object(self)
		self.__editor.emit("quit")
		del self
		self = None
		return

	def __save(self, uri, encoding):
		try:
			uri = uri if uri else self.__editor.uri
			if not uri: raise ValueError
			if self.__editor.readonly: raise TypeError
			self.__editor.emit("private-save-file", uri, encoding)
		except ValueError:
			print "NO URI TO SAVE!"
		except TypeError:
			print "Error: Editor is in readonly mode"
		return False

	def __create_unsaved_file(self):
		return False

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return False

	def __save_file_cb(self, editor, uri, encoding):
		self.__remove_timer()
		from gobject import idle_add
		idle_add(self.__save, uri, encoding, priority=9999)
		return False

	def __saved_file_cb(self, *args):
		if self.__quit: self.__destroy()
		return False

	def __save_error_cb(self, editor, uri, encoding, message):
		self.__error = True
		return False

	def __modified_file_cb(self, editor, modified):
		if editor.uri is None or modified is False: return False
		self.__remove_timer()
		from gobject import timeout_add
		self.__timer = timeout_add(SAVE_TIMER, self.__save, editor.uri, editor.encoding, priority=9999)
		return False

	def __focus_out_cb(self, editor):
		if editor.uri is None or editor.modified is False or self.__quit or self.__error: return False
		from gobject import idle_add
		self.__remove_timer()
		idle_add(self.__save, editor.uri, editor.encoding, priority=9999)
		return False

	def __close_cb(self, editor, save_file):
		try:
			if save_file is False or self.__error or editor.modified is False: raise ValueError
			self.__remove_timer()
			self.__quit = True
			self.__save(editor.uri, editor.encoding) if editor.uri else self.__create_unsaved_file()
		except ValueError:
			self.__destroy()
		return False

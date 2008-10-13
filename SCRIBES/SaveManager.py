from gettext import gettext as _
# Save file 7 seconds after modification.
SAVE_TIMER = 7000  # units in milliseconds (1000th of a second)
filename = _("Unsaved Document ")

class Manager(object):
	"""
	This class decides when to save a file automatically. A file is
	saved:
		- approximately 7 seconds after modification;
		- when the window loses focus;
		- before a window is closed if it has been modified.
	"""

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("close", self.__close_cb)
		self.__sigid2 = editor.connect("save-file", self.__save_file_cb)
		self.__sigid3 = editor.connect("saved-file", self.__saved_file_cb)
		self.__sigid4 = editor.connect("save-error", self.__save_error_cb)
		self.__sigid5 = editor.connect("modified-file", self.__modified_file_cb)
		self.__sigid6 = editor.connect("window-focus-out", self.__focus_out_cb)
		self.__sigid7 = editor.connect("rename-file", self.__rename_file_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__quit = False
		self.__error = False
		self.__rename = False
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.disconnect_signal(self.__sigid6, self.__editor)
		self.__editor.disconnect_signal(self.__sigid7, self.__editor)
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
			message = _("Error: No location or file to save to.")
			self.__error_message(_("URI NOT FOUND"), message)
		except TypeError:
			message = "Error: Editor is in readonly mode"
			self.__error_message(_("READONLY ERROR"), message)
		return False

	def __create_unsaved_file(self):
		uri = self.__create_new_file()
		self.__save(uri, "utf-8")
		return False

	def __create_new_file(self):
		folder = self.__editor.desktop_folder
		# A count to append to unsaved documents if many unsaved documents
		# exists in folder.
		count = 1
		from dircache import listdir
		file_list = listdir(folder)
		# Calculate count to append to unsaved documents.
		while True:
			newfile = filename + str(count)
			if not (newfile in file_list): break
			count += 1
		newfile = folder + "/" + newfile
		from gnomevfs import make_uri_from_shell_arg
		return make_uri_from_shell_arg(newfile)

	def __error_message(self, title, message):
		self.__editor.show_error(title, message, busy=True)
		return False

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return False

########################################################################
#
#						Signal Listeners
#
########################################################################

	def __save_file_cb(self, editor, uri, encoding):
		self.__remove_timer()
		from gobject import idle_add
		idle_add(self.__save, uri, encoding, priority=9999)
		return False
	
	def __rename_file_cb(self, editor, uri, encoding):
		self.__rename = True
		self.__remove_timer()
		from gobject import idle_add
		idle_add(self.__save, uri, encoding, priority=9999)
		return False

	def __saved_file_cb(self, *args):
		self.__error = False
		if self.__quit: self.__destroy()
		if self.__rename: self.__editor.emit("renamed-file", self.__editor.uri, self.__editor.encoding)
		self.__rename = False
		return False

	def __save_error_cb(self, editor, uri, encoding, message):
		self.__error = True
		self.__error_message(uri, message)
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

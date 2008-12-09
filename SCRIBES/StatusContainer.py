class Container(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("fullscreen", self.__fullscreen_cb)
		self.__set_visibility()
		editor.response()
		editor.register_object(self)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monid1 = monitor_add(self.__uri, MONITOR_FILE, self.__changed_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__container = editor.gui.get_widget("StatusContainer")
		# Path to the font database.
		from os.path import join
		folder = join(editor.metadata_folder, "Preferences")
		file_path = join(folder, "MinimalMode.gdb")
		from gnomevfs import get_uri_from_local_path as get_uri
		self.__uri = get_uri(file_path)
		return

	def __destroy(self):
		from gnomevfs import monitor_cancel
		monitor_cancel(self.__monid1)
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __hide(self):
		self.__editor.refresh()
		self.__container.hide()
		self.__editor.refresh()
		return False
	
	def __show(self):
		self.__editor.refresh()
		self.__container.show()
		self.__editor.refresh()
		return False

	def __set_visibility(self):
		from MinimalModeMetadata import get_value as minimal_mode
		self.__hide() if minimal_mode() else self.__show()
		return

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __fullscreen_cb(self, editor, fullscreen):
		self.__hide() if fullscreen else self.__set_visibility()
		return False

	def __changed_cb(self, *args):
		self.__set_visibility()
		return False

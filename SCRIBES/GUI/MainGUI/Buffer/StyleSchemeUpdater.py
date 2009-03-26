class Updater(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monid = monitor_add(self.__uri, MONITOR_FILE, self.__changed_cb)
		self.__update()
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__uri = self.__get_database_uri()
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		from gnomevfs import monitor_cancel
		monitor_cancel(self.__monid)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __update(self):
		self.__editor.response()
		from SCRIBES.ColorThemeMetadata import get_value
		scheme_id = get_value()
		style_scheme = self.__editor.style_scheme_manager.get_scheme(scheme_id)
		if style_scheme: self.__buffer.set_style_scheme(style_scheme)
		self.__editor.refresh()
		return False

	def __get_database_uri(self):
		from os.path import join
		folder = join(self.__editor.metadata_folder, "Preferences")
		_path = join(folder, "ColorTheme.gdb")
		from gnomevfs import get_uri_from_local_path
		uri = get_uri_from_local_path(_path)
		return uri

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update)
		return False

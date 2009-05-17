class Updater(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__monitor.connect("changed", self.__changed_cb)
		self.__update()
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		from gio import File, FILE_MONITOR_NONE
		self.__monitor = File(self.__get_path()).monitor_file(FILE_MONITOR_NONE, None)
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__monitor.cancel()
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
		self.__editor.response()
		return False

	def __get_path(self):
		from os.path import join
		folder = join(self.__editor.metadata_folder, "Preferences")
		return join(folder, "ColorTheme.gdb")

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		monitor, gfile, otherfile, event = args
		if not (event in (0, 2, 3)): return False
		from gobject import idle_add
		idle_add(self.__update)
		return False

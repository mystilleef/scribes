class ColorButton(object):

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__set_properties()
		self.__sigid1 = self.__button.connect("color-set", self.__color_set_cb)
		self.__sigid2 = manager.connect("destroy", self.__destroy_cb)
		self.__monitor.connect("changed", self.__changed_cb)
		self.__button.set_property("sensitive", True)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		self.__button = manager.gui.get_widget("BracketSelectionColorButton")
		from os.path import join
		preference_folder = join(editor.metadata_folder, "PluginPreferences")
		_path = join(preference_folder, "LexicalScopeHighlight.gdb")
		from gio import File, FILE_MONITOR_NONE
		self.__monitor = File(_path).monitor_file(FILE_MONITOR_NONE, None)
		return

	def __set_properties(self):
		from LexicalScopeHighlightMetadata import get_value
		from gtk.gdk import color_parse
		color = color_parse(get_value())
		self.__button.set_color(color)
		return

	def __destroy(self):
		self.__monitor.cancel()
		self.__editor.disconnect_signal(self.__sigid1, self.__button)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__button.destroy()
		del self
		self = None
		return

	def __color_set_cb(self, *args):
		from LexicalScopeHighlightMetadata import set_value
		color = self.__button.get_color().to_string()
		set_value(color)
		return True

	def __destroy_cb(self, *args):
		self.__destroy()
		return True

	def __changed_cb(self, *args):
		monitor, gfile, otherfile, event = args
		if not (event in (0,2,3)): return False
		self.__button.handler_block(self.__sigid1)
		from LexicalScopeHighlightMetadata import get_value
		from gtk.gdk import color_parse
		color = color_parse(get_value())
		self.__button.set_color(color)
		self.__button.handler_unblock(self.__sigid1)
		return True

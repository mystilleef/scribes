class View(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		self.__add_view_to_scroll()
		self.__set_properties()
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		from gtksourceview2 import View, Buffer
		self.__view = View(Buffer())
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __set_properties(self):
		self.__editor.response()
		from gtk import DEST_DEFAULT_ALL
		targets = [("text/uri-list", 0, 80)]
		from gtk.gdk import ACTION_COPY, BUTTON1_MASK, ACTION_DEFAULT
		self.__view.drag_dest_set(DEST_DEFAULT_ALL, targets, ACTION_COPY)
		self.__view.drag_dest_add_text_targets()
		self.__view.set_property("is-focus", True)
		self.__view.set_property("has-focus", True)
		self.__view.set_property("can-focus", True)
		self.__view.set_property("can-default", True)
		self.__view.set_property("has-default", True)
		self.__view.set_property("receives-default", True)
		self.__view.set_property("auto-indent", True)
		self.__view.set_property("highlight-current-line", True)
		self.__view.set_property("show-line-numbers", True)
		self.__view.set_property("indent-width", -1)
		from SCRIBES.TabWidthMetadata import get_value as tab_width
		self.__view.set_property("tab-width", tab_width())
		from SCRIBES.MarginPositionMetadata import get_value as margin_position
		self.__view.set_property("right-margin-position", margin_position())
		from SCRIBES.DisplayRightMarginMetadata import get_value as show_margin
		self.__view.set_property("show-right-margin", show_margin())
		from SCRIBES.UseTabsMetadata import get_value as use_tabs
		self.__view.set_property("insert-spaces-instead-of-tabs",(not use_tabs()))
		from gtksourceview2 import SMART_HOME_END_BEFORE
		self.__view.set_property("smart-home-end", SMART_HOME_END_BEFORE)
		from SCRIBES.FontMetadata import get_value as font_name
		from pango import FontDescription
		font = FontDescription(font_name())
		self.__view.modify_font(font)
		from gtk import WRAP_WORD_CHAR, WRAP_NONE
		from SCRIBES.TextWrappingMetadata import get_value as wrap_mode_bool
		wrap_mode = self.__view.set_wrap_mode
		wrap_mode(WRAP_WORD_CHAR) if wrap_mode_bool() else wrap_mode(WRAP_NONE)
		self.__view.set_property("sensitive", True)
		self.__editor.response()
		return False

	def __add_view_to_scroll(self):
		self.__editor.response()
		swin = self.__editor.gui.get_widget("ScrolledWindow")
		self.__editor.response()
		swin.add(self.__view)
		self.__editor.response()
		swin.show_all()
		self.__editor.response()
		return False


	def __quit_cb(self, *args):
		self.__destroy()
		return False

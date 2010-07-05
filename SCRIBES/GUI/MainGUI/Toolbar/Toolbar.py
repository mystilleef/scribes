class Toolbar(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		self.__set_properties()
		self.__add_toolbuttons()
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		from gtk import Toolbar
		self.__toolbar = Toolbar()
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __set_properties(self):
		from Utils import never_focus
		never_focus(self.__toolbar)
		self.__toolbar.set_property("sensitive", True)
		from gtk import TEXT_WINDOW_WIDGET, ORIENTATION_HORIZONTAL, EventBox
		from gtk import TOOLBAR_ICONS, Frame, SHADOW_IN, ICON_SIZE_SMALL_TOOLBAR
		self.__toolbar.set_property("icon-size", ICON_SIZE_SMALL_TOOLBAR)
		self.__toolbar.set_style(TOOLBAR_ICONS)
		self.__toolbar.set_orientation(ORIENTATION_HORIZONTAL)
		self.__editor.set_data("Toolbar", self.__toolbar)
		frame = Frame()
		frame.add(self.__toolbar)
		frame.set_shadow_type(SHADOW_IN)
		box = EventBox()
		box.add(frame)
		self.__editor.set_data("ToolContainer", box)
		self.__editor.textview.add_child_in_window(box, TEXT_WINDOW_WIDGET, -3, -3)
		return

	def __add_toolbuttons(self):
		from ToolbuttonsInitializer import Initializer
		Initializer(self.__toolbar, self.__editor)
		return

	def __quit_cb(self, *args):
		self.__destroy()
		return False

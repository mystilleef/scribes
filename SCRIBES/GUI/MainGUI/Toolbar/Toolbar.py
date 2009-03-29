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
		self.__toolbar = editor.gui.get_widget("Toolbar")
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
		return

	def __add_toolbuttons(self):
		from ToolbuttonsInitializer import Initializer
		Initializer(self.__toolbar, self.__editor)
		return

	def __quit_cb(self, *args):
		self.__destroy()
		return False

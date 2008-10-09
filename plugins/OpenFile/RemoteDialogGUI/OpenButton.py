
class Button(object):
	"""
	This class defines the properties and behavior of the open button on
	the file chooser.
	"""

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("remote-button-sensitivity", self.__sensitivity_cb)
		self.__sigid2 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid3 = self.__button.connect("clicked", self.__clicked_cb)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		self.__button = manager.remote_gui.get_widget("OpenButton")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__button)
		self.__button.destroy()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __sensitivity_cb(self, manager, value):
		self.__button.set_property("sensitive", value)
		return

	def __clicked_cb(self, *args):
		self.__manager.emit("hide-remote-dialog-window")
		self.__button.set_property("sensitive", False)
		self.__manager.emit("load-remote-file")
		return

class Button(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__button.connect("clicked", self.__clicked_cb)
		self.__button.set_property("sensitive", True)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__button = manager.gui.get_widget("HelpButton")
		return

	def __destroy_cb(self, manager):
		self.__editor.disconnect_signal(self.__sigid1, manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__button)
		self.__button.destroy()
		del self
		self = None
		return

	def __clicked_cb(self, button):
		self.__editor.help()
		return

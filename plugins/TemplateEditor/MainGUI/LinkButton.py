class Button(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = self.__button.connect("clicked", self.__clicked_cb)
		self.__sigid2 = manager.connect("destroy", self.__destroy_cb)
		self.__button.set_property("sensitive", True)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__button = manager.gui.get_widget("LinkButton")
		return

	def __destroy_cb(self, manager):
		self.__editor.disconnect_signal(self.__sigid1, self.__button)
		self.__editor.disconnect_signal(self.__sigid2, manager)
		del self
		self = None
		return

	def __clicked_cb(self, button):
		from gnome import url_show
		uri = self.__button.get_uri()
		url_show(uri)
		return

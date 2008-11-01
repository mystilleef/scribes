class Displayer(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("show-replacebar", self.__show_cb)
		self.__sigid3 = manager.connect("hide-bar", self.__hide_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__label = manager.gui.get_widget("ReplaceLabel")
		self.__separator = manager.gui.get_widget("Separator")
		self.__button = manager.gui.get_widget("ReplaceButton")
		self.__abutton = manager.gui.get_widget("ReplaceAllButton")
		self.__entry = manager.gui.get_widget("ReplaceEntry")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return

	def __show(self):
		self.__label.show()
		self.__separator.show()
		self.__button.show()
		self.__abutton.show()
		self.__entry.show()
		return

	def __hide(self):
		self.__label.hide()
		self.__separator.hide()
		self.__button.hide()
		self.__abutton.hide()
		self.__entry.hide()
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __show_cb(self, *args):
		self.__show()
		return False

	def __hide_cb(self, *args):
		self.__hide()
		return False

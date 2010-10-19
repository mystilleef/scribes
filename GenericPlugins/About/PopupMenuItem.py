from gtk import ImageMenuItem

class PopupMenuItem(ImageMenuItem):

	def __init__(self, editor):
		from gtk import STOCK_ABOUT
		ImageMenuItem.__init__(self, STOCK_ABOUT)
		self.__init_attributes(editor)
		self.set_property("name", "AboutMenuitem")
		self.__sigid1 = self.connect("activate", self.__activate_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		return

	def __activate_cb(self, *args):
		self.__editor.trigger("show-about-dialog")
		return True

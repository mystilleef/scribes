from gtksourceview2 import View, Buffer

class SourceView(View):

	def __init__(self, manager, editor):
		View.__init__(self, Buffer())
		self.__init_attributes(manager, editor)
		self.__add_view_to_scrolled_window()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("valid-trigger", self.__valid_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return  

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __add_view_to_scrolled_window(self):
		self.set_property("sensitive", False)
		scrolled_window = self.__manager.editor_gui.get_widget("ScrolledWindow")
		scrolled_window.add(self)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __valid_cb(self, manager, valid):
		self.set_property("sensitive", valid)
		return False

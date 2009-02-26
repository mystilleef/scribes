class Changer(object):

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("new-scheme", self.__new_scheme_cb)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __change(self, scheme):
		from Metadata import set_value
		set_value(scheme.get_id())
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __new_scheme_cb(self, manager, scheme):
		from gobject import idle_add
		idle_add(self.__change, scheme)
		return False

class Remover(object):

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("remove-scheme", self.__remove_cb)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __remove(self, scheme):
		filename = scheme.get_filename()
		from os.path import exists
		if not exists(filename): return False
		from os import remove
		remove(filename)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __remove_cb(self, manager, scheme):
		self.__remove(scheme)
		return False

class Selector(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("new-imported-templates", self.__new_imported_templates_cb)
		self.__sigid3 = manager.connect_after("templates-dictionary", self.__templates_dictionary_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from collections import deque
		self.__queue = deque()
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return False

	def __select_language(self):
		if not self.__queue: return False
		language_key = self.__queue.pop()#
		language_id = language_key.split("|")[0]
		self.__manager.emit("select-language-treeview-id", language_id)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __new_imported_templates_cb(self, manager, templates_data):
		self.__queue.append(templates_data[-1][0])
		return False

	def __templates_dictionary_cb(self, *args):
		self.__select_language()
		return False

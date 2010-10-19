class Inserter(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("valid-string", self.__valid_cb)
		self.__sigid3 = manager.connect("insert-text", self.__insert_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__string = ""
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return False

	def __insert(self, text):
		self.__editor.textview.window.freeze_updates()
		self.__manager.emit("inserting-text")
		self.__editor.textbuffer.begin_user_action()
		self.__editor.textbuffer.insert_at_cursor(text[len(self.__string):].encode("utf8"))
		self.__editor.textbuffer.end_user_action()
		self.__manager.emit("inserted-text")
		self.__editor.textview.window.thaw_updates()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __valid_cb(self, manager, string):
		self.__string = string
		return False

	def __insert_cb(self, manager, text):
		from gobject import idle_add
		idle_add(self.__insert, text)
		return False

	def __precompile_methods(self):
		methods = (self.__insert,)
		self.__editor.optimize(methods)
		return False

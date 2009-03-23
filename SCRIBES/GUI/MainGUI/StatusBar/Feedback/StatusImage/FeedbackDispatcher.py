class Dispatcher(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("update-message", self.__update_cb)
		self.__sigid3 = editor.connect("set-message", self.__set_cb)
		self.__sigid4 = editor.connect("unset-message", self.__unset_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __update(self, image_id, time):
		self.__manager.emit("update", image_id, time)
		return False

	def __set(self, image_id):
		self.__manager.emit("set", image_id)
		return False

	def __unset(self, image_id):
		self.__manager.emit("unset", image_id)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __update_cb(self, editor, message, image_id, time):
		from gobject import idle_add
		idle_add(self.__update, image_id, time, priority=9999)
		return False

	def __set_cb(self, editor, message, image_id):
		from gobject import idle_add
		idle_add(self.__set, image_id, priority=9999)
		return False

	def __unset_cb(self, editor, message, image_id):
		from gobject import idle_add
		idle_add(self.__unset, image_id, priority=9999)
		return False 

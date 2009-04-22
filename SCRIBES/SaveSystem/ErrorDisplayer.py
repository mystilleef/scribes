class Displayer(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("save-failed", self.__failed_cb)
		self.__sigid3 = manager.connect("session-id", self.__session_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__session_id = ()
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __show(self, data):
		session_id, uri, encoding, message = data
		if self.__session_id != session_id: return False
		self.__editor.show_error(uri, message, busy=True)
		return False
	
	def __quit_cb(self, *args):
		self.__destroy()
		return False
	
	def __session_cb(self, manager, session_id):
		self.__session_id = session_id
		return False
		
	def __failed_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__show, data, priority=9999)
		return

class Completer(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("session-id", self.__session_cb)
		self.__sigid3 = manager.connect("save-succeeded", self.__data_cb)
		self.__sigid4 = manager.connect("save-failed", self.__data_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from collections import deque
		self.__queue = deque()
		self.__session_id = ()
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __verify_session(self, data):
		try:
			print self.__queue
			session_id = tuple(data[0])
			self.__queue.remove(session_id)
			if self.__session_id != session_id: return False
			emit = self.__manager.emit
			emit("saved?", data) if len(data) == 3 else emit("error", data)
		except ValueError:
			print "Module Name: SCRIBES/SaveSystem/SessionCompleter"
			print "Method Name: __verify_session"
			print "ERROR MESSAGE: Session id not in queue", session_id
		finally:
			print self.__queue
			print "==================================================="
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __session_cb(self, manager, session_id):
		self.__session_id = session_id
		self.__queue.append(session_id)
		return False

	def __data_cb(self, manager, data):
		self.__verify_session(data)
		return False

from SCRIBES.SignalConnectionManager import SignalManager

class Completer(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "session-id", self.__session_cb)
		self.connect(manager, "save-succeeded", self.__data_cb)
		self.connect(manager, "save-failed", self.__data_cb)
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
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __verify_session(self, data):
		try:
			session_id = tuple(data[0])
			self.__queue.remove(session_id)
			if self.__session_id != session_id: raise AssertionError # False
			emit = self.__manager.emit
			emit("saved?", data) if len(data) == 3 else emit("error", data)
		except ValueError:
			print "Module Name: SCRIBES/SaveSystem/SessionCompleter"
			print "Method Name: __verify_session"
			print "ERROR MESSAGE: Session id not in queue", session_id
		except AssertionError:
			print "Module Name: SCRIBES/SaveSystem/SessionCompleter"
			print "Method Name: __verify_session"
			print "ERROR: Session id has changed!"
			print "Old session id: %s, New session id: %s" % (self.__session_id, session_id)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __session_cb(self, manager, session_id):
		self.__session_id = session_id
		self.__queue.append(session_id)
		return False

	def __data_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__verify_session, data)
		return False

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
			session_id = tuple(data[0])
			if not session_id in self.__queue: raise ValueError
			if session_id[-1] > self.__queue[-1][-1]: raise StandardError
			if session_id != self.__queue[-1]: raise AssertionError
			self.__queue.remove(session_id)
			emit = self.__manager.emit
			emit("saved?", data) if len(data) == 3 else emit("error", data)
		except ValueError:
			print "ERROR: SAVING WILL NOT OCCUR - DATA CORRUPTION"
		except StandardError:
			print "ERROR: SAVE DATA CORRUPTION!"
		except AssertionError:
			print "STALE OR OLD SAVE DATA - WILL DO NOTHING"
			self.__queue.remove(session_id)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __session_cb(self, manager, session_id):
		self.__queue.append(session_id)
		return False

	def __data_cb(self, manager, data):
		self.__verify_session(data)
		return False

from SCRIBES.SignalConnectionManager import SignalManager

class Checker(SignalManager):

	def __init__(self, manager):
		SignalManager.__init__(self)
		self.__init_attributes(manager)
		self.connect(manager, "pylint-check", self.__check_cb)
		self.connect(manager, "stop", self.__stop_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__stale_session = ()
		return

	def __check(self, data):
		from Exceptions import StaleSessionError, FileChangedError
		try:
			filename, editor_id, session_id, modification_time = data[0], data[1], data[2], data[3]
			from Utils import validate_session, update_python_environment_with
			validate_session(filename, self.__stale_session, editor_id, session_id, modification_time)
			update_python_environment_with(filename)
			import PyLinter
			reload(PyLinter)
			messages = PyLinter.Linter().check(filename, modification_time)
			if messages is None: raise FileChangedError
			messages.sort()
			emit = self.__manager.emit
			if messages:
				error_message = messages[0][0], messages[0][1], editor_id, session_id, modification_time
				emit("finished", error_message)
			else:
				emit("finished", (0, "", editor_id, session_id, modification_time))
		except FileChangedError:
			self.__manager.emit("ignored")
		except StaleSessionError:
			self.__manager.emit("ignored")
		return False

	def __check_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__check, data)
		return False

	def __stop_cb(self, manager, data):
		self.__stale_session = data
		return False

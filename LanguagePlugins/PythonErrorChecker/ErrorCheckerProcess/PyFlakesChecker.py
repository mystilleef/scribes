from SCRIBES.SignalConnectionManager import SignalManager
from ScribesPyflakes import checker

class Checker(SignalManager):

	def __init__(self, manager):
		SignalManager.__init__(self)
		self.__init_attributes(manager)
		self.connect(manager, "flakes-check", self.__check_cb)
		self.connect(manager, "stop", self.__stop_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__stale_session = ()
		return

	def __check(self, data):
		from Exceptions import StaleSessionError, FileChangedError
		try:
			filename, editor_id, session_id, check_type, modification_time, tree = data
			from Utils import validate_session
			validate_session(filename, self.__stale_session, editor_id, session_id, modification_time)
			messages = checker.Checker(tree, filename).messages
			messages.sort(lambda a, b: cmp(a.lineno, b.lineno))
			emit = self.__manager.emit
			ignore_errors = ("ImportStarUsed", )
			if messages: messages = [(warning.lineno, warning.message % warning.message_args, warning) for warning in messages 
										if not (warning.__class__.__name__ in ignore_errors)]
			if messages:
				from Utils import reformat_error
				error_message = messages[0][0], reformat_error(messages[0][1]), editor_id, session_id, modification_time
				emit("finished", error_message)
			else:
				if check_type == 2:
					emit("finished", (0, "", editor_id, session_id, modification_time))
				else:
					emit("pylint-check", (filename, editor_id, session_id, modification_time))
		except FileChangedError:
			self.__manager.emit("ignored")
		except StaleSessionError:
			self.__manager.emit("ignored")
		except (SyntaxError, IndentationError):
			self.__manager.emit("ignored")
		except Exception:
			self.__manager.emit("ignored")
		return False

	def __check_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__check, data)
		return False

	def __stop_cb(self, manager, data):
		self.__stale_session = data
		return False

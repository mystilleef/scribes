from SCRIBES.SignalConnectionManager import SignalManager

class Checker(SignalManager):

	def __init__(self, manager):
		SignalManager.__init__(self)
		self.__init_attributes(manager)
		self.connect(manager, "syntax-check", self.__check_cb)
		self.connect(manager, "stop", self.__stop_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__stale_session = ()
		return

	def __check(self, data):
		# Since compiler.parse does not reliably report syntax errors, use the
		# built in compiler first to detect those.
		from Exceptions import StaleSessionError, FileChangedError
		try:
			try:
				file_content, file_path, editor_id, session_id, check_type, modification_time = data
				from Utils import validate_session
				validate_session(file_path, self.__stale_session, editor_id, session_id, modification_time)
				compile(file_content.encode("utf8"), file_path, "exec")
			except MemoryError:
				# Python 2.4 will raise MemoryError if the source can't be
				# decoded.
				from sys import version_info
				if version_info[:2] == (2, 4): raise SyntaxError(None)
				raise
		except (SyntaxError, IndentationError), value:
			msg = value.args[0]
			lineno = value.lineno
			# If there's an encoding problem with the file, the text is None.
			data = lineno, msg, editor_id, session_id, modification_time
			self.__manager.emit("finished", data)
		except FileChangedError:
			self.__manager.emit("ignored")
		except StaleSessionError:
			self.__manager.emit("ignored")
		else:
			if check_type == 1:
				data = 0, "", editor_id, session_id, modification_time
				signal = "finished"
			else:
				from compiler import parse
				parse_tree = parse(file_content)
				data = file_path, editor_id, session_id, check_type, modification_time, parse_tree
				signal = "flakes-check"
			self.__manager.emit(signal, data)
		return False

	def __check_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__check, data)
		return False

	def __stop_cb(self, manager, data):
		self.__stale_session = data
		return False

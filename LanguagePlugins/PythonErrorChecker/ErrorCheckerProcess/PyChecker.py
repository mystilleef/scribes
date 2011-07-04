from SCRIBES.SignalConnectionManager import SignalManager

class Checker(SignalManager):

	def __init__(self, manager):
		SignalManager.__init__(self)
		self.__init_attributes(manager)
		self.connect(manager, "pycheck", self.__check_cb)
		self.connect(manager, "stop", self.__stop_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__stale_session = ()
		self.__checker = self.__get_pylint_executable()
		self.__flags = " -E -f parseable -d E0611"
		return

	def __check(self, data):
		from Exceptions import StaleSessionError, FileChangedError
		try:
			filename, editor_id, session_id, modification_time = data[0], data[1], data[2], data[3]
			from Utils import validate_session#, update_python_environment_with
			validate_session(filename, self.__stale_session, editor_id, session_id, modification_time)
			# update_python_environment_with(filename)
			error_data = self.__get_errors(filename)
			emit = self.__manager.emit
			if error_data:
				line, error_message = error_data[0], error_data[1].strip()
				error_data = line, error_message, editor_id, session_id, modification_time
				emit("finished", error_data)
			else:
				emit("finished", (0, "", editor_id, session_id, modification_time))
		except FileChangedError:
			self.__manager.emit("ignored")
		except StaleSessionError:
			self.__manager.emit("ignored")
		return False

	def __get_pylint_executable(self):
		pylint_executables = ["/usr/bin/pylint", "/usr/local/bin/pylint"]
		from os.path import exists
		for _file in pylint_executables:
			if exists(_file): return _file
		return ""

	def __get_errors(self, filename):
		from pipes import quote
		from os import chdir
		from os.path import basename, dirname
		chdir(dirname(filename))
		command = "%s %s %s" % (self.__checker, self.__flags, quote(basename(filename)))
		errors = self.__execute(command)
		if not errors: return ()
		error_lines = errors.splitlines()
		cannot_import = [error for error in error_lines if error.endswith("UNABLE TO IMPORT")]
		if cannot_import: return ()
		error_data = error_lines[0].split(":")[1:]
		print error_data
		return error_data

	def __execute(self, command):
		from subprocess import Popen, PIPE
		process = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
		result = process.communicate()
		return result[0]

	def __check_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__check, data)
		return False

	def __stop_cb(self, manager, data):
		self.__stale_session = data
		return False

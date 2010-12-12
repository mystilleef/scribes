from SCRIBES.SignalConnectionManager import SignalManager

class Executor(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "command", self.__command_cb)
		self.connect(manager, "bounds", self.__bounds_cb)
		self.connect(manager, "execute", self.__execute_cb, True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__input = ""
		self.__command = ""
		return

	def __make_input_file(self):
		from tempfile import NamedTemporaryFile
		fd = NamedTemporaryFile(delete=False)
		fd.write(self.__input)
		fd.close()
		return fd

	def __run(self, standard_input_fd):
#		from shlex import split
#		command = split(self.__command)
		command = self.__command
		from subprocess import Popen, PIPE
		process = Popen(command, shell=True, stdin=open(standard_input_fd.name), stdout=PIPE, stderr=PIPE)
		result = process.communicate()
		retcode = process.wait()
		return retcode, result

	def __execute(self):
		standard_input_fd = self.__make_input_file()
		retcode, result = self.__run(standard_input_fd)
		from os import unlink
		unlink(standard_input_fd.name)
		self.__manager.emit("fail") if retcode else self.__manager.emit("result", result[0])
		if retcode: print result[-1]
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

	def __execute_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__execute)
		return False

	def __bounds_cb(self, manager, boundaries):
		from Utils import get_iter
		_buffer = self.__editor.textbuffer
		self.__input = _buffer.get_text(*get_iter(boundaries, _buffer))
		return False

	def __command_cb(self, manager, command):
		self.__command = command
		return False

from glib import PRIORITY_LOW
from gobject import idle_add, source_remove
from SCRIBES.SignalConnectionManager import SignalManager

class Checker(SignalManager):

	def __init__(self, manager, editor):
		editor.refresh()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "check", self.__check_cb)
		editor.refresh()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __check(self):
		# Since compiler.parse does not reliably report syntax errors, use the
		# built in compiler first to detect those.
		try:
			try:
				compile(self.__editor.text, self.__editor.filename, "exec")
			except MemoryError:
				# Python 2.4 will raise MemoryError if the source can't be
				# decoded.
				from sys import version_info
				if version_info[:2] == (2, 4): raise SyntaxError(None)
				raise
		except (SyntaxError, IndentationError), value:
			msg = value.args[0]
			(lineno, offset, text) = value.lineno, value.offset, value.text
			# If there's an encoding problem with the file, the text is None.
			self.__manager.emit("syntax-error", (lineno, offset, msg, text))
			self.__manager.emit("errors-found")
		else:
			from compiler import parse
			parse_tree = parse(self.__editor.text)
			self.__manager.emit("check-tree", parse_tree)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __check_cb(self, *args):
		try:
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = idle_add(self.__check, priority=PRIORITY_LOW)
		return False

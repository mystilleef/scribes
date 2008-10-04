from gettext import gettext as _

class Manager(object):
	"""
	This class checks python source code for syntax errors.
	"""

	def __init__(self, editor):
		self.__init_attributes(editor)

	def __init_attributes(self, editor):
		self.__editor = editor
		return

	def __move_cursor_to_error_line(self, line):
		iterator = self.__editor.textbuffer.get_iter_at_line(line - 1)
		self.__editor.textbuffer.place_cursor(iterator)
		self.__editor.move_view_to_cursor(True)
		message = _("Syntax error on line ") + str(line)
		self.__editor.update_message(message, "fail", 10)
		return

	def check(self):
		try:
			self.__editor.busy()
			from compiler import parse
			parse_tree = parse(self.__editor.text)
			message = _("No syntax errors found")
			self.__editor.update_message(message, "yes")
		except SyntaxError:
			from sys import exc_info
			exc = exc_info()[1]
			self.__move_cursor_to_error_line(exc.lineno)
		finally:
			self.__editor.busy(False)
			from gc import collect
			collect()
			from sys import exc_clear
			exc_clear()
		return

	def destroy(self):
		del self
		self = None
		return

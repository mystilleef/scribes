from gettext import gettext as _

class Manager(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		return

	def __find_matching_bracket(self):
		match = self.__editor.find_matching_bracket()
		if not match: return False
		self.__editor.textbuffer.place_cursor(match)
		self.__editor.move_view_to_cursor()
		return True

	def match(self):
		match = self.__find_matching_bracket()
		if match:
			message = _("Moved cursor to matching bracket")
			self.__editor.update_message(message, "pass")
		else:
			message = _("No matching bracket found")
			self.__editor.update_message(message, "fail")
		return

	def destroy(self):
		del self
		self = None
		return

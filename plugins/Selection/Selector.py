from gettext import gettext as _

class Selector(object):
	
	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("select-word", self.__select_word_cb)
		self.__sigid2 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid3 = manager.connect("select-line", self.__select_line_cb)
		self.__sigid4 = manager.connect("select-statement", self.__select_statement_cb)
		self.__sigid5 = manager.connect("select-paragraph", self.__select_paragraph_cb)
		
	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		del self
		self = None
		return 

	def __select_word(self):
		try:
			if self.__editor.inside_word() is False: raise ValueError
			start, end = self.__editor.get_word_boundary()
			self.__editor.response()
			self.__editor.textbuffer.select_range(start, end)
			self.__editor.response()
			line = start.get_line() + 1
			message = _("Selected word on line %d") % line
			self.__editor.update_message(message, "pass")
		except ValueError:
			self.__editor.update_message(_("No word to select"), "fail")
		return False

	def __select_statement(self):
		try:
			start = self.__editor.backward_to_line_begin()
			if start.ends_line(): raise ValueError
			cursor = self.__editor.cursor.copy()
			expression = cursor.starts_sentence() or cursor.ends_sentence() or cursor.inside_sentence()
			if not expression: raise ValueError
			start = self.__editor.cursor.copy()
			while start.starts_sentence() is False: start.backward_char()
			end = self.__editor.cursor.copy()
			while end.ends_sentence() is False: end.forward_char()
			self.__editor.response()
			self.__editor.textbuffer.select_range(start, end)
			self.__editor.response()
			line = start.get_line() + 1   
			message = _("Selected statement on line %d") % line
			self.__editor.update_message(message, "pass")
		except ValueError:
			message = _("No text to select")
			self.__editor.update_message(message, "fail")
		return False

	def __select_line(self):
		try:
			start = self.__editor.backward_to_line_begin()
			if start.ends_line(): raise ValueError
			end = self.__editor.forward_to_line_end()
			self.__editor.response()
			self.__editor.textbuffer.select_range(start, end)
			self.__editor.response()
			line = start.get_line() + 1
			message = _("Selected line %d") % line
			self.__editor.update_message(message, "pass")
		except ValueError:
			message = _("No text to select")
			self.__editor.update_message(message, "fail")
		return False

	def __select_paragraph(self):
		try:
			if self.__editor.is_empty_line(): raise ValueError
			start = self.__editor.cursor.copy()
			while True:
				if self.__editor.is_empty_line(start): break
				success = start.backward_line()
				if success is False: break
			if self.__editor.is_empty_line(start): start.forward_line()
			end = self.__editor.cursor.copy()
			while True:
				if self.__editor.is_empty_line(end): break
				success = end.forward_line()
				if success is False: break
			self.__editor.response()
			self.__editor.textbuffer.select_range(start, end)
			self.__editor.response()
			message = _("Selected paragraph")
			self.__editor.update_message(message, "pass")
		except ValueError:
			message = _("No text to select")
			self.__editor.update_message(message, "fail")
		return False

	def __select_word_cb(self, *args):
		self.__select_word()
		return False

	def __select_statement_cb(self, *args):
		self.__select_statement()
		return False

	def __select_line_cb(self, *args):
		self.__select_line()
		return False

	def __select_paragraph_cb(self, *args):
		self.__select_paragraph()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

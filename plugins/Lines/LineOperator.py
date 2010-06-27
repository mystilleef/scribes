from gettext import gettext as _

class Operator(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("delete-line", self.__delete_line_cb)
		self.__sigid3 = manager.connect("duplicate-line", self.__duplicate_line_cb)
		self.__sigid4 = manager.connect("join-line", self.__join_line_cb)
		self.__sigid5 = manager.connect("delete-cursor-to-end", self.__delete_cursor_to_end_cb)
		self.__sigid6 = manager.connect("delete-cursor-to-start", self.__delete_cursor_to_start_cb)
		self.__sigid7 = manager.connect("free-line-below", self.__line_below_cb)
		self.__sigid8 = manager.connect("free-line-above", self.__line_above_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = editor.textview
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		self.__editor.disconnect_signal(self.__sigid7, self.__manager)
		self.__editor.disconnect_signal(self.__sigid8, self.__manager)
		del self
		self = None
		return

	def __join(self, start, end):
		text = self.__editor.textbuffer.get_text(start, end)
		lines = text.splitlines()
		if len(lines) in (0,1): raise TypeError
		newlines = [line.strip("\t ") for line in lines[1:]]
		newlines.insert(0, lines[0].rstrip("\t "))
		text = " ".join(newlines)
		self.__editor.textbuffer.delete(start, end)
		self.__editor.textbuffer.insert_at_cursor(text)
		self.__editor.response()
		return False

	def __join_current_and_next_line(self):
		try:
			textbuffer = self.__editor.textbuffer
			offset = self.__editor.cursor.get_line_offset()
			start = self.__editor.backward_to_line_begin()
			end = self.__editor.forward_to_line_end(start.copy())
			end.forward_line()
			end = self.__editor.forward_to_line_end(end.copy())
			self.__join(start, end)
			self.__editor.cursor.set_line_offset(offset)
			textbuffer.place_cursor(textbuffer.get_iter_at_line_offset(self.__editor.cursor.get_line(), offset))
			self.__editor.update_message(_("Joined current and next lines"), "pass")
		except ValueError:
			self.__editor.update_message(_("Cannot join lines"), "fail")
		except TypeError:
			self.__editor.update_message(_("No lines to join"), "fail")
		finally:
			self.__editor.move_view_to_cursor()
		return

	def __join_selections(self):
		try:
			start, end = self.__editor.textbuffer.get_selection_bounds()
			start = self.__editor.backward_to_line_begin(start)
			end = self.__editor.forward_to_line_end(end)
			self.__join(start, end)
			self.__editor.update_message(_("Join selected lines"), "pass")
		except TypeError:
			self.__editor.update_message(_("No lines to join"), "fail")
		finally:
			self.__editor.move_view_to_cursor()
		return

	def __join_line(self):
		if self.__editor.selection_range in (0, 1): return self.__join_current_and_next_line()
		return self.__join_selections()

	def __duplicate_line(self):
		textbuffer = self.__editor.textbuffer
		iterator = self.__editor.cursor.copy()
		cursor_offset = iterator.get_line_offset()
		if textbuffer.props.has_selection:
			start, end = textbuffer.get_selection_bounds()
		else:
			start = self.__editor.cursor.copy()
			end = start.copy()
		start = self.__editor.backward_to_line_begin(start)
		end = self.__editor.forward_to_line_end(end)
		end_offset = end.get_offset()
		text = "\n" + textbuffer.get_text(start, end)
		textbuffer.begin_user_action()
		textbuffer.insert(end, text)
		textbuffer.end_user_action()
		iterator = textbuffer.get_iter_at_offset(end_offset)
		iterator.forward_line()
		iterator.set_line_offset(cursor_offset)
		textbuffer.place_cursor(iterator)
		self.__editor.update_message(_("Duplicated line"), "pass")
		self.__editor.move_view_to_cursor()
		return

	def __line_below(self):
		indentation = self.__editor.get_indentation()
		start = self.__editor.backward_to_line_begin()
		end = self.__editor.forward_to_line_end()
		textbuffer = self.__editor.textbuffer
		textbuffer.begin_user_action()
		self.__editor.response()
		if start.ends_line():
			textbuffer.insert(start, "\n")
		else:
			textbuffer.place_cursor(end)
			textbuffer.insert(end, "\n")
		if indentation: textbuffer.insert(self.__editor.cursor, indentation)
		textbuffer.end_user_action()
		message = _("Freed line %d") % (self.__editor.cursor.get_line() + 1)
		self.__editor.update_message(message, "pass")
		self.__editor.move_view_to_cursor()
		return False

	def __line_above(self):
		indentation = self.__editor.get_indentation()
		start = self.__editor.backward_to_line_begin()
		textbuffer = self.__editor.textbuffer
		textbuffer.begin_user_action()
		self.__editor.response()
		textbuffer.insert(start, "\n")
		start = self.__editor.backward_to_line_begin()
		start.backward_line()
		textbuffer.place_cursor(start)
		if indentation: textbuffer.insert(start, indentation)
		textbuffer.end_user_action()
		message = _("Freed line %d") % (self.__editor.cursor.get_line() + 1)
		self.__editor.update_message(message, "pass")
		self.__editor.move_view_to_cursor()
		return False

	def __del(self, start, end):
		textbuffer = self.__editor.textbuffer
		textbuffer.begin_user_action()
		textbuffer.delete(start, end)
		textbuffer.end_user_action()
		return False

	def __delete_to_end(self):
		start = self.__editor.cursor.copy()
		end = self.__editor.forward_to_line_end(start.copy())
		self.__del(start, end)
		self.__editor.update_message(_("Deleted text to end of line"), "pass")
		self.__editor.move_view_to_cursor()
		return False

	def __delete_to_start(self):
		end = self.__editor.cursor.copy()
		start = self.__editor.backward_to_line_begin(end.copy())
		self.__del(start, end)
		self.__editor.update_message(_("Deleted text to start of line"), "pass")
		self.__editor.move_view_to_cursor()
		return False

	def __delete_single_line(self):
		start = self.__editor.backward_to_line_begin(self.__editor.cursor.copy())
		end = self.__editor.forward_to_line_end(self.__editor.cursor.copy())
		end.forward_char()
		self.__editor.textbuffer.delete(start, end)
		return

	def __delete_line(self):
		try:
			self.__editor.textbuffer.begin_user_action()
			self.__delete_single_line()
			self.__editor.textbuffer.end_user_action()
			message = _("Deleted line %d") % (self.__editor.cursor.get_line() + 1)
			self.__editor.update_message(message, "pass")
		finally:
			self.__editor.move_view_to_cursor()
		return

	def __delete_lines(self):
		start, end = self.__editor.textbuffer.get_selection_bounds()
		start = self.__editor.backward_to_line_begin(start)
		end = self.__editor.forward_to_line_end(end)
		end.forward_char()
		self.__editor.textbuffer.begin_user_action()
		self.__editor.textbuffer.delete(start, end)
		self.__editor.textbuffer.end_user_action()
		message = _("Deleted selected lines")
		self.__editor.update_message(message, "pass")
		self.__editor.move_view_to_cursor()
		return

	def __delete_selection(self):
		start, end = self.__editor.textbuffer.get_selection_bounds()
		self.__editor.textbuffer.begin_user_action()
		self.__editor.textbuffer.delete(start, end)
		self.__editor.textbuffer.end_user_action()
		message = _("Deleted selection on line %d") % (start.get_line() + 1)
		self.__editor.update_message(message, "pass")
		self.__editor.move_view_to_cursor()
		return

	def __delete_last_line(self):
		try:
			self.__editor.textbuffer.begin_user_action()
			self.__delete_single_line()
			iterator = self.__editor.cursor.copy()
			iterator.backward_line()
			end = self.__editor.forward_to_line_end(iterator.copy())
			end.forward_char()
			start = self.__editor.forward_to_line_end(iterator.copy())
			self.__editor.textbuffer.delete(start, end)
			self.__editor.textbuffer.end_user_action()
			self.__editor.update_message(_("Deleted last line"), "pass")
		finally:
			self.__editor.move_view_to_cursor()
		return

	def __delete(self):
		if self.__is_last_line() and not self.__editor.selection_range: return self.__delete_last_line()
		if not self.__editor.selection_range: return self.__delete_line()
		if self.__editor.selection_range == 1: return self.__delete_selection()
		return self.__delete_lines()

	def __is_last_line(self):
		if self.__editor.cursor.get_line() == self.__editor.textbuffer.get_line_count() -1: return True
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __delete_line_cb(self, *args):
		self.__view.window.freeze_updates()
		self.__delete()
		self.__view.window.thaw_updates()
		return False

	def __delete_cursor_to_start_cb(self, *args):
		self.__view.window.freeze_updates()
		self.__delete_to_start()
		self.__view.window.thaw_updates()
		return False

	def __delete_cursor_to_end_cb(self, *args):
		self.__view.window.freeze_updates()
		self.__delete_to_end()
		self.__view.window.thaw_updates()
		return False

	def __duplicate_line_cb(self, *args):
		self.__view.window.freeze_updates()
		self.__duplicate_line()
		self.__view.window.thaw_updates()
		return False

	def __line_below_cb(self, *args):
		self.__view.window.freeze_updates()
		self.__line_below()
		self.__view.window.thaw_updates()
		return False

	def __line_above_cb(self, *args):
		self.__view.window.freeze_updates()
		self.__line_above()
		self.__view.window.thaw_updates()
		return False

	def __join_line_cb(self, *args):
		self.__view.window.freeze_updates()
		self.__join_line()
		self.__view.window.thaw_updates()
		return False

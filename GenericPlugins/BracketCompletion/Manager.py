from gettext import gettext as _
from gtk import keysyms

KEYSYMS = {
	keysyms.quotedbl             : keysyms.quotedbl,
	keysyms.braceleft            : keysyms.braceright,
	keysyms.bracketleft          : keysyms.bracketright,
	keysyms.parenleft            : keysyms.parenright,
	keysyms.leftdoublequotemark  : keysyms.rightdoublequotemark,
	keysyms.guillemotleft        : keysyms.guillemotright,
	keysyms.guillemotright       : keysyms.guillemotleft,
	keysyms.leftsinglequotemark  : keysyms.rightsinglequotemark,
	keysyms.leftmiddlecurlybrace : keysyms.rightmiddlecurlybrace,
	keysyms.lowleftcorner        : keysyms.lowrightcorner,
	keysyms.topleftparens        : keysyms.toprightparens,
	keysyms.topleftsqbracket     : keysyms.toprightsqbracket,
	keysyms.upleftcorner         : keysyms.uprightcorner,
	keysyms.botleftparens        : keysyms.botrightparens,
	keysyms.botleftsqbracket     : keysyms.botrightsqbracket,
	keysyms.less                 : keysyms.greater,
	keysyms.dollar               : keysyms.dollar,
	keysyms.apostrophe           : keysyms.apostrophe,
}

class BracketManager(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__check_mimetype()
		self.__sigid1 = editor.textview.connect("key-press-event", self.__key_press_event_cb)
		self.__sigid2 = editor.connect("cursor-moved", self.__cursor_moved_cb)
		self.__sigid3 = editor.connect("loaded-file", self.__loaded_document_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__match = editor.find_matching_bracket
		self.__monitor_list = []
		self.__escape_character = "\\"
		self.__open_pair_characters = [keysyms.quotedbl,
			keysyms.braceleft, keysyms.bracketleft,
			keysyms.parenleft, keysyms.leftdoublequotemark,
			keysyms.guillemotleft, keysyms.guillemotright,
			keysyms.leftsinglequotemark, keysyms.leftmiddlecurlybrace,
			keysyms.lowleftcorner, keysyms.topleftparens,
			keysyms.topleftsqbracket, keysyms.upleftcorner,
			keysyms.botleftparens, keysyms.botleftsqbracket,
			keysyms.apostrophe]
		self.__open_pair_characters_for_enclosement = self.__open_pair_characters + [keysyms.less, keysyms.apostrophe, keysyms.dollar]
		return

	def __precompile_methods(self):
		methods = (self.__key_press_event_cb, self.__cursor_moved_cb,
			self.__insert_closing_pair_character)
		self.__editor.optimize(methods)
		return False

########################################################################
#
#							Public Methods
#
########################################################################

	def destroy(self):
		self.__destroy()
		return

########################################################################
#
#							Helper Methods
#
########################################################################

	def __insert_closing_pair_character(self, keyval):
		self.__editor.begin_user_action()
		if keyval == keysyms.apostrophe:
			if self.__can_insert_apostrophe():
				self.__insert_pair_characters(keyval, keysyms.apostrophe)
			else:
				self.__insert_apostrophe()
		else:
			self.__insert_pair_characters(keyval, KEYSYMS[keyval])
		self.__editor.end_user_action()
		return

	def __enclose_selection(self, keyval):
		self.__editor.begin_user_action()
		self.__insert_enclosed_selection(keyval, KEYSYMS[keyval])
		self.__editor.end_user_action()
		return

	def __insert_pair_characters(self, open_keyval, close_keyval):
		textbuffer = self.__editor.textbuffer
		from gtk.gdk import keyval_to_unicode
		utf8_open_character = unichr(keyval_to_unicode(open_keyval)).encode("utf-8")
		utf8_closing_character = unichr(keyval_to_unicode(close_keyval)).encode("utf-8")
		cursor_position = self.__editor.cursor
		begin_mark = textbuffer.create_mark(None, cursor_position, True)
		textbuffer.begin_user_action()
		textbuffer.insert_at_cursor(utf8_open_character+utf8_closing_character)
		textbuffer.end_user_action()
		cursor_position = self.__editor.cursor
		end_mark = textbuffer.create_mark(None, cursor_position, False)
		cursor_position.backward_char()
		textbuffer.place_cursor(cursor_position)
		self.__monitor_list.append((close_keyval, (begin_mark, end_mark)))
		message = _("Pair character completion occurred")
		self.__editor.update_message(message, "pass")
		return


	def __insert_enclosed_selection(self, open_keyval, close_keyval):
		textbuffer = self.__editor.textbuffer
		from gtk.gdk import keyval_to_unicode
		utf8_open_character = unichr(keyval_to_unicode(open_keyval)).encode("utf-8")
		utf8_closing_character = unichr(keyval_to_unicode(close_keyval)).encode("utf-8")
		selection = textbuffer.get_selection_bounds()
		string = textbuffer.get_text(selection[0], selection[1])
		text = utf8_open_character + string + utf8_closing_character
		textbuffer.delete(selection[0], selection[1])
		textbuffer.insert_at_cursor(text)
		message = _("Enclosed selected text")
		self.__editor.update_message(message, "pass")
		return

	def __move_cursor_out_of_bracket_region(self):
		textbuffer = self.__editor.textbuffer
		end_mark = self.__monitor_list[-1][1][1]
		iterator = textbuffer.get_iter_at_mark(end_mark)
		textbuffer.place_cursor(iterator)
		self.__editor.move_view_to_cursor()
		return

	def __stop_monitoring(self):
		begin_mark = self.__monitor_list[-1][1][0]
		end_mark = self.__monitor_list[-1][1][1]
		self.__editor.delete_mark(begin_mark)
		self.__editor.delete_mark(end_mark)
		del self.__monitor_list[-1]
		return

	def __remove_closing_pair_character(self):
		textbuffer = self.__editor.textbuffer
		begin_mark = self.__monitor_list[-1][1][0]
		end_mark = self.__monitor_list[-1][1][1]
		begin = textbuffer.get_iter_at_mark(begin_mark)
		end = textbuffer.get_iter_at_mark(end_mark)
		if (len(textbuffer.get_text(begin, end)) != 2): return False
		begin.forward_char()
		from gtk.gdk import keyval_to_unicode
		close_keyval = self.__monitor_list[-1][0]
		character = unichr(keyval_to_unicode(close_keyval)).encode("utf-8")
		if (begin.get_char() != character): return False
		self.__editor.begin_user_action()
		begin.backward_char()
		textbuffer.begin_user_action()
		textbuffer.delete(begin, end)
		textbuffer.end_user_action()
		message = _("Removed pair character")
		self.__editor.update_message(message, "pass")
		self.__editor.end_user_action()
		return True

	def __has_escape_character(self):
		end_iterator = self.__editor.cursor
		start_iterator = end_iterator.copy()
		start_iterator.backward_char()
		if (start_iterator.get_char() == self.__escape_character): return True
		return False

	def __remove_escape_character(self):
		end_iterator = self.__editor.cursor
		start_iterator = end_iterator.copy()
		start_iterator.backward_char()
		self.__editor.textbuffer.delete(start_iterator, end_iterator)
		return

	def __can_insert_apostrophe(self):
		iterator = self.__editor.cursor
		if (iterator.starts_line()): return True
		iterator.backward_char()
		character = iterator.get_char()
		if (character.isalpha()): return False
		return True

	def __insert_apostrophe(self):
		from gtk.gdk import keyval_to_unicode
		utf8_apostrophe_character = unichr(keyval_to_unicode(keysyms.apostrophe)).encode("utf-8")
		self.__editor.textbuffer.insert_at_cursor(utf8_apostrophe_character)
		return

	def __check_mimetype(self):
		markup_mimetype = ["text/html", "application/xml", "text/xml", "application/docbook+xml"]
		if not (self.__editor.uri): return
		try:
			mimetype = self.__editor.mimetype
		except RuntimeError:
			return
		if (mimetype == "text/x-tex"):
			self.__open_pair_characters.append(keysyms.dollar)
		elif mimetype in markup_mimetype:
			self.__open_pair_characters.append(keysyms.less)
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor.textview)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self = None
		del self
		return

########################################################################
#
#						Signal and Event Handlers
#
########################################################################

	def __key_press_event_cb(self, textview, event):
		if self.__editor.has_selection and (event.keyval in self.__open_pair_characters_for_enclosement):
			self.__editor.hide_completion_window()
			self.__enclose_selection(event.keyval)
			return True
		if (self.__monitor_list):
			if (event.keyval == keysyms.BackSpace):
				self.__editor.hide_completion_window()
				result = self.__remove_closing_pair_character()
				return result
			if (keysyms.Escape == event.keyval):
				self.__editor.hide_completion_window()
				self.__move_cursor_out_of_bracket_region()
				return True
			if (self.__monitor_list[-1][0] == event.keyval):
				self.__editor.hide_completion_window()
				if event.keyval in (keysyms.quotedbl, keysyms.apostrophe):
					if (self.__has_escape_character()):
						self.__remove_escape_character()
						self.__insert_closing_pair_character(event.keyval)
						return True
				self.__move_cursor_out_of_bracket_region()
				return True
		if event.keyval in self.__open_pair_characters:
			self.__editor.hide_completion_window()
			self.__insert_closing_pair_character(event.keyval)
			return True
		return False

	def __cursor_moved_cb(self, editor):
		from gobject import idle_add
		idle_add(self.__monitor_pair_characters, priority=9999)
		return

	def __monitor_pair_characters(self):
		if not (self.__monitor_list): return False
		textbuffer = self.__editor.textbuffer
		begin_mark = self.__monitor_list[-1][1][0]
		end_mark = self.__monitor_list[-1][1][1]
		begin = textbuffer.get_iter_at_mark(begin_mark)
		end = textbuffer.get_iter_at_mark(end_mark)
		cursor_position = self.__editor.cursor
		if (cursor_position.equal(begin)) or (cursor_position.equal(end)):
			self.__stop_monitoring()
		elif not (cursor_position.in_range(begin, end)):
			self.__stop_monitoring()
		return False

	def __loaded_document_cb(self, *args):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__check_mimetype, priority=PRIORITY_LOW)
		return

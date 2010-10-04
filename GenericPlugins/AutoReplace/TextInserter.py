from gettext import gettext as _
message = _("Expanded abbreviation")

class Inserter(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("dictionary", self.__dictionary_cb)
		self.__sigid3 = manager.connect("match-found", self.__found_cb)
		self.__sigid4 = manager.connect("no-match-found", self.__nofound_cb)
		self.__sigid5 = editor.textview.connect("key-press-event", self.__event_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__dictionary = {}
		self.__word = None
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor.textview)
		del self
		self = None
		return

	def __insert(self, delimeter):
		if delimeter == "\n": indentation = self.__indent()
		end = self.__editor.cursor.copy()
		start = self.__editor.cursor.copy()
		for item in xrange(len(self.__word)): 
			self.__editor.response()
			start.backward_char()
		from copy import copy
		word = copy(self.__word)
		self.__editor.textbuffer.delete(start, end)
		text = self.__dictionary[word] + delimeter
		self.__editor.textbuffer.insert_at_cursor(text)
		if delimeter == "\n": self.__editor.textbuffer.insert_at_cursor(indentation)
		self.__editor.move_view_to_cursor()
		self.__editor.update_message(message, "pass")
		return False

	def __indent(self):
		start = self.__editor.backward_to_line_begin()
		text = self.__editor.textbuffer.get_text(start.copy(), self.__editor.cursor.copy())
		if not text: return ""
		if not (text[0] in (" ", "\t")): return ""
		indentation = ""
		for character in text:
			self.__editor.response()
			if not (character in (" ", "\t")): break
			indentation += character
		return indentation

	def __precompile_methods(self):
		methods = (self.__event_cb, self.__insert, self.__indent)
		self.__editor.optimize(methods)
		return False

	def __found_cb(self, manager, word):
		self.__word = word
		return False

	def __nofound_cb(self, *args):
		self.__word = None
		return False

	def __event_cb(self, textview, event):
		if self.__word is None: return False
		from gtk import keysyms
		if not (event.keyval in (keysyms.Return, keysyms.space)): return False
		delimeter = " " if event.keyval == keysyms.space else "\n"
		self.__insert(delimeter)
		return True

	def __dictionary_cb(self, manager, dictionary):
		self.__dictionary = dictionary
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

class Inserter(object):

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("loaded-language-templates", self.__loaded_language_templates_cb)
		self.__sigid3 = manager.connect("loaded-general-templates", self.__loaded_general_templates_cb)
		self.__sigid4 = manager.connect("expand-trigger", self.__expand_trigger_cb)
		self.__sigid5 = manager.connect("trigger-found", self.__trigger_found)
		self.__sigid6 = manager.connect("no-trigger-found", self.__no_trigger_found_cb)
		self.__sigid7 = manager.connect("reformat-template", self.__reformat_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		self.__general_dictionary = {}
		self.__language_dictionary = {}
		self.__trigger = None
		self.__reformat = True
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		self.__editor.disconnect_signal(self.__sigid7, self.__manager)
		del self
		self = None
		return

	def __precompile_methods(self):
		methods = (self.__trigger_found, self.__no_trigger_found_cb,
			self.__expand_trigger_cb)
		self.__editor.optimize(methods)
		return False

	def __insert_template(self, template):
		from utils import insert_string
		template = self.__format(template) if self.__reformat else template
		insert_string(self.__editor.textbuffer, template)
		return

	def __format(self, template):
		view = self.__editor.textview
		tab_width = view.get_property("tab-width")
		# Convert tabs to spaces
		template = template.expandtabs(tab_width)
		use_spaces = view.get_property("insert-spaces-instead-of-tabs")
		if use_spaces: return template
		# Convert spaces to tabs
		return self.__convert_indentation_to_tabs(template, tab_width)

	def __convert_indentation_to_tabs(self, template, tab_width):
		tab_indented_lines = [self.__spaces_to_tabs(line, tab_width) for line in template.splitlines(True)]
		return "".join(tab_indented_lines)

	def __spaces_to_tabs(self, line, tab_width):
		self.__editor.response()
		if line[0] != " ": return line
		indentation_width = self.__get_indentation_width(line)
		if indentation_width < tab_width: return line
		indentation = ("\t" * (indentation_width/tab_width)) + (" " * (indentation_width%tab_width))
		return indentation + line[indentation_width:]

	def __get_indentation_width(self, line):
		self.__editor.response()
		from itertools import takewhile
		is_space = lambda character: character == " "
		return len([space for space in takewhile(is_space, line)])

	def __remove_trigger(self):
		iterator = self.__editor.cursor
		from utils import remove_trailing_spaces_on_line
		remove_trailing_spaces_on_line(self.__editor.textview, iterator.get_line())
		iterator = self.__editor.cursor
		temp_iter = iterator.copy()
		for character in xrange(len(self.__trigger)): temp_iter.backward_char()
		self.__editor.textbuffer.delete(iterator, temp_iter)
		return

	def __place_template_in_buffer(self):
		from gtk import clipboard_get, gdk
		self.__clipboards = {'SELECTION': clipboard_get(gdk.SELECTION_PRIMARY)}
		self.__clipboards['SELECTION'].request_text(self.__selection_text_received)
		return

	def __selection_text_received(self, clipboard, text, data):
		from gtk import clipboard_get
		self.__clipboards['SELECTION'].text_clip = text
		self.__clipboards['CLIPBOARD'] = clipboard_get()
		self.__clipboards['CLIPBOARD'].request_text(self.__clipboard_text_received)
		return

	def __clipboard_text_received(self, clipboard, text, data):
		self.__clipboards['CLIPBOARD'].text_clip = text
		self.__place_template_in_buffer_callback()
		return

	def __place_template_in_buffer_callback(self):
		self.__editor.response()
		template = self.__get_template()
		self.__remove_trigger()
		start = self.__editor.create_left_mark()
		end = self.__editor.create_right_mark()
		self.__insert_template(template)
		self.__editor.textview.scroll_mark_onscreen(end)
		self.__expand_special_placeholders(template, start, end)
		self.__mark_placeholders(template, start, end)
		self.__editor.response()
		return False

	def __expand_special_placeholders(self, template, mstart, end):
		from utils import get_special_placeholders
		placeholders = get_special_placeholders(template)
		if not placeholders: return
		from gtk import TEXT_SEARCH_VISIBLE_ONLY
		from utils import replace_special_placeholder
		buffer_ = self.__editor.textbuffer
		mark = self.__editor.create_right_mark()
		start = buffer_.get_iter_at_mark(mstart)
		for placeholder in placeholders:
			epos = buffer_.get_iter_at_mark(end)
			begin, end_ = start.forward_search(placeholder, TEXT_SEARCH_VISIBLE_ONLY, epos)
			buffer_.place_cursor(begin)
			buffer_.delete(begin, end_)
			nplaceholder = replace_special_placeholder(placeholder, self.__editor.uri, self.__clipboards)
			cursor_position = self.__editor.cursor
			buffer_.move_mark(mark, cursor_position)
			buffer_.insert_at_cursor(nplaceholder)
			start = buffer_.get_iter_at_mark(mark)
		self.__editor.delete_mark(mark)
		return

	def __mark_placeholders(self, template, mstart, mend):
		from utils import get_placeholders
		placeholders = get_placeholders(template)
		if not placeholders: return
		from gtk import TEXT_SEARCH_VISIBLE_ONLY
		from utils import replace_special_placeholder
		buffer_ = self.__editor.textbuffer
		mark = self.__editor.create_right_mark()
		start = buffer_.get_iter_at_mark(mstart)
		from collections import deque
		placeholder_marks = deque([])
		for placeholder in placeholders:
			epos = buffer_.get_iter_at_mark(mend)
			begin, end_ = start.forward_search(placeholder, TEXT_SEARCH_VISIBLE_ONLY, epos)
			buffer_.place_cursor(begin)
			nplaceholder = placeholder.strip("${}")
			if nplaceholder == "cursor":
				nplaceholder = ""
				buffer_.delete(begin, end_)
				emark = self.__editor.create_right_mark()
				emark.set_visible(True)
				pmark = (emark,)
			else:
				if not nplaceholder: nplaceholder = " "
				bmark = self.__editor.create_left_mark(begin)
				emark = self.__editor.create_right_mark(end_)
#				bmark.set_visible(True)
#				emark.set_visible(True)
				pmark = bmark, emark
				buffer_.place_cursor(begin)
				buffer_.delete(begin, end_)
			placeholder_marks.append(pmark)
			cursor_position = self.__editor.cursor
			buffer_.move_mark(mark, cursor_position)
			buffer_.insert_at_cursor(nplaceholder)
			self.__manager.emit("tag-placeholder", pmark)
			start = buffer_.get_iter_at_mark(mark)
		self.__editor.delete_mark(mark)
		self.__manager.emit("activate-template-mode")
		self.__manager.emit("template-boundaries", (mstart, mend))
		self.__manager.emit("placeholders", placeholder_marks)
		placeholder_marks.clear()
		del placeholder_marks
		return

	def __get_template(self):
		if self.__trigger is None: return None
		general = "General" + self.__trigger
		language = None
		if self.__editor.language: language = self.__editor.language + self.__trigger
		if language and self.__language_dictionary.has_key(language):
			return self.__language_dictionary[language]
		if self.__general_dictionary.has_key(general):
			return self.__general_dictionary[general]
		return None

	def __loaded_general_templates_cb(self, manager, dictionary):
		self.__general_dictionary.clear()
		self.__general_dictionary.update(dictionary)
		return

	def __loaded_language_templates_cb(self, manager, dictionary):
		self.__language_dictionary.clear()
		self.__language_dictionary.update(dictionary)
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __expand_trigger_cb(self, *args):
		self.__place_template_in_buffer()
		return

	def __trigger_found(self, manager, trigger):
		self.__trigger = trigger
		return False

	def __no_trigger_found_cb(self, *args):
		self.__trigger = None
		return False

	def __reformat_cb(self, manager, reformat):
		self.__reformat = reformat
		return False

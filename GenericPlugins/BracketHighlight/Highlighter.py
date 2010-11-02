from SCRIBES.SignalConnectionManager import SignalManager

class Highlighter(SignalManager):
	"""
	The class implements and object that highlights regions within pair
	characters. The following characters are supported "(", ")", "[", "]"
	"<", ">", "{" and "}"
	"""

	def __init__(self, editor):
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		self.connect(editor, "cursor-moved", self.__cursor_moved_cb)
		self.connect(editor.textbuffer, "apply-tag", self.__apply_tag_cb)
		self.connect(editor.textbuffer, "remove-tag", self.__remove_tag_cb)
		self.connect(editor, "loaded-file", self.__generic_highlight_on_cb)
		self.connect(editor, "readonly", self.__generic_highlight_on_cb)
		self.connect(editor, "load-error", self.__generic_highlight_on_cb)
		self.__monitor.connect("changed", self.__highlight_cb)
		self.__highlight_region()
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__can_highlight = True
		self.__buffer_is_tagged = False
		self.__highlight_tag = self.__create_highlight_tag()
		self.__match = editor.find_matching_bracket
		self.__start_mark = None
		self.__end_mark = None
		self.__start_characters = ("(", "[", "<", "{")
		self.__end_characters = (")", "]", ">", "}")
		from os.path import join
		preference_folder = join(editor.metadata_folder, "PluginPreferences")
		database_path = join(preference_folder, "LexicalScopeHighlight.gdb")
		self.__monitor = editor.get_file_monitor(database_path)
		return

	def __precompile_methods(self):
		methods = (self.__cursor_moved_cb, self.__apply_tag_cb,
			self.__remove_tag_cb, self.__highlight_region,
			self.__highlight_cb,)
		self.__editor.optimize(methods)
		return False

	def destroy(self):
		self.__destroy()
		return

	def __highlight_region(self):
		textbuffer = self.__editor.textbuffer
		if (self.__buffer_is_tagged):
			begin = textbuffer.get_iter_at_mark(self.__start_mark)
			end = textbuffer.get_iter_at_mark(self.__end_mark)
			textbuffer.remove_tag(self.__highlight_tag, begin, end)
		iterator = self.__editor.cursor
		match = self.__match(iterator.copy())
		if not match: return False
		try:
			start, end = self.__get_boundary(iterator, match)
			textbuffer.apply_tag(self.__highlight_tag, start, end)
		except:
			pass
		return False

	def __get_boundary(self, iterator, end):
		# The madness going on over here is as a result of the strangeness
		# of the GtkSourceView API. If your head hurts, kindly move along.
		if self.__is_start_character(iterator.copy()):
			end.forward_char()
		elif self.__is_end_character(iterator.copy()):
			pass
		else:
			return None
		return iterator, end

	def __is_start_character(self, iterator):
		if iterator.get_char() in self.__start_characters: return True
		return False

	def __is_end_character(self, iterator):
		success = iterator.backward_char()
		if not success: return False
		if iterator.get_char() in self.__end_characters: return True
		return False

	def __create_highlight_tag(self):
		from gtk import TextTag
		tag = TextTag("lexical_scope_tag")
		self.__editor.textbuffer.get_tag_table().add(tag)
		from LexicalScopeHighlightMetadata import get_value
		tag.set_property("background", get_value())
		tag.set_property("foreground", "white")
		return tag

	def __destroy(self):
		self.__monitor.cancel()
		self.disconnect()
		self.__remove_highlight_tag()
		if self.__start_mark: self.__editor.delete_mark(self.__start_mark)
		if self.__end_mark: self.__editor.delete_mark(self.__end_mark)
		del self
		return

	def __remove_highlight_tag(self):
		try:
			self.__editor.textbuffer.get_tag_table().remove(self.__highlight_tag)
		except ValueError:
			pass
		return False

	def __highlight_region_timeout(self):
		from gobject import timeout_add
		self.__timer = timeout_add(250, self.__highlight_on_idle, priority=9999)
		return False

	def __highlight_on_idle(self):
		from gobject import idle_add
		self.__timer = idle_add(self.__highlight_region, priority=9999)
		return False

########################################################################
#
#						Signal and Event Handlers
#
########################################################################

	def __cursor_moved_cb(self, editor):
		if not (self.__can_highlight): return
		try:
			from gobject import source_remove, idle_add
			source_remove(self.__timer)
		except:
			pass
		finally:
			self.__timer = idle_add(self.__highlight_region_timeout, priority=9999)
		return

	def __apply_tag_cb(self, textbuffer, tag, start, end):
		if (tag != self.__highlight_tag): return False
		textbuffer = self.__editor.textbuffer
		if self.__start_mark is None: self.__start_mark = textbuffer.create_mark(None, start, True)
		if self.__end_mark is None: self.__end_mark = textbuffer.create_mark(None, end, False)
		textbuffer.move_mark(self.__start_mark, start)
		textbuffer.move_mark(self.__end_mark, end)
		self.__buffer_is_tagged = True
		return True

	def __remove_tag_cb(self, textbuffer, tag, start, end):
		if (tag != self.__highlight_tag): return False
		self.__buffer_is_tagged = False
		return True

	def __generic_highlight_off_cb(self, *args):
		self.__can_highlight = False
		begin, end = self.__editor.textbuffer.get_bounds()
		self.__editor.textbuffer.remove_tag(self.__highlight_tag, begin, end)
		return

	def __generic_highlight_on_cb(self, *args):
		self.__can_highlight = True
		from gobject import idle_add, source_remove
		try:
			source_remove(self.__generic_id)
		except:
			pass
		self.__generic_id = idle_add(self.__highlight_region, priority=9999)
		return

########################################################################
#
#						GConf Signal Handlers
#
########################################################################

	def __highlight_cb(self, *args):
		if not self.__editor.monitor_events(args, (0,2,3)): return False
		textbuffer = self.__editor.textbuffer
		begin, end = textbuffer.get_bounds()
		textbuffer.remove_tag(self.__highlight_tag, begin, end)
		from LexicalScopeHighlightMetadata import get_value
		color = get_value()
		self.__highlight_tag.set_property("background", color)
		from gobject import idle_add, source_remove
		try:
			source_remove(self.__highlight_id)
		except AttributeError:
			pass
		self.__highlight_id = idle_add(self.__highlight_region, priority=9999)
		return
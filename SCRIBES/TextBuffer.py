class Buffer(object):
	"""
	This class defines the behavior of the editor's buffer.
	"""

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__set_properties()
		self.__sigid1 = self.__buffer.connect("notify::cursor-position", self.__cursor_position_cb)
		self.__sigid2 = editor.connect("quit", self.__quit_cb)
		self.__sigid3 = self.__buffer.connect("insert-text", self.__insert_text_cb)
		self.__sigid4 = self.__buffer.connect("modified-changed", self.__modified_changed_cb)
		self.__sigid5 = editor.connect("checking-file", self.__checking_file_cb)
		self.__sigid6 = editor.connect("loaded-file", self.__loaded_file_cb)
		self.__sigid7 = editor.connect("load-error", self.__load_error_cb)
		self.__sigid8 = editor.connect("saved-file", self.__saved_file_cb)
		self.__sigid9 = editor.connect("undo", self.__undo_cb)
		self.__sigid10 = editor.connect("redo", self.__redo_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monid1 = monitor_add(self.__theme_database_uri, MONITOR_FILE, self.__theme_changed_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__processing = False
		from os.path import join
		preference_folder = join(editor.metadata_folder, "Preferences")
		theme_database_path = join(preference_folder, "ColorTheme.gdb")
		from gnomevfs import get_uri_from_local_path
		self.__theme_database_uri = get_uri_from_local_path(theme_database_path)
		return False

	def __destroy(self):
		from gnomevfs import monitor_cancel
		monitor_cancel(self.__monid1)
		self.__editor.disconnect_signal(self.__sigid1, self.__buffer)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__buffer)
		self.__editor.disconnect_signal(self.__sigid4, self.__buffer)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.disconnect_signal(self.__sigid6, self.__editor)
		self.__editor.disconnect_signal(self.__sigid7, self.__editor)
		self.__editor.disconnect_signal(self.__sigid8, self.__editor)
		self.__editor.disconnect_signal(self.__sigid9, self.__editor)
		self.__editor.disconnect_signal(self.__sigid10, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __set_properties(self):
		self.__buffer.begin_not_undoable_action()
		mgr = self.__editor.style_scheme_manager
		from ColorThemeMetadata import get_value
		style_scheme = mgr.get_scheme(get_value())
		if style_scheme: self.__buffer.set_style_scheme(style_scheme)
		self.__buffer.set_property("highlight-syntax", True)
		self.__buffer.set_property("highlight-matching-brackets", False)
		self.__buffer.set_property("max-undo-levels", -1)
		self.__buffer.set_text("")
		start, end = self.__buffer.get_bounds()
		self.__buffer.remove_all_tags(start, end)
		self.__buffer.remove_source_marks(start, end)
		if self.__buffer.get_modified(): self.__buffer.set_modified(False)
		self.__buffer.notify("cursor-position")
		self.__buffer.end_not_undoable_action()
		return

	def __undo(self):
		if self.__buffer.can_undo(): return self.__buffer.undo()
		print "Cannot undo"
		return False

	def __redo(self):
		if self.__buffer.can_redo(): return self.__buffer.redo()
		print "Cannot redo"
		return

	def __stop_update_cursor_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__cursor_update_timer)
		except:
			pass
		return

	def __update_cursor_position(self, quit=False):
		if not (self.__editor.uri): return False
		cursor = self.__editor.cursor
		cursor_line = cursor.get_line()
		cursor_index = cursor.get_line_index()
		cursor_position = cursor_line, cursor_index
		from CursorMetadata import set_value
		if quit:
			if self.__editor.uri: set_value(str(self.__editor.uri), cursor_position)
		else:
			from thread import start_new_thread
			start_new_thread(set_value, (str(self.__editor.uri), cursor_position))
		return False

	def __set_cursor_position(self):
		try:
			from CursorMetadata import get_value
			position = get_value(self.__editor.uri)
			cursor_line, cursor_index = position[0] + 1, position[1]
		except TypeError:
			cursor_line, cursor_index = 1, 0
		start_iterator = self.__buffer.get_start_iter()
		number_of_lines = self.__buffer.get_line_count()
		if cursor_line > number_of_lines:
			self.__buffer.place_cursor(start_iterator)
			return False
		iterator = self.__buffer.get_iter_at_line(cursor_line - 1)
		line_index = iterator.get_bytes_in_line()
		if cursor_index > line_index:
			iterator.set_line_index(line_index)
		else:
			iterator.set_line_index(cursor_index)
		self.__buffer.place_cursor(iterator)
		self.__editor.move_view_to_cursor()
		return False

################################################################################
#
#							Signal Listeners
#
################################################################################

	def __cursor_position_cb(self, *args):
		self.__editor.emit("cursor-moved")
		self.__stop_update_cursor_timer()
		from gobject import timeout_add
		self.__cursor_update_timer = timeout_add(1000, self.__update_cursor_position, priority=9999)
		return False

	def __insert_text_cb(self, buffer_, iter, text, length, *args):
		if length > 1: return False
		#FIXME: Experimental code, remove if you have problems.
		from gobject import idle_add
		idle_add(self.__editor.response)
		return False

	def __modified_changed_cb(self, *args):
		self.__editor.emit("modified-file", self.__buffer.get_modified())
		return False

	def __checking_file_cb(self, *args):
		self.__buffer.begin_not_undoable_action()
		self.__buffer.set_language(self.__editor.language_object)
		self.__buffer.handler_block(self.__sigid4)
		if self.__buffer.get_modified(): self.__buffer.set_modified(False)
		return False

	def __loaded_file_cb(self, *args):
		self.__set_cursor_position()
		if self.__buffer.get_modified(): self.__buffer.set_modified(False)
		self.__buffer.handler_unblock(self.__sigid4)
		self.__buffer.end_not_undoable_action()
		return False

	def __load_error_cb(self, *args):
		self.__buffer.set_language(None)
		if self.__buffer.get_modified(): self.__buffer.set_modified(False)
		self.__buffer.handler_unblock(self.__sigid4)
		self.__buffer.end_not_undoable_action()
		return False

	def __saved_file_cb(self, *args):
		if self.__buffer.get_modified(): self.__buffer.set_modified(False)
		return False

	def __undo_cb(self, *args):
		self.__undo()
		return False

	def __redo_cb(self, *args):
		self.__redo()
		return False

	def __quit_cb(self, *args):
		self.__stop_update_cursor_timer()
		self.__update_cursor_position(True)
		self.__destroy()
		return False

################################################################################
#
#					Preferences Database Listeners
#
################################################################################

	def __theme_changed_cb(self, *args):
		from ColorThemeMetadata import get_value
		style_scheme = self.__editor.style_scheme_manager.get_scheme(get_value())
		if style_scheme: self.__buffer.set_style_scheme(style_scheme)
		self.__editor.refresh()
		return False


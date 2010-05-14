'''
High-level editor interface that communicates with underlying editor (like
Espresso, Coda, etc.) or browser.
Basically, you should call <code>set_context(obj)</code> method to
set up undelying editor context before using any other method.

This interface is used by <i>zen_actions.py</i> for performing different
actions like <b>Expand abbreviation</b>

@example
import zen_editor
zen_editor.set_context(obj);
//now you are ready to use editor object
zen_editor.get_selection_range();

@author Sergey Chikuyonok (serge.che@gmail.com)
@link http://chikuyonok.ru
'''

class ZenEditor(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__view = editor.textview
		self.__manager = manager
		return

	def set_context(self, context):
		"""
		Setup underlying editor context. You should call this method
		<code>before</code> using any Zen Coding action.
		@param context: context object
		"""
		self.context = context
#		default_locale = locale.getdefaultlocale()[0]
#		lang = re.sub(r'_[^_]+$', '', default_locale)
		from zen_core import set_caret_placeholder, set_variable
		set_caret_placeholder('')
#		if lang != default_locale:
#			set_variable('lang', lang)
#			set_variable('locale', default_locale.replace('_', '-'))
#		else:
#			set_variable('lang', default_locale)
#			set_variable('locale', default_locale)
#		self.encoding = self.document.get_encoding().get_charset()
#		set_variable('charset', self.encoding)
		if self.__view.get_insert_spaces_instead_of_tabs():
			set_variable('indentation', " " * self.__view.get_tab_width())
		else:
			set_variable('indentation', "\t")
		return

	def get_selection_range(self):
		"""
		Returns character indexes of selected text
		@return: list of start and end indexes
		@example
		start, end = zen_editor.get_selection_range();
		print('%s, %s' % (start, end))
		"""
		cursor_offset = self.__editor.cursor.get_offset()
		if self.__editor.has_selection is False: return cursor_offset, cursor_offset
		start, end = self.__editor.selection_bounds
		return start.get_offset(), end.get_offset()

	def create_selection(self, start, end=None):
		"""
		Creates selection from <code>start</code> to <code>end</code> character
		indexes. If <code>end</code> is ommited, this method should place caret
		and <code>start</code> index
		@type start: int
		@type end: int
		@example
		zen_editor.create_selection(10, 40)
		# move caret to 15th character
		zen_editor.create_selection(15)
		"""
		try:
			get_iterator = self.__buffer.get_iter_at_offset
			start_iterator = get_iterator(start)
			if end is None: raise ValueError
			end_iterator = get_iterator(end)
			self.__buffer.select_range(start_iterator, end_iterator)
		except ValueError:	
			self.__buffer.place_cursor(start_iterator)
		return

	def get_current_line_range(self):
		"""
		Returns current line's start and end indexes
		@return: list of start and end indexes
		@example
		start, end = zen_editor.get_current_line_range();
		print('%s, %s' % (start, end))
		"""
		start = self.__editor.backward_to_line_begin()
		end = self.__editor.forward_to_line_end()
		return start.get_offset(), end.get_offset()

	def get_caret_pos(self):
		""" Returns current caret position """
		return self.__editor.cursor.get_offset()

	def set_caret_pos(self, pos):
		"""
		Set new caret position
		@type pos: int
		"""
		iterator = self.__buffer.get_iter_at_offset(pos)
		self.__buffer.place_cursor(iterator)
		return

	def get_current_line(self):
		"""
		Returns content of current line
		@return: str
		"""
		return self.__editor.get_line_text()

	def replace_content(self, value, start=None, end=None):
		"""
		Replace editor's content or it's part (from <code>start</code> to
		<code>end</code> index). If <code>value</code> contains
		<code>caret_placeholder</code>, the editor will put caret into
		this position. If you skip <code>start</code> and <code>end</code>
		arguments, the whole target's content will be replaced with
		<code>value</code>.

		If you pass <code>start</code> argument only,
		the <code>value</code> will be placed at <code>start</code> string
		index of current content.

		If you pass <code>start</code> and <code>end</code> arguments,
		the corresponding substring of current target's content will be
		replaced with <code>value</code>
		@param value: Content you want to paste
		@type value: str
		@param start: Start index of editor's content
		@type start: int
		@param end: End index of editor's content
		@type end: int
		"""
		if start is None and end is None:
			iter_start, iter_end = self.__buffer.get_bounds()
		elif end is None:
			iter_start = self.__buffer.get_iter_at_offset(start)
			iter_end = iter_start.copy()
		else:
			iter_start = self.__buffer.get_iter_at_offset(start)
			iter_end = self.__buffer.get_iter_at_offset(end)
		self.__buffer.begin_user_action()
		self.__buffer.delete(iter_start, iter_end)
		start_insertion_offset = self.__editor.cursor.get_offset()
		from zen_actions import get_current_line_padding
		padding = get_current_line_padding(self)
		from zen_core import pad_string
		self.__buffer.insert_at_cursor(pad_string(value, padding))
		end_insertion_offset = self.__editor.cursor.get_offset()
		self.__buffer.end_user_action()
		self.__manager.emit("insertion-offsets", (start_insertion_offset, end_insertion_offset))
		return

	def get_content(self):
		"""
		Returns editor's content
		@return: str
		"""
		return self.__editor.text

	def get_syntax(self):
		"""
		Returns current editor's syntax mode
		@return: str
		"""
		language = self.__editor.language
		if language.lower() == "html": return "html"
		if language.lower() == "css": return "css"
		if language.lower() in ("xslt", "xsl"): return "xsl"

	def get_profile_name(self):
		"""
		Returns current output profile name (@see zen_coding#setup_profile)
		@return {String}
		"""
		return 'xhtml'

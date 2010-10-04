from gtk import ImageMenuItem
from gettext import gettext as _

class PopupMenuItem(ImageMenuItem):

	def __init__(self, editor):
		editor.response()
		ImageMenuItem.__init__(self, _("Selection"))
		self.__init_attributes(editor)
		self.__creates_widgets()
		self.__set_properties()
		self.__signal_id_1 = self.select_word_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_2 = self.select_line_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_3 = self.select_sentence_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_4 = self.paragraph_item.connect("activate", self.__popup_activate_cb)
		self.__signal_id_5 = self.select_word_menuitem.connect("map-event", self.__popup_word_map_event_cb)
		self.__signal_id_6 = self.select_line_menuitem.connect("map-event", self.__popup_line_map_event_cb)
		self.__signal_id_7 = self.select_sentence_menuitem.connect("map-event", self.__popup_sentence_map_event_cb)
		self.__signal_id_9 = self.scribesview.connect("focus-in-event", self.__focus_in_event_cb)
		editor.response()

	def __init_attributes(self, editor):
		self.scribesview = editor.textview
		self.editor = editor
		self.menu = None
		self.image = None
		self.select_word_menuitem = None
		self.select_line_menuitem = None
		self.select_sentence_menuitem = None
		return

	def __creates_widgets(self):
		from gtk import Image, STOCK_BOLD, Menu
		self.image = Image()
		self.image.set_property("stock", STOCK_BOLD)
		self.menu = Menu()
		self.select_word_menuitem = self.editor.create_menuitem(_("Select word (alt + w)"))
		self.select_line_menuitem = self.editor.create_menuitem(_("Select line (alt + l)"))
		self.select_sentence_menuitem = self.editor.create_menuitem(_("Select sentence (alt + s)"))
		self.paragraph_item = self.editor.create_menuitem(_("Select paragraph (alt + p)"))
		return

	def __set_properties(self):
		self.set_image(self.image)
		self.set_submenu(self.menu)
		self.menu.append(self.select_line_menuitem)
		self.menu.append(self.select_word_menuitem)
		self.menu.append(self.select_sentence_menuitem)
		self.menu.append(self.paragraph_item)
		if self.editor.readonly: self.set_property("sensitive", False)
		return

	def __popup_activate_cb(self, menuitem):
		if menuitem == self.select_word_menuitem:
			self.editor.trigger("select-word")
		elif menuitem == self.select_line_menuitem:
			self.editor.trigger("select-line")
		elif menuitem == self.select_sentence_menuitem:
			self.editor.trigger("select-sentence")
		elif menuitem == self.paragraph_item:
			self.editor.trigger("select-paragraph")
		return True

	def __popup_word_map_event_cb(self, menuitem, event):
		menuitem.set_property("sensitive", False)
		from word import inside_word, starts_word, ends_word
		cursor_position = self.editor.get_cursor_iterator()
		if inside_word(cursor_position) or starts_word(cursor_position) or ends_word(cursor_position):
			menuitem.set_property("sensitive", True)
		return True

	def __popup_line_map_event_cb(self, menuitem, event):
		menuitem.set_property("sensitive", False)
		from lines import get_line_bounds
		begin_position, end_position = get_line_bounds(self.editor.textbuffer)
		if not begin_position.get_char() in ["\n", "\x00"]:
			menuitem.set_property("sensitive", True)
		return True

	def __popup_sentence_map_event_cb(self, menuitem, event):
		menuitem.set_property("sensitive", False)
		cursor_position = self.editor.get_cursor_iterator()
		if cursor_position.starts_sentence() or cursor_position.ends_sentence() or cursor_position.inside_sentence():
			menuitem.set_property("sensitive", True)
		return True

	def __focus_in_event_cb(self, event, textview):
		self.editor.disconnect_signal(self.__signal_id_1, self.select_word_menuitem)
		self.editor.disconnect_signal(self.__signal_id_2, self.select_line_menuitem)
		self.editor.disconnect_signal(self.__signal_id_3, self.select_sentence_menuitem)
		self.editor.disconnect_signal(self.__signal_id_4, self.select_sentence_menuitem)
		self.editor.disconnect_signal(self.__signal_id_5, self.select_word_menuitem)
		self.editor.disconnect_signal(self.__signal_id_6, self.select_line_menuitem)
		self.editor.disconnect_signal(self.__signal_id_7, self.select_sentence_menuitem)
		self.editor.disconnect_signal(self.__signal_id_9, self.scribesview)
		if self.select_word_menuitem: self.select_word_menuitem.destroy()
		if self.select_sentence_menuitem: self.select_sentence_menuitem.destroy()
		if self.select_line_menuitem: self.select_line_menuitem.destroy()
		if self.image: self.image.destroy()
		if self.menu: self.menu.destroy()
		del self
		self = None
		return False

from gtk import ImageMenuItem

class IndentPopupMenuItem(ImageMenuItem):

	def __init__(self, editor):
		from i18n import msg0008
		ImageMenuItem.__init__(self, msg0008)
		self.__init_attributes(editor)
		self.__create_wigets()
		self.__set_properties()
		self.__signal_id_1 = self.indent_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_2 = self.unindent_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_3 = self.unindent_menuitem.connect("map-event", self.__popup_map_event_cb)
		self.__signal_id_4 = self.scribesview.connect("focus-in-event", self.__popup_focus_event_cb)

	def __init_attributes(self, editor):
		self.scribesview = editor.textview
		self.editor = self.__editor = editor
		self.menu = None
		self.image = None
		self.indent_menuitem = None
		self.unindent_menuitem = None
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		self.__signal_id_3 = None
		self.__signal_id_4 = None
		return

	def __create_wigets(self):
		from gtk import Image, STOCK_JUSTIFY_CENTER, Menu
		self.image = Image()
		self.image.set_property("stock", STOCK_JUSTIFY_CENTER)
		self.menu = Menu()
		from i18n import msg0009, msg0010
		from gtk import STOCK_UNINDENT, STOCK_INDENT
		self.indent_menuitem = self.__editor.create_menuitem(msg0009, STOCK_INDENT)
		self.unindent_menuitem = self.__editor.create_menuitem(msg0010, STOCK_UNINDENT)
		return

	def __set_properties(self):
		self.set_image(self.image)
		self.set_submenu(self.menu)
		self.menu.append(self.indent_menuitem)
		self.menu.append(self.unindent_menuitem)
		if self.editor.is_readonly: self.set_property("sensitive", False)
		return

	def __popup_activate_cb(self, menuitem):
		if menuitem == self.indent_menuitem:
			self.editor.trigger("indent_line")
		if menuitem == self.unindent_menuitem:
			self.editor.trigger("unindent_line")
		return True

	def __popup_map_event_cb(self, menuitem, event):
		menuitem.set_property("sensitive", False)
		cursor_line = self.__editor.get_cursor_line()
		begin_position = self.editor.textbuffer.get_iter_at_line(cursor_line)
		try:
			begin_selection, end_selection = self.editor.textbuffer.get_selection_bounds()
		except ValueError:
			if begin_position.get_char() in [" ", "\t"]:
				menuitem.set_property("sensitive", True)
			else:
				menuitem.set_property("sensitive", False)
			return True
		first_selected_line = begin_selection.get_line()
		last_selected_line = end_selection.get_line()
		if first_selected_line == last_selected_line:
			if begin_position.get_char() in [" ", "\t"]:
				menuitem.set_property("sensitive", True)
			else:
				menuitem.set_property("sensitive", False)
			return True
		indentation_is_possible = False
		for line in range(first_selected_line, last_selected_line+1):
			begin_position = self.editor.textbuffer.get_iter_at_line(line)
			if begin_position.get_char() in [" ", "\t"]:
				indentation_is_possible = True
		menuitem.set_property("sensitive", indentation_is_possible)
		return True

	def __popup_focus_event_cb(self, event, textview):
		self.__editor.disconnect_signal(self.__signal_id_1, self.indent_menuitem)
		self.__editor.disconnect_signal(self.__signal_id_2, self.unindent_menuitem)
		self.__editor.disconnect_signal(self.__signal_id_3, self.unindent_menuitem)
		self.__editor.disconnect_signal(self.__signal_id_4, self.scribesview)
		if self.indent_menuitem: self.indent_menuitem.destroy()
		if self.unindent_menuitem: self.unindent_menuitem.destroy()
		if self.menu: self.menu.destroy()
		if self.image: self.image.destroy()
		self.destroy()
		del self
		self = None
		return False

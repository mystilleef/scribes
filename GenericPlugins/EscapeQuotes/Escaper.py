class Escaper(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("escape", self.__escape_cb)
		self.__sigid3 = manager.connect("unescape", self.__unescape_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return

	def __escape(self):
		textbuffer = self.__editor.textbuffer
		selection = textbuffer.get_selection_bounds()
		if not selection: 
			message = _("No selection found")
			self.__editor.update_message(message, "pass")		   
			return False
	
		text = textbuffer.get_text(selection[0], selection[1])
		if not text: 
			message = _("No selected text found")
			self.__editor.update_message(message, "pass")		   
			return False
	
		new_text = ""
		num_quotes = 0;
		prev_ch = text[0] # Used to see if char has been replaced already
		for ch in text:
			if ch == '"' and not prev_ch == "\\":
				new_text += "\\\""
				num_quotes += 1	
			else:
				new_text += ch
			prev_ch = ch
			
			
		textbuffer.begin_user_action()		
		textbuffer.delete(selection[0], selection[1])		
		
		textbuffer.insert_at_cursor(new_text)
		
		# Restore the selection, including the new backward slashes
		select_start_mark = textbuffer.get_insert()
		select_start = textbuffer.get_iter_at_mark(select_start_mark)
		select_end = textbuffer.get_iter_at_mark(select_start_mark)
		select_end.backward_chars(len(new_text))
		textbuffer.select_range(select_start, select_end)
		
		textbuffer.end_user_action()
		
		message = _("Escaped %d quote(s) in selected text" % num_quotes)
		self.__editor.update_message(message, "pass")
		return

	def __unescape(self):
		textbuffer = self.__editor.textbuffer
		selection = textbuffer.get_selection_bounds()
		if not selection: 
			message = _("No selection found")
			self.__editor.update_message(message, "pass")		   
			return False
	
		text = textbuffer.get_text(selection[0], selection[1])
		if not text: 
			message = _("No selected text found")
			self.__editor.update_message(message, "pass")		   
			return False
		
		num_quotes = text.count("\\\"")
		new_text = text.replace("\\\"",'"')
		
		textbuffer.begin_user_action()
		textbuffer.delete(selection[0], selection[1])
		textbuffer.insert_at_cursor(new_text)
		
		# Restore the selection, including the removed backward slashes
		select_start_mark = textbuffer.get_insert()
		select_start = textbuffer.get_iter_at_mark(select_start_mark)
		select_end = textbuffer.get_iter_at_mark(select_start_mark)
		select_end.backward_chars(len(new_text))
		textbuffer.select_range(select_start, select_end)
		
		textbuffer.end_user_action()
		
		
		message = _("Unescaped %d quote(s) in selected text" % num_quotes)
		self.__editor.update_message(message, "pass")
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __escape_cb(self, *args):
		self.__escape()
		return False

	def __unescape_cb(self, *args):
		self.__unescape()
		return False

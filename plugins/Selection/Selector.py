from gettext import gettext as _

class Selector(object):
	
	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("select-word", self.__select_word_cb)
		self.__sigid2 = manager.connect("destroy", self.__destroy_cb)
		
	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return 
	
	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return 
	
	def __select_word(self):
		try:
			if self.__editor.inside_word(self.__editor.cursor) is False: raise ValueError
			start, end = self.__editor.get_word_boundary(self.__editor.cursor)
			self.__editor.textbuffer.select_range(start, end)
			self.__editor.update_message(_("Selected word"), "pass")
		except ValueError:
			self.__editor.update_message(_("No word found to select"), "fail")
		return False
	
	def __select_word_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__select_word, priority=9999)
		return False
	
	def __destroy_cb(self, *args):
		self.__destroy()
		return False

class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__trigger1.connect("activate", self.__delete_line_cb)
		self.__sigid2 = self.__trigger2.connect("activate", self.__join_line_cb)
		self.__sigid3 = self.__trigger3.connect("activate", self.__line_above_cb)
		self.__sigid4 = self.__trigger4.connect("activate", self.__line_below_cb)
		self.__sigid5 = self.__trigger5.connect("activate", self.__cursor_to_end_cb)
		self.__sigid6 = self.__trigger6.connect("activate", self.__cursor_to_start_cb)
		self.__sigid7 = self.__trigger7.connect("activate", self.__duplicate_line_cb)
		self.__sigid8 = editor.textview.connect("populate-popup", self.__popup_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__manager = None
		self.__trigger1 = self.__create_trigger("delete_line", "<alt>d")
		self.__trigger2 = self.__create_trigger("join_line", "<alt>j")
		self.__trigger3 = self.__create_trigger("free_line_above", "<alt><shift>o")
		self.__trigger4 = self.__create_trigger("free_line_below", "<alt>o")
		self.__trigger5 = self.__create_trigger("delete_cursor_to_end", "<alt>End")
		self.__trigger6 = self.__create_trigger("delete_cursor_to_begin", "<alt>Home")
		self.__trigger7 = self.__create_trigger("duplicate_line", "<ctrl><shift>d")
		return

	def __destroy(self):
		if self.__manager: self.__manager.destroy()
		self.__editor.remove_triggers((self.__trigger1, self.__trigger2,
		self.__trigger3, self.__trigger4, self.__trigger5, 
		self.__trigger6, self.__trigger7))
		self.__editor.disconnect_signal(self.__sigid1, self.__trigger1)
		self.__editor.disconnect_signal(self.__sigid2, self.__trigger2)
		self.__editor.disconnect_signal(self.__sigid3, self.__trigger3)
		self.__editor.disconnect_signal(self.__sigid4, self.__trigger4)
		self.__editor.disconnect_signal(self.__sigid5, self.__trigger5)
		self.__editor.disconnect_signal(self.__sigid6, self.__trigger6)
		self.__editor.disconnect_signal(self.__sigid7, self.__trigger7)
		self.__editor.disconnect_signal(self.__sigid8, self.__editor.textview)
		del self
		self = None
		return False

	def __get_manager(self):
		if self.__manager: return self.__manager
		from Manager import Manager
		self.__manager = Manager(self.__editor)
		return self.__manager

	def __create_trigger(self, name, shortcut):
		trigger = self.__editor.create_trigger(name, shortcut)
		self.__editor.add_trigger(trigger)
		return trigger

	def __delete_line_cb(self, *args):
		self.__get_manager().delete_line()
		return

	def __duplicate_line_cb(self, *args):
		self.__get_manager().duplicate_line()
		return

	def __join_line_cb(self, *args):
		self.__get_manager().join_line()
		return

	def __line_above_cb(self, *args):
		self.__get_manager().free_line_above()
		return

	def __line_below_cb(self, *args):
		self.__get_manager().free_line_below()
		return

	def __cursor_to_end_cb(self, *args):
		self.__get_manager().delete_cursor_to_end()
		return

	def __cursor_to_start_cb(self, *args):
		self.__get_manager().delete_cursor_to_start()
		return

	def __popup_cb(self, *args):
		from PopupMenuItem import PopupMenuItem
		self.__editor.add_to_popup(PopupMenuItem(self.__editor))
		return False

	def destroy(self):
		self.__destroy()
		return

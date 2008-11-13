class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.textview.connect_after("populate-popup", self.__popup_cb)
		self.__sigid2 = self.__trigger1.connect("activate", self.__toggle_bookmark_cb)
		self.__sigid3 = self.__trigger2.connect("activate", self.__remove_all_bookmarks_cb)
		self.__sigid4 = self.__trigger3.connect("activate", self.__show_browser_cb)

	def __init_attributes(self, editor):
		from Manager import Manager
		self.__manager = Manager(editor)
		self.__editor = editor
		self.__trigger1 = self.__create_trigger("toggle-bookmark", "ctrl+d")
		self.__trigger2 = self.__create_trigger("remove-all-bookmarks", "ctrl+shift+b")
		self.__trigger3 = self.__create_trigger("show-bookmark-browser", "ctrl+b")
		self.__browser = None
		return

	def __create_trigger(self, name, shortcut):
		trigger = self.__editor.create_trigger(name, shortcut)
		self.__editor.add_trigger(trigger)
		return trigger

	def destroy(self):
		triggers = (self.__trigger1, self.__trigger2, self.__trigger3)
		self.__editor.remove_triggers(triggers)
		self.__editor.disconnect_signal(self.__sigid1, self.__editor.textview)
		self.__editor.disconnect_signal(self.__sigid2, self.__trigger1)
		self.__editor.disconnect_signal(self.__sigid3, self.__trigger2)
		self.__editor.disconnect_signal(self.__sigid4, self.__trigger3)
		del self
		self = None
		return

	def __popup_cb(self, textview, menu):
		from PopupMenuItem import PopupMenuItem
		menu.prepend(PopupMenuItem(self.__editor))
		menu.show_all()
		return False

	def __toggle_bookmark_cb(self, *args):
		self.__manager.toggle_bookmark()
		return False

	def __remove_all_bookmarks_cb(self, *args):
		self.__manager.remove_bookmarks()
		return False

	def __show_browser_cb(self, *args):
		try:
			self.__browser.show()
		except AttributeError:
			from GUI.Manager import Manager
			self.__browser = Manager(self.__manager, self.__editor)
			self.__browser.show()
		return False

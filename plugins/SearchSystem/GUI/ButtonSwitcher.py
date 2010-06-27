class Switcher(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid4 = manager.connect("found-matches", self.__found_matches_cb)
		self.__sigid2 = manager.connect("search", self.__search_cb)
		self.__sigid3 = manager.connect("reset", self.__reset_cb)
		self.__sigid5 = manager.connect("hide-bar", self.__reset_cb)
		self.__sigid6 = manager.connect("search-string", self.__reset_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__search_button = manager.gui.get_widget("FindButton")
		self.__stop_button = manager.gui.get_widget("StopButton")
		self.__next_button = manager.gui.get_widget("NextButton")
		self.__hbox = manager.gui.get_widget("HBox")
		self.__matches = []
		self.__current_button = ""
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		del self
		self = None
		return

	def __hide_buttons(self):
		self.__stop_button.hide()
		self.__search_button.hide()
		self.__next_button.hide()
		return False

	def __change_button(self, matches):
		show = self.__show_button
		nbutton = self.__next_button
		sbutton = self.__search_button
		show(nbutton) if len(matches) > 1 else show(sbutton)
		return

	def __show_button(self, button):
		self.__editor.response()
		self.__hide_buttons()
		button.show()
		self.__manager.set_data("activate_button", button)
		self.__editor.response()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __search_cb(self, *args):
		self.__show_button(self.__stop_button)
		return False

	def __found_matches_cb(self, manager, matches):
		self.__change_button(matches)
		return False

	def __reset_cb(self, *args):
		self.__show_button(self.__search_button)
		return False

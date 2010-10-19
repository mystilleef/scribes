from gtk import RecentChooserMenu

class RecentMenu(RecentChooserMenu):

	def __init__(self, editor):
		self.__init_attributes(editor)
		manager = editor.get_data("RecentManager")
		RecentChooserMenu.__init__(self, manager)
		self.__set_properties()
		self.__sigid1 = self.__editor.connect("quit", self.__quit_cb)
		self.__sigid2 = self.connect("item-activated", self.__activated_cb)
		editor.set_data("RecentMenu", self)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		return

	def __set_properties(self):
		from ..Utils import never_focus
		never_focus(self)
		from gtk import RECENT_SORT_MRU
		self.set_show_numbers(False)
		self.set_property("sort-type", RECENT_SORT_MRU)
		self.set_property("filter", self.__create_filter())
		self.set_property("limit", 15)
		self.set_property("local-only", False)
		self.set_property("show-icons", True)
		self.set_property("show-not-found", False)
		self.set_property("show-tips", True)
		from gettext import gettext as _
		self.set_tooltip_text(_("Recently opened files"))
		return

	def __create_filter(self):
		from gtk import RecentFilter
		recent_filter = RecentFilter()
		recent_filter.add_application("scribes")
		return recent_filter

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self)
		self.destroy()
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __activated_cb(self, recent_chooser):
		uri = self.get_current_uri()
		self.__editor.open_file(uri)
		return True

	def __quit_cb(self, editor):
		self.__destroy()
		return

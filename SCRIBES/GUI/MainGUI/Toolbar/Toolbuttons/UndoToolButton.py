from gtk import ToolButton

class Button(ToolButton):

	def __init__(self, editor):
		ToolButton.__init__(self)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = self.connect("clicked", self.__clicked_cb)
		self.__sigid3 = editor.connect_after("undo", self.__undo_cb)
		self.__sigid4 = editor.connect_after("redo", self.__undo_cb)
		self.__sigid5 = editor.connect("modified-file", self.__undo_cb)
		self.__sigid6 = editor.connect("bar-is-active", self.__active_cb)
		editor.register_object(self)
		self.show()

	def __init_attributes(self, editor):
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.disconnect_signal(self.__sigid6, self.__editor)
		self.__editor.unregister_object(self)
		del self
		return

	def __set_properties(self):
		from ..Utils import never_focus
		never_focus(self)
		from gtk import STOCK_UNDO
		self.set_property("stock-id", STOCK_UNDO)
		self.set_property("name", "UndoToolButton")
		self.set_property("sensitive", False)
		from gettext import gettext as _
		self.set_tooltip_text(_("Undo last action (ctrl + z)"))
		return

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __sensitive(self):
		sensitive = True if self.__editor.textbuffer.can_undo() else False
		self.set_property("sensitive", sensitive)
		return False

	def __clicked_cb(self, *args):
		self.__editor.undo()
		self.__sensitive()
		return False

	def __undo_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__sensitive)
#		self.__sensitive()
		return False

	def __active_cb(self, editor, active):
		self.set_property("sensitive", False) if active else self.__sensitive()
		return False

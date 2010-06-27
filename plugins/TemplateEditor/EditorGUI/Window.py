from gettext import gettext as _

class Window(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("show-add-template-editor", self.__add_cb)
		self.__sigid3 = manager.connect("hide-template-editor", self.__hide_cb)
		self.__sigid4 = self.__window.connect("delete-event", self.__delete_event_cb)
		self.__sigid5 = self.__window.connect("key-press-event", self.__key_press_event_cb)
		self.__sigid6 = manager.connect("show-edit-template-editor", self.__edit_cb)
		self.__sigid7 = manager.connect("ready", self.__show_cb)
		self.__sigid8 = manager.connect("updating-database", self.__delete_event_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__window = manager.editor_gui.get_widget("Window")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__window)
		self.__editor.disconnect_signal(self.__sigid5, self.__window)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		self.__editor.disconnect_signal(self.__sigid7, self.__manager)
		self.__editor.disconnect_signal(self.__sigid8, self.__manager)
		self.__window.destroy()
		del self
		self = None
		return False

	def __set_properties(self):
		window = self.__manager.gui.get_widget("Window")
		self.__window.set_transient_for(window)
		return False

	def __show(self):
		self.__window.show_all()
		return False

	def __hide(self):
		self.__window.hide()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __hide_cb(self, *args):
		self.__hide()
		return False

	def __show_cb(self, *args):
		self.__show()
		return False

	def __delete_event_cb(self, *args):
		self.__manager.emit("hide-template-editor")
		return True

	def __key_press_event_cb(self, window, event):
		from gtk.keysyms import Escape
		if event.keyval != Escape: return False
		self.__manager.emit("hide-template-editor")
		return True

	def __add_cb(self, *args):
		self.__window.set_title(_("Add Template"))
		return False

	def __edit_cb(self, *args):
		self.__window.set_title(_("Edit Template"))
		return False

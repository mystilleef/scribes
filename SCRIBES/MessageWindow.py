from gettext import gettext as _

class Window(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = self.__window.connect("delete-event", self.__delete_event_cb)
		self.__sigid3 = self.__window.connect("key-press-event", self.__key_press_event_cb)
		self.__sigid4 = self.__button.connect("clicked", self.__clicked_cb)
		self.__sigid5 = editor.connect("show-error", self.__show_error_cb)
		self.__sigid6 = editor.connect("show-info", self.__show_info_cb)
		editor.register_object(self)
		
	def __init_attributes(self, editor):
		self.__editor = editor
		from os.path import join
		glade_file = join(editor.data_folder, "MessageWindow.glade")
		from gtk.glade import XML
		glade = XML(glade_file, "Window", "scribes")
		self.__image = glade.get_widget("Image")
		self.__window = glade.get_widget("Window")
		self.__title_label = glade.get_widget("TitleLabel")
		self.__message_label = glade.get_widget("MessageLabel")
		self.__button = glade.get_widget("CloseButton")
		self.__busy = False
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__window)
		self.__editor.disconnect_signal(self.__sigid3, self.__window)
		self.__editor.disconnect_signal(self.__sigid4, self.__button)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.disconnect_signal(self.__sigid6, self.__editor)
		self.__window.destroy()
		self.__editor.unregister_object(self)
		del self
		self = None
		return False
	
	def __hide(self):
		if self.__busy: self.__editor.busy(False)
		self.__busy = False
		self.__window.hide()
		return False

	def __show(self, error, title, message, window, busy):
		self.__window.set_title(_("ERROR")) if error else self.__window.set_title(_("INFORMATION"))
		from gtk import ICON_SIZE_DIALOG as DIALOG, STOCK_DIALOG_ERROR as ERROR
		from gtk import STOCK_DIALOG_INFO as INFO
		self.__image.set_from_stock(ERROR, DIALOG) if error else self.__image.set_from_stock(INFO, DIALOG)
		self.__title_label.set_label("<b>" + title + "</b>")
		self.__message_label.set_label(message)
		self.__window.set_transient_for(window)
		self.__busy = busy
		if busy: self.__editor.busy()
		self.__window.show_all()
		return False

	def __show_error_cb(self, editor, title, message, window, busy):
		self.__show(True, title, message, window, busy)
		return False

	def __show_info_cb(self, editor, title, message, window, busy):
		self.__show(False, title, message, window, busy)
		return False

	def __clicked_cb(self, *args):
		self.__hide()
		return False

	def __delete_event_cb(self, *args):
		self.__hide()
		return True

	def __key_press_event_cb(self, window, event):
		from gtk import keysyms
		if event.keyval != keysyms.Escape: return False
		self.__hide()
		return True

	def __quit_cb(self, *args):
		self.__destroy()
		return False

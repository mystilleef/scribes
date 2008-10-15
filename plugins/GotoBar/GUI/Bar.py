from gettext import gettext as _
message = _("Move cursor to a specific line")

class Bar(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("hide-bar", self.__hide_cb)
		self.__sigid3 = manager.connect("show-bar", self.__show_cb)
		self.__sigid4 = editor.textview.connect("focus-in-event", self.__hide_cb)
		self.__sigid5 = editor.textview.connect("button-press-event", self.__hide_cb)
		self.__block_signals()
		
	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__container = manager.gui.get_widget("HBox")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor.textview)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor.textview)
		del self
		self = None
		return 

	def __block_signals(self):
		self.__editor.textview.handler_block(self.__sigid4)
		self.__editor.textview.handler_block(self.__sigid5)
		return False
	
	def __unblock_signals(self):
		self.__editor.textview.handler_unblock(self.__sigid4)
		self.__editor.textview.handler_unblock(self.__sigid5)
		return False

	def __hide(self):
		from SCRIBES.Exceptions import BarBoxInvalidObjectError
		try:
			self.__editor.remove_bar_object(self.__container)
			self.__block_signals()
			self.__editor.unset_message(message, "scribes")
			self.__editor.textview.grab_focus()
		except BarBoxInvalidObjectError:
			pass
		return False

	def __show(self):
		from SCRIBES.Exceptions import BarBoxAddError
		try:
			self.__editor.add_bar_object(self.__container)
			self.__unblock_signals()
			self.__editor.set_message(message, "scribes")
		except BarBoxAddError:
			pass
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

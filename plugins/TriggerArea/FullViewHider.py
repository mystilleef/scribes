from SCRIBES.SignalConnectionManager import SignalManager

class Hider(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(editor, "toolbar-is-visible", self.__visible_cb)
		self.__sigid1 = self.connect(editor.window, "key-press-event", self.__event_cb)
		self.__block()
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__window = editor.window
		self.__blocked = False
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __block(self):
		if self.__blocked: return False
		self.__window.handler_block(self.__sigid1)
		self.__blocked = True
		return False

	def __unblock(self):
		if self.__blocked is False: return False
		self.__window.handler_unblock(self.__sigid1)
		self.__blocked = False
		return False

	def __event_cb(self, window, event):
		from gtk.keysyms import Escape
		if event.keyval != Escape: return False
		self.__editor.hide_full_view()
		return True

	def __visible_cb(self, editor, visible):
		self.__unblock() if visible else self.__block()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

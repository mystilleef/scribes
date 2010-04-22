#FIXME: This module doesn't work well. Needs to connect to more signals?
# There's a possibility to improve performance if this module works well.
# GTK+ blocks all events on all windows except the focused one.

from SCRIBES.SignalConnectionManager import SignalManager

class Grabber(SignalManager):

	def __init__(self, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(self.__window, "focus-in-event", self.__in_cb, True)
		self.connect(editor, "ready", self.__in_cb, True)
		self.connect(editor, "loaded-file", self.__in_cb, True)
		self.connect(self.__window, "focus-out-event", self.__out_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__window = editor.window
		self.__is_grabbed = False
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __grab(self):
		if self.__is_grabbed: return False
		self.__window.grab_add()
		self.__is_grabbed = True
		print "%i grabbed focus" % self.__editor.id_
		return False
	
	def __ungrab(self):
		if self.__is_grabbed is False: return False
		self.__is_grabbed = False
		self.__window.grab_remove()
		print "%i ungrabbed focus" % self.__editor.id_
		return False

	def __in_cb(self, *args):
		self.__grab()
		return False

	def __out_cb(self, *args):
		self.__ungrab()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		self.connect(editor, "quit", self.__destroy_cb)
		self.connect(self.__vscrollbar, "value-changed", self.__changed_cb, data=True)
		self.connect(self.__hscrollbar, "value-changed", self.__changed_cb, data=False)
		self.connect(editor, "loaded-file", self.__loaded_cb, True)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__vscrollbar = editor.gui.get_widget("ScrolledWindow").get_vscrollbar()
		self.__hscrollbar = editor.gui.get_widget("ScrolledWindow").get_hscrollbar()
		self.__vdelta = False
		self.__hdelta = False
		return

	def __update(self, _range, vertical=True):
		idelta = self.__vdelta if vertical else self.__hdelta
		delta = True if _range.get_value() else False
		if delta == idelta: return False
		if vertical: self.__vdelta = delta
		if vertical is False: self.__hdelta = delta
		self.__editor.emit("scrollbar-visibility-update")
		return True

	def __remove_timer(self, _timer=1):
		try:
			timers = {
				1: self.__timer1,
			}
			from gobject import source_remove
			source_remove(timers[_timer])
		except AttributeError:
			pass
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

	def __changed_cb(self, _range, vertical):
		self.__remove_timer(1)
		from gobject import idle_add, PRIORITY_LOW
		self.__timer1 = idle_add(self.__update, _range, vertical, priority=PRIORITY_LOW)
		return False

	def __loaded_cb(self, *args):
		self.__editor.emit("scrollbar-visibility-update")
		return False

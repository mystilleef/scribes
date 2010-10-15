from SCRIBES.SignalConnectionManager import SignalManager

class Label(SignalManager):

	def __init__(self, manager, editor):
		editor.refresh()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "message", self.__message_cb)
		self.connect(manager, "hide-message", self.__hide_cb)
		editor.refresh()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__label = manager.main_gui.get_object("FeedbackLabel")
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __set_message(self, data):
		_type, message = data
		template = {
			"ERROR": "<span foreground='red'><b>%s</b></span>",
			"INFO": "<span foreground='blue'><b>%s</b></span>",
			"PROGRESS": "<i>%s</i>",
		}
		self.__label.set_markup(template[_type] % message)
		self.__label.show()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __message_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__set_message, data)
		return False

	def __hide_cb(self, *args):
		self.__label.hide()
		return False

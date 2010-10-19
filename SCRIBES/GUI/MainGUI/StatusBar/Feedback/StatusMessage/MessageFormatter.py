class Formatter(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("update-message", self.__update_cb)
		self.__sigid3 = manager.connect("fallback-message", self.__update_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __format(self, message, bold, italic, color):
		try:
			if not message: raise ValueError
			if color: message = "<span foreground='%s'>" % color + message + "</span>"
			if bold: message =  "<b>" + message + "</b>"
			if italic: message = "<i>" + message + "</i>"
		except ValueError:
			message = ""
		finally:
			self.__manager.emit("set-message", message)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __update_cb(self, manager, message, bold, italic, color):
		from gobject import idle_add
		idle_add(self.__format, message, bold, italic, color, priority=9999)
		return False

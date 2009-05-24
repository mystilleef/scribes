from gio import ERROR_NOT_MOUNTED

class Handler(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("gio-error", self.__error_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		# Map GIO Error codes to Scribes signals for errors we want to
		# handle in a special manner.
		self.__dictionary = {
			ERROR_NOT_MOUNTED: "ErrorNotMounted",
			14: "NoFeedbackError",
		}
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __process(self, data):
		try:
			gfile, error = data
			self.__manager.emit(self.__dictionary[error.code], data)
		except KeyError:
			self.__manager.emit("unhandled-gio-error", data)
		return False

	def __error_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__process, data, priority=9999)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

class Label(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("error", self.__error_cb)
		self.__label.hide()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__label = manager.gui.get_widget("ErrorLabel")
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __show_error(self, error):
		try:
			from gobject import timeout_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__show(error)
			self.__timer = timeout_add(10000, self.__hide, priority=9999)
		return False

	def __show(self, error):
		message = "<span foreground='red'><b>%s</b></span>" % error
		self.__label.set_label(message)
		self.__label.show()
		return False

	def __hide(self):
		self.__label.hide()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __error_cb(self, manager, error):
		self.__show_error(error)
		return False

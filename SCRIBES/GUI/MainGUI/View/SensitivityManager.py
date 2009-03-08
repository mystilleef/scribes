class Manager(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("busy", self.__busy_cb)
		self.__sigid3 = editor.connect("ready", self.__ready_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__swin = editor.gui.get_widget("ScrolledWindow")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __sensitive(self, sensitive):
		self.__editor.refresh(False)
		self.__swin.props.sensitive = sensitive
		self.__editor.refresh()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __busy_cb(self, editor, busy):
		self.__sensitive(not busy)
		return False

	def __ready_cb(self, *args):
		self.__sensitive(True)
		return False

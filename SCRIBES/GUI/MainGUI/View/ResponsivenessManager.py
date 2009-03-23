class Manager(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = self.__view.connect("set-scroll-adjustments", self.__response_cb)
		self.__sigid3 = self.__view.connect("backspace", self.__response_cb)
		self.__sigid4 = self.__view.connect("copy-clipboard", self.__response_cb)
		self.__sigid5 = self.__view.connect("cut-clipboard", self.__response_cb)
		self.__sigid6 = self.__view.connect("delete-from-cursor", self.__response_cb)
		self.__sigid7 = self.__view.connect("insert-at-cursor", self.__response_cb)
		self.__sigid8 = self.__view.connect("move-cursor", self.__response_cb)
		self.__sigid9 = self.__view.connect("move-focus", self.__response_cb)
		self.__sigid10 = self.__view.connect("move-viewport", self.__response_cb)
		self.__sigid11 = self.__view.connect("page-horizontally", self.__response_cb)
		self.__sigid12 = self.__view.connect("paste-clipboard", self.__response_cb)
		self.__sigid13 = self.__view.connect("populate-popup", self.__response_cb)
		self.__sigid14 = self.__view.connect("set-anchor", self.__response_cb)
		self.__sigid15 = self.__view.connect("toggle-overwrite", self.__response_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__view = editor.textview
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__view)
		self.__editor.disconnect_signal(self.__sigid3, self.__view)
		self.__editor.disconnect_signal(self.__sigid4, self.__view)
		self.__editor.disconnect_signal(self.__sigid5, self.__view)
		self.__editor.disconnect_signal(self.__sigid6, self.__view)
		self.__editor.disconnect_signal(self.__sigid7, self.__view)
		self.__editor.disconnect_signal(self.__sigid8, self.__view)
		self.__editor.disconnect_signal(self.__sigid9, self.__view)
		self.__editor.disconnect_signal(self.__sigid10, self.__view)
		self.__editor.disconnect_signal(self.__sigid11, self.__view)
		self.__editor.disconnect_signal(self.__sigid12, self.__view)
		self.__editor.disconnect_signal(self.__sigid13, self.__view)
		self.__editor.disconnect_signal(self.__sigid14, self.__view)
		self.__editor.disconnect_signal(self.__sigid15, self.__view)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __response_cb(self, *args):
		self.__editor.response()
		return False

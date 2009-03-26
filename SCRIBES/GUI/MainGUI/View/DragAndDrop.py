class DragAndDrop(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = self.__view.connect("drag-motion", self.__motion_cb)
		self.__sigid3 = self.__view.connect("drag-drop", self.__drop_cb)
		self.__sigid4 = self.__view.connect("drag-data-received", self.__received_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__view = editor.textview
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__view)
		self.__editor.disconnect_signal(self.__sigid3, self.__view)
		self.__editor.disconnect_signal(self.__sigid4, self.__view)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __motion_cb(self, textview, context, x, y, time):
		editor.response()
		if "text/uri-list" in context.targets: return True
		editor.response()
		return False

	def __drop_cb(self, textview, context, x, y, time):
		editor.response()
		if "text/uri-list" in context.targets: return True
		editor.response()
		return False

	def __received_cb(self, textview, context, x, y, data, info, time):
		editor.response()
		if not ("text/uri-list" in context.targets): return False
		editor.response()
		if info != 80: return False
		editor.response()
		uri_list = list(data.get_uris())
		editor.response()
		self.__editor.open_files(uri_list, "utf-8")
		editor.response()
		context.finish(True, False, time)
		editor.response()
		return True

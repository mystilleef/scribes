class Inserter(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("processed-text", self.__processed_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __insert(self, text):
		self.__editor.busy()
		self.__editor.textview.window.freeze_updates()
		self.__editor.textbuffer.begin_user_action()
		self.__editor.response()
		self.__editor.textbuffer.set_text(text)
		self.__editor.response()
		self.__editor.textbuffer.end_user_action()
		self.__editor.busy(False)
		self.__manager.emit("inserted-text")
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __processed_cb(self, manager, text):
		self.__insert(text)
		return False

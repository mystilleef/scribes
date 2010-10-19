class Label(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("fileinfo", self.__fileinfo_cb)
		self.__label.set_text("")

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__label = manager.glade.get_widget("WordsLabel")
		from re import UNICODE, compile
		self.__pattern = compile(r"[^-\w]", UNICODE)
		return

	def __set_label(self, fileinfo):
		from re import split
		words = split(self.__pattern, self.__editor.text)
		is_word = lambda word: not (word in ("", " "))
		words = [word for word in words if is_word(word)]
		self.__label.set_text(str(len(words)))
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__label.destroy()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __fileinfo_cb(self, manager, fileinfo):
		self.__set_label(fileinfo)
		return

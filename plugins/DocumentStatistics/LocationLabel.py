class Label(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("fileinfo", self.__fileinfo_cb)
		self.__label.set_text("")

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__label = manager.glade.get_widget("LocationLabel")
		return

	def __set_label(self, fileinfo):
		try:
			if self.__editor.uri in ("", None): raise TypeError
			from gnomevfs import get_local_path_from_uri
			path = get_local_path_from_uri(str(self.__editor.uri))
			from os.path import dirname
			folder = dirname(path).replace(self.__editor.home_folder.rstrip("/"), "~")
			self.__label.set_text(folder)
		except TypeError:
			self.__label.set_text("Unknown")
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

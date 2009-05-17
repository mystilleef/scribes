class Creator(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("create-unsaved-file", self.__create_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __get_uri(self):
		folder = self.__editor.desktop_folder
		# A count to append to unsaved documents if many unsaved
		# documents exists in folder.
		count = 1
		from dircache import listdir
		file_list = listdir(folder)
		# Calculate count to append to unsaved documents.
		from gettext import gettext as _
		filename = _("Unsaved Document ")
		while True:
			self.__editor.response()
			newfile = filename + str(count)
			if not (newfile in file_list): break
			count += 1
		newfile = folder + "/" + newfile
		from gio import File
		return File(newfile).get_uri()

	def __create(self):
		uri = self.__get_uri()
		self.__editor.rename_file(uri, self.__editor.encoding)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __create_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__create, priority=9999)
		return False

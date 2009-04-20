class Creator(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		manager.connect("create-swap-file", self.__create_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__dictionary = {}
		self.__folder = self.__create_folder()
		return

	def __create(self, data):
		try:
			editor_id = data[0][0]
			swapfile = self.__get_file(editor_id)
			self.__dictionary[editor_id] = swapfile
			data = data + (swapfile,)
			self.__manager.emit("write-to-swap-file", data)
		except:
			from gettext import gettext as _
			message = _("Failed to create swap area")
			data = data + (message,)
			self.__manager.emit("oops", data)
		return False

	def __get_file(self, editor_id):
		if editor_id in self.__dictionary.keys(): return self.__dictionary[editor_id]
		return self.__create_file()

	def __create_file(self):
		from tempfile import NamedTemporaryFile
		swapfile = NamedTemporaryFile(mode="w+", suffix="Scribes", prefix="scribes", dir=self.__folder)
		from gnomevfs import get_uri_from_local_path
		swapfile = get_uri_from_local_path(swapfile.name)
		return swapfile

	def __create_folder(self):
		from tempfile import mkdtemp
		from SCRIBES.Globals import home_folder
		folder = mkdtemp(suffix="scribes", prefix=".Scribes", dir=home_folder)
		return folder

	def __create_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__create, data)
		return False

class Updater(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("get-uris", self.__get_uris_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return

	def __process(self):
		uris = self.__editor.uris
		if not uris: return False
		from gnomevfs import get_mime_type, URI, mime_get_description
		get_mime = lambda uri: mime_get_description(get_mime_type(uri)).split()[0].capitalize()
		get_filename = lambda uri: URI(uri).short_name
		get_path = lambda uri: URI(uri).path
#		get_data = lambda uri: get_mime(uri), get_filename(uri), get_path(uri), uri
		hfolder = self.__editor.home_folder
		format = lambda filename: filename.replace(hfolder, "~") if filename.startswith(hfolder) else filename
		def get_data(uri):
			self.__editor.response()
			return get_mime(uri), get_filename(uri), format(get_path(uri)), uri
		data = [get_data(uri) for uri in uris]
		self.__manager.emit("update", data)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __get_uris_cb(self, *args):
		self.__process()
		return False

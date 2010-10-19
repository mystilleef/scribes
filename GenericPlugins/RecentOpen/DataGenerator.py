from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager
from Utils import pretty_date

class Generator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(editor, manager)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "recent-infos", self.__info_cb)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __get_language(self, mimetype):
		from gio import content_type_get_description as get_desc
		return get_desc(mimetype).split()[0].lower()

	def __get_search_path_from(self, uri):
		from gio import File
		path = File(uri).get_parse_name()
		path = path.replace(self.__editor.home_folder, "").strip("/\\")
		return path

	def __get_display_path_from(self, uri):
		from gio import File
		path = File(uri).get_parent().get_parse_name()
		path = path.replace(self.__editor.home_folder, "").strip("/\\")
		from os.path import split
		if not path: return split(self.__editor.home_folder)[-1].strip("/\\")
		return path

	def __format(self, info):
		uri = info.get_uri()
		file_path = self.__get_search_path_from(uri)
		display_path = self.__get_display_path_from(uri)
		display_name = info.get_display_name()
		modified = pretty_date(info.get_modified())
		location = "" if info.is_local() else _("remote")
		filetype = self.__get_language(info.get_mime_type())
		icon = info.get_icon(32)
		return file_path, icon, display_name, display_path, modified, location, filetype, uri

	def __process(self, infos):
		data = [self.__format(info) for info in infos]
		self.__manager.emit("recent-infos-data", data)
		return False

	def __process_timeout(self, infos):
		from gobject import idle_add
		self.__timer = idle_add(self.__process, infos)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __info_cb(self, manager, infos):
		try:
			from gobject import timeout_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(250, self.__process_timeout, infos)
		return False

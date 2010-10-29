from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager
from Utils import pretty_date

class Generator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(editor, manager)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(editor.recent_manager, "changed", self.__changed_cb)
		from gobject import idle_add
		idle_add(self.__process)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		self.__infos = editor.recent_infos
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __get_language(self, mimetype):
		self.__editor.refresh()
		from gio import content_type_get_description as get_desc
		return get_desc(mimetype).split()[0].lower()

	def __get_search_path_from(self, uri):
		self.__editor.refresh()
		from gio import File
		path = File(uri).get_parse_name()
		self.__editor.refresh()
		path = path.replace(self.__editor.home_folder, "").strip("/\\")
		self.__editor.refresh()
		return path

	def __get_display_path_from(self, uri):
		self.__editor.refresh()
		from gio import File
		path = File(uri).get_parent().get_parse_name()
		self.__editor.refresh()
		path = path.replace(self.__editor.home_folder, "").strip("/\\")
		self.__editor.refresh()
		from os.path import split
		self.__editor.refresh()
		if not path: return split(self.__editor.home_folder)[-1].strip("/\\")
		self.__editor.refresh()
		return path

	def __format(self, info):
		self.__editor.refresh()
		uri = info.get_uri()
		self.__editor.refresh(False)
		file_path = self.__get_search_path_from(uri)
		self.__editor.refresh(False)
		display_path = self.__get_display_path_from(uri)
		self.__editor.refresh()
		display_name = info.get_display_name()
		self.__editor.refresh()
		modified = pretty_date(info.get_modified())
		self.__editor.refresh()
		location = "" if info.is_local() else _("remote")
		filetype = self.__get_language(info.get_mime_type())
		self.__editor.refresh()
		icon = info.get_icon(32)
		self.__editor.refresh()
		return file_path, icon, display_name, display_path, modified, location, filetype, uri

	def __process(self):
		self.__editor.refresh(False)
		data = [self.__format(info) for info in self.__editor.recent_infos]
		self.__editor.refresh(False)
		self.__manager.emit("recent-infos-data", data)
		self.__editor.refresh(False)
		return False

	def __process_timeout(self):
		from gobject import idle_add, PRIORITY_LOW
		self.__timer = idle_add(self.__process, priority=PRIORITY_LOW)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		try:
			from gobject import timeout_add, source_remove, PRIORITY_LOW
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(5000, self.__process_timeout, priority=PRIORITY_LOW)
		return False

from gettext import gettext as _

class Manager(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect_after("error", self.__error_cb)
		self.__sigid3 = manager.connect_after("encoding-error", self.__encoding_error_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__error_codes = {
			1: _("ERROR: You do not have permission to view %s"),
			2: _("ERROR: You do not have access to %s"),
			3: _("ERROR: Cannot find file information object for %s"),
			4: _("ERROR: %s does not exist"),
			5: _("ERROR: Failed to open %s for loading"),
			6: _("ERROR: Failed to read %s for loading"),
			7: _("ERROR: Failed to close %s for loading"),
		}
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return False

	def __show(self, uri, error_code):
		from gnomevfs import format_uri_for_display, URI
		title = _("File: %s") % (URI(uri).path)
		message = self.__error_codes[error_code] % URI(uri).short_name
		self.__editor.show_error(title, message)
		return False

	def __destroy_cb(self, *args):
		self.__destroy
		return False

	def __error_cb(self, manager, uri, error_code):
		self.__show(uri, error_code)
		return False

	def __encoding_error_cb(self, *args):
		self.__editor.show_load_encoding_error_window()
		return False

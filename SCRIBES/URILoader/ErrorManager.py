from gettext import gettext as _

class Manager(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect_after("error", self.__error_cb)
		self.__sigid3 = manager.connect_after("encoding-error", self.__encoding_error_cb)
		self.__sigid4 = manager.connect_after("unhandled-gio-error", self.__gio_error_cb)
		self.__sigid5 = manager.connect_after("NoFeedbackError", self.__no_feedback_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		del self
		return False

	def __show(self, data):
		uri, message = data
		self.__editor.emit("load-error", uri)
		from gio import File
		gfile = File(uri)
		title = _("File: %s") % gfile.get_parse_name()
		self.__editor.show_error(title, message)
		return False

	def __destroy_cb(self, *args):
		self.__destroy
		return False

	def __error_cb(self, manager, data):
		self.__show(data)
		return False

	def __encoding_error_cb(self, manager, uri, *args):
		print "Load encoding error."
		self.__editor.show_load_encoding_error_window(uri)
		return False

	def __gio_error_cb(self, manager, data):
		gfile, error = data
		self.__show((gfile.get_uri(), error.message))
		return False

	def __no_feedback_cb(self, manager, data):
		gfile, error = data
		self.__editor.emit("load-error", gfile.get_uri())
		self.__editor.busy(False)
		return False

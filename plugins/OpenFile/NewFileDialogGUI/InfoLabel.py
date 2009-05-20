from gettext import gettext as _
message = _("Create a new file in <b>%s</b> and open it.")

class Label(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("show-newfile-dialog-window", self.__new_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__label = manager.new_gui.get_widget("InfoLabel")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __set_label(self):
		from gio import File
		uri = self.__editor.uri
		if uri: folder = File(uri).get_parent().get_parse_name()
		if not uri: folder = self.__editor.desktop_folder
		folder = folder.replace(self.__editor.home_folder.rstrip("/"), "~")
		self.__label.set_label(message % folder)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __new_cb(self, *args):
		self.__set_label()
		return False

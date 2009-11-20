class Selector(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__select()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect_after("show", self.__show_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__chooser = manager.gui.get_object("FileChooser")
		return

	def __select(self):
		try:
			self.__editor.response()
			if not self.__editor.uri: raise ValueError
			from gio import File 
			gfile = File(self.__editor.uri)
			folder_uri = gfile.get_parent().get_uri()
			if folder_uri != self.__chooser.get_current_folder_uri():
				self.__chooser.set_current_folder_uri(folder_uri)
			fileinfo = gfile.query_info("standard::display-name")
			self.__chooser.set_current_name(fileinfo.get_display_name())
		except ValueError:
			self.__chooser.set_current_name(_("Unsaved Document"))
			self.__chooser.set_current_folder(self.__editor.desktop_folder)
		finally:
			self.__editor.response()
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __show_cb(self, *args):
		self.__select()
		return False

from gettext import gettext as _
message = _("Information about Scribes")

class Dialog(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__set_properties()

	def __init_attributes(self, editor):
		self.__editor = editor
		gui = editor.get_glade_object(globals(), "AboutDialog.glade", "AboutDialog")
		self.__dialog = gui.get_widget("AboutDialog")
		return

	def __destroy(self):
		self.__dialog.destroy()
		del self
		self = None
		return

	def __set_properties(self):
		# Set dialog properties.
		self.__dialog.set_artists(self.__editor.artists)
		self.__dialog.set_authors(self.__editor.author)
		self.__dialog.set_documenters(self.__editor.documenters)
		self.__dialog.set_transient_for(self.__editor.window)
		self.__dialog.set_property("copyright", self.__editor.copyrights)
		self.__dialog.set_property("license", self.__editor.license.strip())
		self.__dialog.set_property("translator-credits", self.__editor.translators)
		self.__dialog.set_property("version", self.__editor.version)
		self.__dialog.set_property("icon-name", "stock_about")
		return

	def show(self):
		self.__editor.busy()
		self.__editor.set_message(message)
		response = self.__dialog.run()
		if response: self.hide()
		return

	def hide(self):
		self.__editor.busy(False)
		self.__editor.unset_message(message)
		self.__dialog.hide()
		return

	def destroy(self):
		self.__destroy()
		return False

class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__trigger.connect("activate", self.__show_cb)
		self.__sigid2 = self.__editor.textview.connect("populate-popup", self.__popup_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__about_dialog = None
		self.__trigger = self.__create_trigger("show_about_dialog")
		return

	def __create_trigger(self, name, shortcut=None):
		# Trigger to show the about dialog.
		trigger = self.__editor.create_trigger("show_about_dialog")
		self.__editor.add_trigger(trigger)
		return trigger

	def destroy(self):
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__sigid1, self.__trigger)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor.textview)
		if self.__about_dialog: self.__about_dialog.destroy()
		del self
		self = None
		return

	def __show_cb(self, *args):
		try:
			self.__about_dialog.show()
		except AttributeError:
			from AboutDialog import Dialog
			self.__about_dialog = Dialog(self.__editor)
			self.__about_dialog.show()
		return

	def __popup_cb(self, *args):
		from PopupMenuItem import PopupMenuItem
		self.__editor.add_to_popup(PopupMenuItem(self.__editor))
		return False

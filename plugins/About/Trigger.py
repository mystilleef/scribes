from SCRIBES.SignalConnectionManager import SignalManager
from SCRIBES.TriggerManager import TriggerManager

class Trigger(SignalManager, TriggerManager):

	def __init__(self, editor):
		editor.response()
		SignalManager.__init__(self)
		TriggerManager.__init__(self, editor)
		self.__init_attributes(editor)
		self.connect(self.__trigger, "activate", self.__show_cb)
		self.connect(self.__editor.textview, "populate-popup", self.__popup_cb)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__about_dialog = None
		self.__trigger = self.create_trigger("show-about-dialog")
		return

	def destroy(self):
		self.disconnect()
		self.remove_triggers()
		if self.__about_dialog: self.__about_dialog.destroy()
		del self
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


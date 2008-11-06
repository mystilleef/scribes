class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sig_id1 = self.__trigger.connect("activate", self.__show_about_dialog_cb)
		self.__sig_id2 = editor.textview.connect_after("populate-popup", self.__popup_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__about_dialog = None
		self.__trigger = self.__create_trigger()
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		self.__signal_id_3 = None
		return

	def __create_trigger(self):
		# Trigger to show the about dialog.
		trigger = self.__editor.create_trigger("show_about_dialog")
		self.__editor.add_trigger(trigger)
		return trigger

	def destroy(self):
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__sig_id1, self.__trigger)
		self.__editor.disconnect_signal(self.__sig_id2, self.__editor.textview)
		if self.__about_dialog: self.__about_dialog.destroy_()
		del self
		self = None
		return

	def __show_about_dialog_cb(self, *args):
		try:
			self.__about_dialog.show_dialog()
		except AttributeError:
			from AboutDialog import Dialog
			self.__about_dialog = Dialog(self.__editor)
			self.__about_dialog.show_dialog()
		return

	def __popup_cb(self, textview, menu):
		from gtk import SeparatorMenuItem
		menu.append(SeparatorMenuItem())
		from PopupMenuItem import PopupMenuItem
		menu.append(PopupMenuItem(self.__editor))
		menu.show_all()
		return False

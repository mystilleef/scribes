from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class PrintTrigger(GObject):
	"""
	This class implements an object that creates a trigger to show the
	text editor's print dialog.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the object.

		@param self: Reference to the PrintTrigger instance.
		@type self: A PrintTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__create_trigger()
		self.__signal_id_1 = self.__trigger.connect("activate", self.__show_print_dialog_cb)
		self.__signal_id_2 = self.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the object's data attributes.

		@param self: Reference to the PrintTrigger instance.
		@type self: A PrintTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__print_dialog = None
		self.__trigger = None
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		return

	def __create_trigger(self):
		"""
		Creates a trigger to show the text editor's print dialog.

		@param self: Reference to the PrintTrigger instance.
		@type self: A PrintTrigger object.
		"""
		# Trigger to show the print dialog.
		self.__trigger = self.__editor.create_trigger("show_print_dialog", "<ctrl>p")
		self.__editor.add_trigger(self.__trigger)
		return

	def __show_print_dialog_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the PrintTrigger instance.
		@type self: A PrintTrigger object.

		@param trigger: A trigger to show the print dialog.
		@type trigger: A Trigger object.
		"""
		from Dialog import PrintDialog
		self.__print_dialog = PrintDialog(self.__editor)
		return

	def __destroy_cb(self, trigger):
		"""
		Handles callback when the destroy "signal" is emitted.

		@param self: Reference to the PrintDialogTrigger instance.
		@type self: An PrintDialogTrigger object.

		@param trigger: Reference to the PrintDialogTrigger instance.
		@type trigger: An PrintDialogTrigger object.
		"""
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		del self
		self = None
		return

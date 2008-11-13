from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class AutoReplaceGUITrigger(GObject):
	"""
	This class creates an object, a trigger, that allows users to show
	a automatic replacement dialog.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the trigger.

		@param self: Reference to the AutoReplaceGUITrigger instance.
		@type self: A AutoReplaceGUITrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__create_trigger()
		self.__signal_id_1 = self.__trigger.connect("activate", self.__show_autoreplace_dialog_cb)
		self.__signal_id_2 = self.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the trigger's attributes.

		@param self: Reference to the AutoReplaceGUITrigger instance.
		@type self: A AutoReplaceGUITrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__manager = None
		self.__trigger = None
		self.__signal_id_2 = None
		self.__signal_id_1 = None
		from MenuItem import AutoReplaceMenuItem
		self.__menuitem = AutoReplaceMenuItem(self, editor)
		return

	def __create_trigger(self):
		"""
		Create the trigger.

		@param self: Reference to the AutoReplaceGUITrigger instance.
		@type self: A AutoReplaceGUITrigger object.
		"""
		# Trigger to show the automatic replacement dialog.
		self.__trigger = self.__editor.create_trigger("show_autoreplace_dialog")
		self.__editor.add_trigger(self.__trigger)
		return

	def __show_autoreplace_dialog_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the AutoReplaceGUITrigger instance.
		@type self: A AutoReplaceGUITrigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.show()
		except AttributeError:
			from Manager import AutoReplaceGUIManager
			self.__manager = AutoReplaceGUIManager(self.__editor)
			self.__manager.show()
		return

	def __destroy_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the AutoReplaceGUITrigger instance.
		@type self: An AutoReplaceGUITrigger object.

		@param trigger: Reference to the AutoReplaceGUITrigger instance.
		@type trigger: A AutoReplaceGUITrigger object.
		"""
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		if self.__manager: self.__manager.emit("destroy")
		del self
		self = None
		return

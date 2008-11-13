from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class FullScreenTrigger(GObject):
	"""
	This class creates an object, a trigger, that allows users to toggle
	fullscreen mode.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the trigger.

		@param self: Reference to the FullScreenTrigger instance.
		@type self: A FullScreenTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__create_trigger()
		self.__signal_id_1 = self.__trigger.connect("activate", self.__toggle_fullscreen_cb)
		self.__signal_id_2 = self.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the trigger's attributes.

		@param self: Reference to the FullScreenTrigger instance.
		@type self: A FullScreenTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__trigger = None
		self.__signal_id_2 = None
		self.__signal_id_1 = None
		return

	def __create_trigger(self):
		"""
		Create the trigger.

		@param self: Reference to the FullScreenTrigger instance.
		@type self: A FullScreenTrigger object.
		"""
		# Trigger to toggle fullscreen mode.
		self.__trigger = self.__editor.create_trigger("toggle_fullscreen", "F11")
		self.__editor.add_trigger(self.__trigger)
		return

	def __toggle_fullscreen_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the FullScreenTrigger instance.
		@type self: A FullScreenTrigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		if self.__editor.window.is_fullscreen:
			self.__editor.emit("disable-fullscreen")
		else:
			self.__editor.emit("enable-fullscreen")
		return

	def __destroy_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the FullScreenTrigger instance.
		@type self: An FullScreenTrigger object.

		@param trigger: Reference to the FullScreenTrigger instance.
		@type trigger: A FullScreenTrigger object.
		"""
		self.__editor.triggermanager.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		del self
		self = None
		return

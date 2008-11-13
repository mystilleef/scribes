from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class CaseTrigger(GObject):
	"""
	This class implements triggers to perform case changing
	manipulations.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the trigger.

		@param self: Reference to the CaseTrigger instance.
		@type self: An CaseTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__create_triggers()
		self.__signal_id_1 = self.__uppercase_trigger.connect("activate", self.__uppercase_trigger_cb)
		self.__signal_id_2 = self.__lowercase_trigger.connect("activate", self.__lowercase_trigger_cb)
		self.__signal_id_3 = self.__titlecase_trigger.connect("activate", self.__titlecase_trigger_cb)
		self.__signal_id_4 = self.__swapcase_trigger.connect("activate", self.__swapcase_trigger_cb)
		self.__signal_id_5 = self.connect("destroy", self.__destroy_cb)
		self.__signal_id_6 = self.__editor.textview.connect_after("populate-popup", self.__popup_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the trigger's attributes.

		@param self: Reference to the CaseTrigger instance.
		@type self: A CaseTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__case_processor = None
		self.__uppercase_trigger = None
		self.__lowercase_trigger = None
		self.__titlecase_trigger = None
		self.__swapcase_trigger = None
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		self.__signal_id_3 = None
		self.__signal_id_4 = None
		self.__signal_id_5 = None
		self.__signal_id_6 = None
		return

	def __create_triggers(self):
		"""
		Create the trigger.

		@param self: Reference to the CaseTrigger instance.
		@type self: A CaseTrigger object.
		"""
		# Trigger to convert selected text to uppercase.
		self.__uppercase_trigger = self.__editor.create_trigger("uppercase", "alt+u")
		self.__editor.add_trigger(self.__uppercase_trigger)

		# Trigger to convert selected text to lowercase.
		self.__lowercase_trigger = self.__editor.create_trigger("lowercase")
		self.__editor.add_trigger(self.__lowercase_trigger)

		# Trigger to title the case of selected text.
		self.__titlecase_trigger = self.__editor.create_trigger("titlecase", "alt+shift+u")
		self.__editor.add_trigger(self.__titlecase_trigger)

		# Trigger to swap the case of selected text.
		self.__swapcase_trigger = self.__editor.create_trigger("swapcase", "alt+shift+L")
		self.__editor.add_trigger(self.__swapcase_trigger)
		return

	def __uppercase_trigger_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the CaseTrigger instance.
		@type self: A CaseTrigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		try:
			self.__case_processor.upper()
		except AttributeError:
			from case import CaseProcessor
			self.__case_processor = CaseProcessor(self.__editor)
			self.__case_processor.upper()
		return

	def __lowercase_trigger_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the CaseTrigger instance.
		@type self: A CaseTrigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		try:
			self.__case_processor.lower()
		except AttributeError:
			from case import CaseProcessor
			self.__case_processor = CaseProcessor(self.__editor)
			self.__case_processor.lower()
		return

	def __titlecase_trigger_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the CaseTrigger instance.
		@type self: A CaseTrigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		try:
			self.__case_processor.title()
		except AttributeError:
			from case import CaseProcessor
			self.__case_processor = CaseProcessor(self.__editor)
			self.__case_processor.title()
		return

	def __swapcase_trigger_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the CaseTrigger instance.
		@type self: A CaseTrigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		try:
			self.__case_processor.swapcase()
		except AttributeError:
			from case import CaseProcessor
			self.__case_processor = CaseProcessor(self.__editor)
			self.__case_processor.swapcase()
		return

	def __destroy_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the CaseTrigger instance.
		@type self: An CaseTrigger object.

		@param trigger: Reference to the FullScreenTrigger instance.
		@type trigger: A FullScreenTrigger object.
		"""
		remove_triggers = self.__editor.remove_triggers
		remove_triggers([self.__uppercase_trigger, self.__lowercase_trigger, self.__titlecase_trigger, self.__swapcase_trigger])
		self.__editor.disconnect_signal(self.__signal_id_1, self.__uppercase_trigger)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__lowercase_trigger)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__titlecase_trigger)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__swapcase_trigger)
		self.__editor.disconnect_signal(self.__signal_id_5, self)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__editor.textview)
		if self.__case_processor: self.__case_processor.emit("destroy")
		del self
		self = None
		return

	def __popup_cb(self, textview, menu):
		"""
		Handles callback when the "populate-popup" signal is emitted.

		@param self: Reference to the SelectionTrigger instance.
		@type self: An SelectionTrigger object.

		@param textview: Reference to the editor's textview.
		@type textview: A ScribesTextView object.

		@param menu: Reference to the editor's popup menu.
		@type menu: A gtk.Menu object.
		"""
		from PopupMenuItem import CasePopupMenuItem
		menu.prepend(CasePopupMenuItem(self.__editor))
		menu.show_all()
		return False

class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__create_triggers()
		self.__signal_id_1 = self.__up_trigger.connect("activate", self.__up_cb)
		self.__signal_id_2 = self.__down_trigger.connect("activate", self.__down_cb)
		self.__signal_id_3 = self.__middle_trigger.connect("activate", self.__middle_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__manager = None
		return

	def __create_triggers(self):
		# Trigger to scroll up.
		self.__up_trigger = self.__editor.create_trigger("scroll_up", "ctrl+Up")
		self.__editor.add_trigger(self.__up_trigger)

		# Trigger to scroll down.
		self.__down_trigger = self.__editor.create_trigger("scroll_down", "ctrl+Down")
		self.__editor.add_trigger(self.__down_trigger)

		# Trigger to center current line.
		self.__middle_trigger = self.__editor.create_trigger("center", "alt+m")
		self.__editor.add_trigger(self.__middle_trigger)
		return

	def __up_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.scroll_up()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.scroll_up()
		return

	def __down_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.scroll_down()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.scroll_down()
		return

	def __middle_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.center()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.center()
		return

	def __destroy(self):
		"""
		Destroy trigger.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__up_trigger)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__down_trigger)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__middle_trigger)
		self.__editor.remove_trigger(self.__up_trigger)
		self.__editor.remove_trigger(self.__down_trigger)
		self.__editor.remove_trigger(self.__middle_trigger)
		if self.__manager: self.__manager.destroy()
		del self
		self = None
		return

	def destroy(self):
		"""
		Destroy trigger.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.
		"""
		self.__destroy()
		return

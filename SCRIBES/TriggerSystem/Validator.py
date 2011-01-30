from SCRIBES.SignalConnectionManager import SignalManager

class Validator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "quit", self.__quit_cb)
		self.connect(editor, "add-trigger", self.__add_cb)
		self.connect(editor, "add-triggers", self.__adds_cb)
		self.connect(editor, "remove-trigger", self.__remove_cb)
		self.connect(editor, "remove-triggers", self.__removes_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__names = []
		self.__accelerators = []
		return

	def __validate(self, trigger):
		from Exceptions import NoTriggerNameError, DuplicateAcceleratorError
		from Exceptions import DuplicateTriggerNameError
		from Exceptions import InvalidAcceleratorError
		try:
			name, accelerator = trigger.name, trigger.accelerator
			self.__validate_name(name)
			self.__names.append(name)
			self.__validate_accelerator(accelerator)
			if accelerator: self.__accelerators.append(accelerator)
			self.__manager.emit("add", trigger)
		except NoTriggerNameError:
			print "ERROR: Trigger must have a name"
		except DuplicateTriggerNameError:
			print "ERROR: Duplicate trigger name found", name
		except DuplicateAcceleratorError:
			print "ERROR: Accelerator: %s, already in use" % accelerator
		except InvalidAcceleratorError:
			print "ERROR: %s is an invalid accelerator" % accelerator
		return False

	def __validate_name(self, name):
		from Exceptions import NoTriggerNameError, DuplicateTriggerNameError
		if not name: raise NoTriggerNameError
		if name in self.__names: raise DuplicateTriggerNameError
		return False

	def __validate_accelerator(self, accelerator):
		if not accelerator: return False
		from Exceptions import DuplicateAcceleratorError
		if accelerator in self.__accelerators: raise DuplicateAcceleratorError
		from gtk import accelerator_parse, accelerator_valid
		keyval, modifier = accelerator_parse(accelerator)
		if accelerator_valid(keyval, modifier): return False
		from Exceptions import InvalidAcceleratorError
		raise InvalidAcceleratorError

	def __remove(self, trigger):
		name, accelerator = trigger.name, trigger.accelerator
		if name in self.__names: self.__names.remove(name)
		if accelerator in self.__accelerators: self.__accelerators.remove(accelerator)
		return False

	def __validate_triggers(self, triggers):
		[self.__validate(trigger) for trigger in triggers]
		return False

	def __add_cb(self, editor, trigger):
		self.__validate_triggers((trigger,))
		return False

	def __adds_cb(self, editor, triggers):
		self.__validate_triggers(triggers)
		return False

	def __remove_cb(self, editor, trigger):
		self.__remove(trigger)
		return False

	def __removes_cb(self, editor, triggers):
		[self.__remove(trigger) for trigger in triggers]
		return False

	def __quit_cb(self, *args):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

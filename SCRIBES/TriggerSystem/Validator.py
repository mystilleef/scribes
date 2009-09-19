class Validator(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("add-trigger", self.__add_cb)
		self.__sigid3 = editor.connect("add-triggers", self.__adds_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__names = []
		self.__accelerators = []
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __validate(self, trigger):
		from Exceptions import NoTriggerNameError, DuplicateAcceleratorError
		from Exceptions import DuplicateTriggerNameError
		from Exceptions import InvalidAcceleratorError
		try:
			self.__editor.response()
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
		finally:
			self.__editor.response()
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
		return False

	def __validate_triggers(self, triggers):
		[self.__validate(trigger) for trigger in triggers]
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __add_cb(self, editor, trigger):
		from gobject import idle_add
		idle_add(self.__validate_triggers, (trigger,))
		return False

	def __adds_cb(self, editor, triggers):
		from gobject import idle_add
		idle_add(self.__validate_triggers, triggers)
		return False

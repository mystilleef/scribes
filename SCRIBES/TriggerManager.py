class TriggerManager(object):

	def __init__(self, editor):
		self.__init_attributes(editor)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__triggers = []
		return

	def create_trigger(self, command, shortcut):
		trigger = self.__editor.create_trigger(command, shortcut)
		self.__editor.add_trigger(trigger)
		self.__triggers.append(trigger)
		return trigger

	def remove_triggers(self):
		[self.__editor.remove_trigger(trigger) for trigger in self.__triggers]
		return False

class TriggerManager(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__triggers = []
		return

	def create_trigger(self, name, accelerator="", description="", category="", error=True, removable=True):
		self.__editor.response()
		trigger = self.__editor.create_trigger(name, accelerator, description, category, error, removable)
		self.__editor.add_trigger(trigger)
		self.__triggers.append(trigger)
		self.__editor.response()
		return trigger

	def remove_triggers(self):
		[self.__editor.remove_trigger(trigger) for trigger in self.__triggers]
		return False

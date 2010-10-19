from SCRIBES.SignalConnectionManager import SignalManager

class Handler(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(self.__tbox, "enter-notify-event", self.__notify_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__tbox = manager.get_data("TriggerWidget")
		return

	def __notify_cb(self, *args):
		self.__editor.show_full_view()
		return False

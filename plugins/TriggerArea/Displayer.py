from SCRIBES.SignalConnectionManager import SignalManager

class Displayer(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "toolbar-is-visible", self.__show_cb, True)
		self.connect(editor, "show-full-view", self.__hide_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__tbox = manager.get_data("TriggerWidget")
		return False

	def __show_cb(self, editor, visible):
		if visible is False: self.__tbox.show_all()
		return False

	def __hide_cb(self, *args):
		self.__tbox.hide()
		return False

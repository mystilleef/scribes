from SCRIBES.SignalConnectionManager import SignalManager

class Expander(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "execute", self.__execute_cb, True)
		self.connect(manager, "destroy", self.__destroy_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __expand(self, _string):
		options = {
			'textmate': False,
			'no-last-newline': True,
			'indent-spaces': self.__editor.textview.get_tab_width()
		}
		from sparkup import Router
		string = Router().start(options, _string, True)
		self.__manager.emit("sparkup-template", string)
		return False

	def __execute_cb(self, manager, string):
		from gobject import idle_add
		idle_add(self.__expand, string)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

from SCRIBES.SignalConnectionManager import SignalManager
from SCRIBES.TriggerManager import TriggerManager

class Trigger(SignalManager, TriggerManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		TriggerManager.__init__(self, editor)
		self.__init_attributes(editor)
		self.connect(self.__trigger, "activate", self.__activate_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__trigger = self.create_trigger("activate-foo-power", "<ctrl><alt>f")
		self.__manager = None
		return

	def __destroy(self):
		if self.__manager: self.__manager.destroy()
		self.disconnect()
		self.remove_triggers()
		del self
		self = None
		return False

	def __activate(self):
		try :
			self.__manager.activate()
		except AttributeError :
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.activate()
		finally:
			self.__editor.response()
		return False

	def __activate_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__activate)
		return

	def destroy(self):
		self.__destroy()
		return

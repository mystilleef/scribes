from SCRIBES.SignalConnectionManager import SignalManager

class Switcher(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "switch", self.__switch_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __switch(self):
		from Metadata import get_value
		uri = get_value()
		uris = [instance.uri for instance in self.__editor.instances]
		if self.__editor.uri: uris.remove(self.__editor.uri)
		if uri in uris:
			self.__editor.focus_file(uri)
		else:
			_id = self.__get_last_id()
			self.__editor.focus_by_id(_id)
		return False

	def __get_last_id(self):
		ids = [instance.id_ for instance in self.__editor.instances]
		ids.sort()
		if not self.__editor.id_: return ids[-1]
		ids.remove(self.__editor.id_)
		if not ids: return self.__editor.id_
		return ids[-1]

	def __switch_cb(self, *args):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__switch, priority=PRIORITY_LOW)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

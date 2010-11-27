from SCRIBES.SignalConnectionManager import SignalManager

class Switcher(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "next-window", self.__next_cb)
		self.connect(manager, "previous-window", self.__previous_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __switch(self, direction="forward"):
		try:
			ids = [object_.id_ for object_ in self.__editor.objects]
			ids.sort()
			index = ids.index(self.__editor.id_)
			rotation = 1 if direction == "forward" else -1
			id_ = ids[index+rotation]
			self.__editor.focus_by_id(id_)
		except IndexError:
			index = 0 if direction == "forward" else len(ids) -1
			self.__editor.focus_by_id(ids[index])
		return False

	def __next(self):
		self.__switch("forward")
		return

	def __previous(self):
		self.__switch("backward")
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __next_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__next)
		return False

	def __previous_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__previous)
		return False

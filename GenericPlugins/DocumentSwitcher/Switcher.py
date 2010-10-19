class Switcher(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("switch", self.__switch_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __switch(self):
		try:
			ids = [object_.id_ for object_ in self.__editor.objects]
			index = ids.index(self.__editor.id_)
			id_ = ids[index+1]
			self.__editor.focus_by_id(id_)
		except IndexError:
			self.__editor.focus_by_id(ids[0])
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __switch_cb(self, *args):
		self.__switch()
		return False

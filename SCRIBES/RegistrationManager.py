from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		self.connect(editor, "register-object", self.__register_cb)
		self.connect(editor, "unregister-object", self.__unregister_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		from collections import deque
		self.__objects = deque()
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.emit("post-quit")
		self.__editor.imanager.unregister_editor(self.__editor)
		self.__editor.window.destroy()
		del self
		return False

	def __register(self, _object):
		self.__objects.append(_object)
		return False

	def __unregister(self, _object):
		try:
			self.__objects.remove(_object)
		except ValueError:
			print _object, "not in queue"
		finally:
			if not self.__objects: self.__destroy()
		return False

	def __register_cb(self, editor, _object):
		self.__register(_object)
		return False

	def __unregister_cb(self, editor, _object):
		self.__unregister(_object)
		return False

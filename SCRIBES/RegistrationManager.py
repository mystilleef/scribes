from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		self.connect(editor, "register-object", self.__register_cb)
		self.connect(editor, "unregister-object", self.__unregister_cb)
		editor.response()

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
		self.__editor.response()
		self.__objects.append(_object)
		self.__editor.response()
		return False

	def __unregister(self, _object):
		try:
			self.__editor.response()
			self.__objects.remove(_object)
#			print "Unregistering: ", _object.__class__
		except ValueError:
			print _object, "not in queue"
		finally:
			self.__editor.response()
			if not self.__objects: self.__destroy()
#			print self.__objects
		return False

	def __register_cb(self, editor, _object):
		self.__register(_object)
		return False

	def __unregister_cb(self, editor, _object):
		self.__unregister(_object)
		return False

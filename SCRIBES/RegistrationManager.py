from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		self.connect(editor, "register-object", self.__register_cb)
		self.connect(editor, "unregister-object", self.__unregister_cb)
		self.connect(editor, "quit", self.__quit_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		from collections import deque
		self.__objects = deque()
		return

	def __destroy(self):
		self.__remove_timer()
		self.disconnect()
		self.__editor.emit("post-quit")
		self.__editor.imanager.unregister_editor(self.__editor)
		del self
		return False

	def __force_quit(self):
		try:
			# Don't force quit if file is not yet saved.
			if self.__editor.modified is False: return True
		except AttributeError:
			pass
		print "Forcing the editor to quit. Damn something is wrong!"
		self.__destroy()
		return False

	def __register(self, _object):
		self.__objects.append(_object)
		return False

	def __unregister(self, _object):
		try:
			self.__objects.remove(_object)
		except ValueError:
			pass
			# print _object, "not in queue"
		finally:
			if not self.__objects: self.__destroy()
		return False

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return False

	def __register_cb(self, editor, _object):
		from gobject import idle_add
		idle_add(self.__register, _object)
		return False

	def __unregister_cb(self, editor, _object):
		from gobject import idle_add
		idle_add(self.__unregister, _object)
		return False

	def __quit_cb(self, *args):
		# Give the editor 60 secs to quit properly. Otherwise force quit it.
		from gobject import timeout_add, PRIORITY_LOW
		self.__timer = timeout_add(60000, self.__force_quit, priority=PRIORITY_LOW)
		return False

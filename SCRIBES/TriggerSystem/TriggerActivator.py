class Activator(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("trigger", self.__activate_cb)
		self.__sigid3 = manager.connect("add", self.__add_cb)
		self.__sigid4 = manager.connect("remove", self.__remove_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		# Dictionary Format: {trigger_name: trigger}
		self.__dictionary = {}
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __add(self, trigger):
		self.__editor.response()
		self.__dictionary[trigger.name] = trigger
		self.__editor.response()
		return False

	def __remove(self, trigger):
		try:
			self.__editor.response()
			name = trigger.name
			trigger.destroy()
			del trigger
			del self.__dictionary[name]
		except KeyError:
			print "Error: Trigger named %s not found" % name
		finally:
			if not self.__dictionary: self.__manager.emit("triggers-cleared")
			self.__editor.response()
		return False

	def __activate(self, name):
		self.__editor.response()
		self.__dictionary[name].activate()
		self.__editor.response()
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __activate_cb(self, editor, name):
		from gobject import idle_add
		idle_add(self.__activate, name)
		return False

	def __add_cb(self, manager, trigger):
		from gobject import idle_add
		idle_add(self.__add, trigger)
		return False

	def __remove_cb(self, manager, trigger):
		from gobject import idle_add
		idle_add(self.__remove, trigger)
		return False

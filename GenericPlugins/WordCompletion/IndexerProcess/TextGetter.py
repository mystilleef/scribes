DBUS_SERVICE = "net.sourceforge.Scribes"
DBUS_PATH = "/net/sourceforge/Scribes"

class Getter(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		manager.connect("get-text", self.__get_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__process = self.__get_process()
		return

	def __get_process(self):
		from SCRIBES.Globals import dbus_iface, session_bus
		services = dbus_iface.ListNames()
		if not (DBUS_SERVICE in services): return None
		process = session_bus.get_object(DBUS_SERVICE, DBUS_PATH)
		return process

	def __get_text(self):
		self.__process.get_text(dbus_interface=DBUS_SERVICE,
											reply_handler=self.__reply_cb,
											error_handler=self.__error_cb)
		return False

	def __combine(self, texts):
		from string import whitespace
		texts = [text.strip(whitespace) for text in texts]
		text = " ".join(texts)
		self.__manager.emit("index", text.strip(whitespace))
		return False

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return

	def __get_cb(self, *args):
		self.__remove_timer()
		from gobject import idle_add, PRIORITY_LOW
		self.__timer = idle_add(self.__get_text, priority=PRIORITY_LOW)
		return False

	def __reply_cb(self, texts):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__combine, texts, priority=PRIORITY_LOW)
		return

	def __error_cb(self, *args):
		return False

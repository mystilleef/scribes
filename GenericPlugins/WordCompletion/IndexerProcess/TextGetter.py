DBUS_SERVICE = "net.sourceforge.Scribes"
DBUS_PATH = "/net/sourceforge/Scribes"

class Getter(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		manager.connect("index-request", self.__request_cb)
		manager.connect("clipboard-text", self.__clipboard_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__process = self.__get_process()
		self.__clipboard_text = ""
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
		clipboard_plus_texts = list(texts)
		clipboard_plus_texts.append(self.__clipboard_text)
		from string import whitespace
		strings = [text.strip(whitespace) for text in clipboard_plus_texts]
		text = " ".join(strings)
		self.__manager.emit("index", text.strip(whitespace))
		return False

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return

	def __request_cb(self, *args):
		self.__remove_timer()
		from gobject import idle_add, PRIORITY_LOW
		self.__timer = idle_add(self.__get_text, priority=PRIORITY_LOW)
		return False

	def __reply_cb(self, texts):
		from gobject import idle_add, PRIORITY_LOW
		self.__timer = idle_add(self.__combine, texts, priority=PRIORITY_LOW)
		return

	def __error_cb(self, *args):
		return False

	def __clipboard_cb(self, manager, text):
		self.__clipboard_text = "%s%s" % (self.__clipboard_text, text)
		return False

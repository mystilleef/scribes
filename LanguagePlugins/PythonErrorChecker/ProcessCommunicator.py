from ErrorCheckerProcess.Utils import DBUS_SERVICE, DBUS_PATH
from SCRIBES.SignalConnectionManager import SignalManager

class Communicator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "check", self.__check_cb)
		self.connect(manager, "error-check-type", self.__check_type_cb)
		self.__sigid1 = self.connect(editor.textbuffer, "changed", self.__changed_cb)
		editor.session_bus.add_signal_receiver(self.__name_change_cb,
						'NameOwnerChanged',
						'org.freedesktop.DBus',
						'org.freedesktop.DBus',
						'/org/freedesktop/DBus',
						arg0=DBUS_SERVICE)
		editor.session_bus.add_signal_receiver(self.__finished_cb,
						signal_name="finished",
						dbus_interface=DBUS_SERVICE)
		self.__block()
		self.__manager.emit("start-check")

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__checker = self.__get_checker()
		self.__session_id = 0
		self.__is_blocked = False
		self.__modtime = 0
		# 1 = syntax checking, 2 = syntax + pyflakes, 3 = syntax + pyflakes + pylint
		self.__check_type = 1
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.session_bus.remove_signal_receiver(self.__name_change_cb,
			'NameOwnerChanged',
			'org.freedesktop.DBus',
			'org.freedesktop.DBus',
			'/org/freedesktop/DBus',
			arg0=DBUS_SERVICE)
		self.__editor.session_bus.remove_signal_receiver(self.__finished_cb,
			signal_name="finished",
			dbus_interface=DBUS_SERVICE)
		del self
		return False

	def __get_checker(self):
		from SCRIBES.Globals import dbus_iface, session_bus
		services = dbus_iface.ListNames()
		if not (DBUS_SERVICE in services): return None
		checker = session_bus.get_object(DBUS_SERVICE, DBUS_PATH)
		return checker

	def __recheck(self):
		self.__checker = self.__get_checker()
		self.__manager.emit("start-check")
		return False

	def __check(self):
		try:
			from Utils import get_modification_time
			if self.__editor.window_is_active is False: return False
			file_content, file_path = self.__editor.text.decode("utf8"), self.__editor.filename.decode("utf8")
			self.__session_id += 1
			self.__modtime = get_modification_time(file_path)
			data = (
				file_content,
				file_path,
				self.__editor.id_,
				self.__session_id,
				self.__check_type,
				self.__modtime,
			)
			self.__checker.check(data, dbus_interface=DBUS_SERVICE,
				reply_handler=self.__reply_handler_cb,
				error_handler=self.__error_handler_cb)
		except AttributeError:
			from gobject import idle_add
			idle_add(self.__recheck)
		except Exception:
			print "ERROR: Cannot send message to python checker process"
		return False

	def __stop_analysis(self, session_id):
		try:
			data = (self.__editor.id_, self.__session_id)
			self.__checker.stop(data, dbus_interface=DBUS_SERVICE,
				reply_handler=self.__reply_handler_cb,
				error_handler=self.__error_handler_cb)
		except AttributeError:
			from gobject import idle_add
			idle_add(self.__recheck)
		except Exception:
			print "ERROR: Cannot send message to python checker process"
		return False

	def __block(self):
		if self.__is_blocked: return False
		self.__editor.textbuffer.handler_block(self.__sigid1)
		self.__is_blocked = True
		return False

	def __unblock(self):
		if self.__is_blocked is False: return False
		self.__editor.textbuffer.handler_unblock(self.__sigid1)
		self.__is_blocked = False
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __check_cb(self, *args):
		self.__unblock()
		from gobject import idle_add
		idle_add(self.__check)
		return False

	def __name_change_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__recheck)
		return False

	def __finished_cb(self, data):
		modification_time, session_id, editor_id = data[-1], data[-2], data[-3]
		if self.__editor.window_is_active is False: return False
		if editor_id != self.__editor.id_: return False
		if session_id != self.__session_id: return False
		if modification_time != self.__modtime: return False
		self.__manager.emit("error-data", data)
		return False

	def __reply_handler_cb(self, *args):
		return False

	def __error_handler_cb(self, *args):
		print "ERROR: Failed to communicate with scribes python checker process"
		return False

	def __check_type_cb(self, manager, more_error_checks):
		# 1 = syntax checking, 2 = syntax + pyflakes, 3 = syntax + pyflakes + pylint
		error_check_type = 3 if more_error_checks else 1
		self.__check_type = error_check_type
		return False

	def __changed_cb(self, *args):
		self.__block()
		self.__stop_analysis(self.__session_id)
		self.__session_id += 1
		return False

from dbus.service import Object, method, BusName, signal

from Utils import DBUS_SERVICE, DBUS_PATH

class DBusService(Object):

	def __init__(self, manager):
		from SCRIBES.Globals import session_bus
		from dbus.exceptions import NameExistsException
		try:
			bus_name = BusName(DBUS_SERVICE, bus=session_bus, do_not_queue=True)
			Object.__init__(self, bus_name, DBUS_PATH)
			self.__manager = manager
			manager.connect("finished", self.__finished_cb)
		except NameExistsException:
			manager.quit()

	@method(DBUS_SERVICE, in_signature="(ssxxid)")
	def check(self, data):
		# data is (file_content, file_path, editor_id, session_id, check_type, modification_time)
		return self.__manager.check(data)

	@method(DBUS_SERVICE, in_signature="(xx)")
	def stop(self, data):
		# data is (editor_id, session_id)
		return self.__manager.stop(data)

	@signal(DBUS_SERVICE, signature="(xsxxd)")
	def finished(self, data):
		# data is (line_number, error_message, editor_id, session_id, modification_time)
		return

	def __finished_cb(self, manager, data):
		self.finished(data)
		return False

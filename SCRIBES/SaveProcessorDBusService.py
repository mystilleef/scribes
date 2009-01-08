from dbus.service import Object, method, BusName, signal
dbus_service = "org.sourceforge.ScribesSaveProcessor"
dbus_path = "/org/sourceforge/ScribesSaveProcessor"

class DBusService(Object):

	def __init__(self, processor):
		from Globals import session_bus as session
		bus_name = BusName(dbus_service, bus=session)
		Object.__init__(self, bus_name, dbus_path)
		self.__processor = processor

	@method(dbus_service)
	def process(self, editor_id, text, uri, encoding):
		return self.__processor.save_file(editor_id, text, uri, encoding)

	@method(dbus_service)
	def update(self, editor_id):
		return self.__processor.update(editor_id)

	@signal(dbus_service)
	def is_ready(self):
		return

	@signal(dbus_service)
	def saved_file(self, editor_id, uri, encoding):
		return

	@signal(dbus_service)
	def error(self, editor_id, uri, encoding, error_message, error_id):
		return

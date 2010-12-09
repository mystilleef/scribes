from SCRIBES.SignalConnectionManager import SignalManager
from SCRIBES.Globals import SCRIBES_SAVE_PROCESS_DBUS_SERVICE

class Sender(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "session-id", self.__session_cb)
		self.connect(manager, "save-data", self.__data_cb)
		self.connect(manager, "save-processor-object", self.__processor_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__session_id = ()
		self.__processor = None
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __get_text(self):
		# Make sure file is always saved with a newline character.
		text = self.__editor.text
		if not text: return text + "\n"
		if text[-1] in ("\n", "\r", "\r\n"): return text
		return text + "\n"

	def __send(self, data):
		uri, encoding, session_id = data
		if self.__session_id != session_id: return False
#		from gio import File
#		 Make sure uri is properly escaped.
#		uri = File(uri).get_uri()
		if not encoding: encoding = "utf-8"
		data = session_id, uri, encoding, self.__get_text()
		self.__processor.process(data,
				dbus_interface=SCRIBES_SAVE_PROCESS_DBUS_SERVICE,
				reply_handler=self.__reply_handler_cb,
				error_handler=self.__error_handler_cb)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __session_cb(self, manager, session_id):
		self.__session_id = session_id
		return False

	def __data_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__send, data, priority=9999)
		return False

	def __processor_cb(self, manager, processor):
		self.__processor = processor
		return False

	def __reply_handler_cb(self, *args):
		return False

	def __error_handler_cb(self, error):
		print "======================================================="
		print "Module Name: SCRIBES/SaveSystem/DbusDataSender.py"
		print "Class Name: Sender"
		print "Method Name: __error_handler_cb"
		print "ERROR MESSAGE: ", error
		print "======================================================="
		return False

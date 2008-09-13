class Saver(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("private-save-file", self.__save_file_cb)
		self.__sigid3 = editor.connect("dbus-saved-file", self.__dbus_saved_file_cb)
		self.__sigid4 = editor.connect("dbus-save-error", self.__dbus_save_error_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__is_saving = False
		from collections import deque
		self.__queue = deque([])
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __save(self, uri, encoding):
		try:
			if self.__is_saving: raise AttributeError
			self.__is_saving = True
			from gobject import idle_add
			idle_add(self.__send_data_to_processor, uri, encoding, priority=9999)
		except AttributeError:
			print "Deffering save process"
			self.__queue.append(encoding)
		return False

	def __send_data_to_processor(self, uri, encoding):
		self.__editor.emit("send-data-to-processor", uri, encoding)
		return False

	def __check_queue(self, uri, encoding):
		try:
			encoding = self.__queue.pop()
			from gobject import idle_add
			idle_add(self.__save, uri, encoding, priority=9999)
		except IndexError:
			self.__is_saving = False
			self.__editor.emit("saved-file", uri, encoding)
		return False

################################################################################
#
#							Signal Listeners
#
################################################################################

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __save_file_cb(self, editor, uri, encoding):
		from gobject import idle_add
		idle_add(self.__save, uri, encoding, priority=9999)
		return False

	def __dbus_saved_file_cb(self, editor, uri, encoding):
		from gobject import idle_add
		idle_add(self.__check_queue, uri, encoding, priority=9999)
		return False

	def __dbus_save_error_cb(self, editor, uri, encoding, message):
		self.__editor.emit("save-error", uri, encoding, message)
		return False

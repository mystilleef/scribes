# Save file 7 seconds after modification.
SAVE_TIMER = 7000  # units in milliseconds (1000th of a second)

class Saver(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("close", self.__close_cb)
		self.__sigid2 = editor.connect("save-file", self.__save_file_cb)
		self.__sigid3 = editor.connect("modified-file", self.__modified_file_cb)
		self.__sigid4 = editor.connect("dbus-saved-file", self.__dbus_saved_file_cb)
		self.__sigid5 = editor.connect("dbus-save-error", self.__dbus_save_error_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__quit = False
		self.__is_saving = False
		from collections import deque
		self.__queue = deque([])
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.unregister_object(self)
		self.__editor.emit("quit")
		del self
		self = None
		return

	def __save(self, encoding):
		try:
			if self.__is_saving: raise AttributeError
			self.__is_saving = True
			from gobject import idle_add
			idle_add(self.__send_data_to_processor, encoding, priority=9999)
		except AttributeError:
			print "Deffering save process"
			self.__queue.append(encoding)
		return False

	def __send_data_to_processor(self, encoding):
		self.__editor.emit("send-data-to-processor", encoding)
		return False

	def __check_queue(self, uri, encoding):
		try:
			encoding = self.__queue.pop()
			self.__remove_timer()
			from gobject import idle_add
			self.__timer = idle_add(self.__save, encoding, priority=9999)
		except IndexError:
			self.__is_saving = False
			self.__remove_timer()
			self.__editor.emit("saved-file", uri, encoding)
			if self.__quit: self.__destroy()
		return False

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return False

################################################################################
#
#							Signal Listeners
#
################################################################################

	def __close_cb(self, editor, quit):
		self.__quit = True
		self.__save(editor.encoding) if editor.modified else self.__destroy()
		return False

	def __modified_file_cb(self, editor, modified):
		if editor.uri is None or modified is False: return False
		self.__remove_timer()
		from gobject import timeout_add
		self.__timer = timeout_add(SAVE_TIMER, self.__save, editor.encoding, priority=9999)
		return False

	def __save_file_cb(self, editor, encoding):
		self.__remove_timer()
		from gobject import idle_add
		self.__timer = idle_add(self.__save, encoding, priority=9999)
		return False

	def __dbus_saved_file_cb(self, editor, uri, encoding):
		from gobject import idle_add
		idle_add(self.__check_queue, uri, encoding, priority=9999)
		return False

	def __dbus_save_error_cb(self, *args):
		self.__editor.emit("save-error")
		return False

from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, editor, uri):
		SignalManager.__init__(self)
		self.__init_attributes(editor, uri)
		self.connect(editor, "close", self.__close_cb)
		self.__sigid2 = self.connect(self.__window, "focus-out-event", self.__update_cb)
		self.__sigid3 = self.connect(self.__window, "focus-in-event", self.__update_cb)
		self.connect(editor, "checking-file", self.__checking_cb)
		self.connect(editor, "load-error", self.__error_cb)
		self.connect(editor, "saved-file", self.__saved_cb)
		self.connect(editor, "loaded-file", self.__loaded_cb, True)
		editor.register_object(self)

	def __init_attributes(self, editor, uri):
		self.__editor = editor
		self.__uri = uri
		self.__window = editor.window
		self.__blocked = False
		return False

	def __destroy(self):
		self.disconnect()
		self.__set_position_in_database()
		self.__window.hide()
		self.__editor.unregister_object(self)
		del self
		return False

	def __block_signals(self):
		if self.__blocked: return False
		self.__window.handler_block(self.__sigid2)
		self.__window.handler_block(self.__sigid3)
		self.__blocked = True
		return False

	def __unblock_signals(self):
		if self.__blocked is False: return False
		self.__window.handler_unblock(self.__sigid2)
		self.__window.handler_unblock(self.__sigid3)
		self.__blocked = False
		return False

	def __set_position_in_database(self):
		xcoordinate, ycoordinate = self.__window.get_position()
		width, height = self.__window.get_size()
		is_maximized = self.__editor.maximized
		uri = self.__uri if self.__uri else "<EMPTY>"
		maximized_position = (True, None, None, None, None)
		unmaximized_position = (False, width, height, xcoordinate, ycoordinate)
		window_position = maximized_position if is_maximized else unmaximized_position
		from SCRIBES.PositionMetadata import update_window_position_in_database
		update_window_position_in_database(str(uri), window_position)
		return False

	def __close_cb(self, *args):
		self.__destroy()
		return False

	def __update_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__set_position_in_database, priority=9999)
		return False

	def __checking_cb(self, editor, uri):
		self.__block_signals()
		self.__uri = uri
		return False

	def __error_cb(self, *args):
		self.__unblock_signals()
		self.__uri = None
		return False

	def __loaded_cb(self, *args):
		self.__unblock_signals()
		return False

	def __saved_cb(self, editor, uri, *args):
		self.__uri = uri
		return False

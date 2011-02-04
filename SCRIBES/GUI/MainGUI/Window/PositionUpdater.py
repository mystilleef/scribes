from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, editor, uri):
		SignalManager.__init__(self)
		self.__init_attributes(editor, uri)
		self.connect(editor, "close", self.__close_cb)
		editor.register_object(self)

	def __init_attributes(self, editor, uri):
		self.__editor = editor
		self.__window = editor.window
		return False

	def __destroy(self):
		self.disconnect()
		self.__set_position_in_database()
		# self.__editor.refresh(False)
		self.__window.hide()
		# self.__editor.refresh(False)
		self.__editor.unregister_object(self)
		del self
		return False

	def __set_position_in_database(self):
		xcoordinate, ycoordinate = self.__window.get_position()
		width, height = self.__window.get_size()
		is_maximized = self.__editor.maximized
		uri = self.__editor.uri if self.__editor.uri else "<EMPTY>"
		maximized_position = (True, None, None, None, None)
		unmaximized_position = (False, width, height, xcoordinate, ycoordinate)
		window_position = maximized_position if is_maximized else unmaximized_position
		from SCRIBES.PositionMetadata import update_window_position_in_database
		update_window_position_in_database(str(uri), window_position)
		return False

	def __close_cb(self, *args):
		self.__destroy()
		return False

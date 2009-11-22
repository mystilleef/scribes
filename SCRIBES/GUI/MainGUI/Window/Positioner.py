class Positioner(object):

	def __init__(self, editor, uri):
		editor.response()
		self.__init_attributes(editor, uri)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect_after("checking-file", self.__checking_cb)
		self.__sigid3 = editor.connect("load-error", self.__error_cb)
		editor.register_object(self)
		self.__position(uri)
		editor.response()

	def __init_attributes(self, editor, uri):
		self.__editor = editor
		self.__window = editor.window
		self.__positioned = False
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __position(self, uri):
		try:
			self.__editor.response()
			self.__window.hide()
			self.__editor.response()
			uri = uri if uri else "<EMPTY>"
			if uri != "<EMPTY>": self.__positioned = True
			# Get window position from the position database, if possible.
			from SCRIBES.PositionMetadata import get_window_position_from_database as gp
			maximize, width, height, xcoordinate, ycoordinate = gp(uri)
			if maximize:
				self.__editor.response()
				self.__window.maximize()
				self.__editor.response()
			else:
				self.__editor.response()
				self.__window.resize(width, height)
				self.__editor.response()
				self.__window.move(xcoordinate, ycoordinate)
				self.__editor.response()
		except TypeError:
			self.__editor.response()
		finally:
			self.__window.present()
			self.__editor.response()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __checking_cb(self, editor, uri):
		if not self.__positioned: self.__position(uri)
		return False

	def __error_cb(self, *args):
		self.__position(None)
		return False

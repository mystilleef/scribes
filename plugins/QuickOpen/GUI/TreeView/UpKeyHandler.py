class Handler(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("up-key-press", self.__press_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = manager.gui.get_object("TreeView")
		self.__selection = self.__view.get_selection()
		self.__column = self.__view.get_column(0)
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __up(self):
		try:
			model, paths = self.__selection.get_selected_rows()
			if not paths: raise ValueError
			row = paths[0][0]
			if not row: raise ValueError
			previous_row = row - 1
			self.__selection.select_path(previous_row)
			self.__view.set_cursor(previous_row, self.__column)
			self.__view.scroll_to_cell(previous_row, None, True, 0.5, 0.5)
		except ValueError:
			self.__manager.emit("focus-entry")
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __press_cb(self, *args):
		self.__up()
		return False

from SCRIBES.SignalConnectionManager import SignalManager

class Grabber(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "hiding-browser", self.__ungrab_cb)
		self.connect(manager, "showing-browser", self.__grab_cb)
		self.connect(manager, "updated-model", self.__updated_cb, True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__treeview = manager.gui.get_object("TreeView")
		self.__first_time = True
		self.__is_visible = False
		return

	def __focus_first(self):
		from ...Exceptions import EmptyModelError
		try:
			model = self.__treeview.get_model()
			if not len(model): raise EmptyModelError
			path = model[0].path
			self.__treeview.set_cursor(path)
		except EmptyModelError:
			pass
		finally:
			if self.__is_visible: self.__treeview.grab_focus()
		return False

	def __focus_filename(self):
		from ...Exceptions import EmptyModelError
		try:
			self.__first_time = False
			if not self.__editor.uri: return False
			model = self.__treeview.get_model()
			if not len(model): return False
			for row in model:
				if row[-1] == "folder": continue
				if row[-2] != self.__editor.uri: continue
				self.__treeview.set_cursor(row.path)
				break
		except EmptyModelError:
			pass
		finally:
			self.__treeview.grab_focus()
		return False

	def __grab(self):
		self.__is_visible = True
		self.__treeview.grab_focus()
		return False

	def __ungrab(self):
		self.__is_visible = False
		self.__editor.textview.grab_focus()
		return False

	def __ungrab_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__ungrab)
		return False

	def __grab_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__grab)
		return False

	def __updated_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__focus_filename) if self.__first_time else idle_add(self.__focus_first)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

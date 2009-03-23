class Manager(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		editor.set_data("bar_is_active", False)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("add-bar-object", self.__add_cb)
		self.__sigid3 = editor.connect("remove-bar-object", self.__remove_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __add(self, bar):
		container = self.__editor.gui.get_widget("BarBox")
		from Exceptions import BarBoxAddError
		if container.get_children(): raise BarBoxAddError
		self.__editor.response()
		container.add(bar) if bar.parent is None else bar.reparent(container)
		container.show_all()
		self.__editor.response()
		self.__editor.set_data("bar_is_active", True)
		self.__editor.emit("bar-is-active", True)
		return False

	def __remove(self, bar):
		container = self.__editor.gui.get_widget("BarBox")
		from Exceptions import BarBoxInvalidObjectError
		if not (bar in container.get_children()): raise BarBoxInvalidObjectError
		self.__editor.response()
		container.hide()
		container.remove(bar)
		self.__editor.response()
		self.__editor.set_data("bar_is_active", False)
		self.__editor.emit("bar-is-active", False)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __add_cb(self, editor, bar):
		self.__add(bar)
		return False

	def __remove_cb(self, editor, bar):
		self.__remove(bar)
		return False

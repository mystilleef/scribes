from gettext import gettext as _

class UndoRedo(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("checking-file", self.__checking_cb)
		self.__sigid3 = editor.connect("loaded-file", self.__loaded_cb)
		self.__sigid4 = editor.connect("load-error", self.__error_cb)
		self.__sigid5 = editor.connect("undo", self.__undo_cb)
		self.__sigid6 = editor.connect("redo", self.__redo_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.disconnect_signal(self.__sigid6, self.__editor)
		self.__editor.unregister_object(self)
		del self
		return False

	def __undo(self):
		try:
			self.__editor.freeze()
			if not self.__buffer.can_undo(): raise ValueError
			self.__buffer.undo()
			self.__editor.move_view_to_cursor()
			message = _("Undo last action")
			self.__editor.update_message(message, "pass")
		except ValueError:
			message = _("Cannot undo last action")
			self.__editor.update_message(message, "fail")
		finally:
			self.__editor.thaw()
		return False

	def __redo(self):
		try:
			self.__editor.freeze()
			if not self.__buffer.can_redo(): raise ValueError
			self.__buffer.redo()
			self.__editor.move_view_to_cursor()
			message = _("Redo previous action")
			self.__editor.update_message(message, "pass")
		except ValueError:
			message = _("Cannot redo previous action")
			self.__editor.update_message(message, "fail")
		finally:
			self.__editor.thaw()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __checking_cb(self, *args):
		self.__buffer.begin_not_undoable_action()
		return False

	def __loaded_cb(self, *args):
		self.__buffer.end_not_undoable_action()
		return False

	def __error_cb(self, *args):
		self.__buffer.end_not_undoable_action()
		return False

	def __undo_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__undo)
		return False

	def __redo_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__redo)
		return False

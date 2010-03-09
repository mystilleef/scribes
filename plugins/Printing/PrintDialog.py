# Module needs refactoring.

from SCRIBES.SignalConnectionManager import SignalManager

class Dialog(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.connect(self.__operation, "begin-print", self.__begin_cb)
		self.connect(self.__operation, "draw-page", self.__draw_page_cb)
		self.connect(self.__operation, "done", self.__done_cb)
		self.connect(self.__operation, "paginate", self.__paginate_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from gtk import PrintOperation
		self.__operation = PrintOperation()
		return

	def __destroy(self):
		self.__manager.emit("print-dialog-is-visible", False)
		self.disconnect()
		del self
		return False

	def __set_properties(self):
		self.__operation.set_allow_async(True)
		self.__operation.set_show_progress(True)
		return False

	def show(self):
		self.__manager.emit("print-dialog-is-visible", True)
		from gtksourceview2 import print_compositor_new_from_view
		self.__compositor = print_compositor_new_from_view(self.__editor.textview)
		from gtk import PRINT_OPERATION_ACTION_PRINT_DIALOG
		self.__operation.run(PRINT_OPERATION_ACTION_PRINT_DIALOG, self.__editor.window)
		return False

	def __begin_cb(self, operation, context):
		return False

	def __draw_page_cb(self, operation, context, page_nr):
		self.__compositor.draw_page(context, page_nr)
		return False

	def __paginate_cb(self, operation, context):
		if not self.__compositor.paginate(context): return False
		n_pages = self.__compositor.get_n_pages()
		operation.set_n_pages(n_pages)
		return True

	def __done_cb(self, operation, result):
		from gtk import PRINT_OPERATION_RESULT_ERROR
		from gtk import PRINT_OPERATION_RESULT_APPLY
		from gtk import PRINT_OPERATION_RESULT_CANCEL
		from gtk import PRINT_OPERATION_RESULT_IN_PROGRESS
		if result is PRINT_OPERATION_RESULT_ERROR: self.__result_error()
		if result is PRINT_OPERATION_RESULT_APPLY: self.__result_apply()
		if result is PRINT_OPERATION_RESULT_CANCEL: self.__result_cancel()
		if result is PRINT_OPERATION_RESULT_IN_PROGRESS: self.__result_progress()
		return False

	def __result_error(self):
		print self.__operation.get_error()
		return False

	def __result_apply(self):
		self.__destroy()
		return False

	def __result_cancel(self):
		self.__destroy()
		return False

	def __result_progress(self):
		return False

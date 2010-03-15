from gtk import PRINT_OPERATION_RESULT_ERROR
from gtk import PRINT_OPERATION_RESULT_APPLY
from gtk import PRINT_OPERATION_RESULT_CANCEL
from SCRIBES.SignalConnectionManager import SignalManager

class Printer(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.connect(self.__operation, "draw-page", self.__draw_page_cb)
		self.connect(self.__operation, "done", self.__done_cb)
		self.connect(self.__operation, "paginate", self.__paginate_cb)
		self.connect(self.__operation, "status-changed", self.__status_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from Utils import get_compositor
		self.__compositor = get_compositor(editor)
		from gtk import PrintOperation
		self.__operation = PrintOperation()
		self.__print_settings = self.__print_settings_from_file()
		self.__result_handler = {
			PRINT_OPERATION_RESULT_ERROR: self.__error,
			PRINT_OPERATION_RESULT_APPLY: self.__apply,
			PRINT_OPERATION_RESULT_CANCEL: self.__cancel,
		}
		return

	def __destroy(self):
		#self.disconnect()
		#del self
		return False

	def __set_properties(self):
		from Utils import default_page_setup
		self.__operation.set_default_page_setup(default_page_setup())
		self.__operation.set_allow_async(True)
		self.__operation.set_use_full_page(False)
		if not self.__print_settings: return False
		self.__operation.set_print_settings(self.__print_settings)
		return False

	def show(self):
		if self.__print_settings: self.__print_settings.load_file(self.__editor.print_settings_filename)
		from gtk import PRINT_OPERATION_ACTION_PRINT_DIALOG
		self.__operation.run(PRINT_OPERATION_ACTION_PRINT_DIALOG, self.__editor.window)
		return False

	def __print_settings_to_file(self):
		try:
			self.__print_settings = self.__operation.get_print_settings()
			from os.path import exists
			if not exists(self.__editor.print_settings_filename): raise AssertionError
		except AssertionError:
			from gio import File
			File(self.__editor.print_settings_filename).replace_contents("")
		finally:
			self.__print_settings.to_file(self.__editor.print_settings_filename)
		return False

	def __print_settings_from_file(self):
		from os.path import exists
		if not exists(self.__editor.print_settings_filename): return None
		from gtk import PrintSettings
		settings = PrintSettings()
		if settings.load_file(self.__editor.print_settings_filename): return settings
		return None

	def __error(self):
		error_message = self.__operation.get_error()
		return False

	def __apply(self):
		self.__print_settings_to_file()
		return False

	def __cancel(self):
		self.__manager.emit("cancel")
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
		self.__result_handler[result]()
		self.__destroy()
		return False

	def __status_cb(self, operation, *args):
		self.__manager.emit("feedback", operation.get_status())
		return False

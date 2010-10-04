from gettext  import gettext as _

class Manager(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__view = editor.textview
		return

	def __precompile_methods(self):
		methods = (self.scroll_up, self.scroll_down, self.center)
		self.__editor.optimize(methods)
		return False

	def scroll_up(self):
		rectangle = self.__view.get_visible_rect()
		x, y, width, height = rectangle.x, rectangle.y, rectangle.width, rectangle.height
		iterator = self.__view.get_iter_at_location(x, y)
		iterator.backward_line()
		self.__editor.response()
		self.__view.scroll_to_iter(iterator, 0.001)
		self.__editor.response()
		return

	def scroll_down(self):
		rectangle = self.__view.get_visible_rect()
		x, y, width, height = rectangle.x, rectangle.y, rectangle.width, rectangle.height
		iterator = self.__view.get_iter_at_location(x, y+height)
		iterator.forward_line()
		self.__editor.response()
		self.__view.scroll_to_iter(iterator, 0.001)
		self.__editor.response()
		return

	def center(self):
		iterator = self.__editor.cursor
		self.__editor.response()
		self.__view.scroll_to_iter(iterator, 0.001, use_align=True, xalign=1.0)
		self.__editor.response()
		message = _("Centered current line")
		self.__editor.update_message(message, "pass")
		return

	def destroy(self):
		del self
		self = None
		return

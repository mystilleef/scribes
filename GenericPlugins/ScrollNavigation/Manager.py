from gettext  import gettext as _

INCREMENT = 5

class Manager(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__compile, priority=PRIORITY_LOW)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__view = editor.textview
		self.__hadjustment = editor.gui.get_widget("ScrolledWindow").get_hadjustment()
		self.__upper = 0
		return

	def __compile(self):
		methods = (self.scroll_right, self.scroll_left, self.center)
		self.__editor.optimize(methods)
		return False

	def scroll_right(self):
		self.__editor.refresh(False)
		from gtk import WRAP_NONE
		if self.__editor.textview.get_wrap_mode() != WRAP_NONE: return False
		new_value = self.__hadjustment.value + INCREMENT
		if new_value == self.__upper: return False
		self.__upper = new_value
		self.__hadjustment.set_value(new_value)
		self.__hadjustment.value_changed()
		self.__editor.refresh(False)
		return

	def scroll_left(self):
		self.__editor.refresh(False)
		from gtk import WRAP_NONE
		if self.__editor.textview.get_wrap_mode() != WRAP_NONE: return False
		new_value = self.__hadjustment.get_value() - INCREMENT
		if new_value < 0: new_value = 0
		self.__hadjustment.set_value(new_value)
		self.__hadjustment.value_changed()
		self.__editor.refresh(False)
		return

	def center(self):
		self.__editor.refresh(False)
		iterator = self.__editor.cursor
		self.__view.scroll_to_iter(iterator, 0.001, use_align=True, xalign=1.0)
		self.__editor.refresh(False)
		message = _("Centered current line")
		self.__editor.update_message(message, "pass")
		return

	def destroy(self):
		del self
		return

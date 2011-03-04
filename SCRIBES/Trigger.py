from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE
from gobject import SIGNAL_ACTION, SIGNAL_NO_RECURSE
SSIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Trigger(GObject):

	__gsignals__ = {
		"activate": (SSIGNAL, TYPE_NONE, ())
	}

	def __init__(self, editor, name, accelerator="", description="", category="", error=True, removable=True):
		GObject.__init__(self)
		self.__init_attributes(editor, name, accelerator, description, category, error, removable)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__compile, priority=PRIORITY_LOW)

	def __init_attributes(self, editor, name, accelerator, description, category, error, removable):
		self.__editor = editor
		self.__name = name
		self.__accelerator = accelerator
		self.__description = description
		self.__error = error
		self.__removable = removable
		self.__category = category
		return

	name = property(lambda self: self.__name)
	accelerator = property(lambda self: self.__accelerator)
	description = property(lambda self: self.__description)
	category = property(lambda self: self.__category)
	error = property(lambda self: self.__error)
	removable = property(lambda self: self.__removable)

	def __activate(self):
		self.__editor.grab_focus()
		if self.__editor.bar_is_active: return False
		self.__editor.hide_completion_window()
		from gobject import idle_add, PRIORITY_HIGH
		idle_add(self.emit, "activate", priority=PRIORITY_HIGH)
		return False

	def activate(self):
		from gobject import idle_add, PRIORITY_HIGH
		idle_add(self.__activate, priority=PRIORITY_HIGH)
		return False

	def destroy(self):
		del self
		return False

	def __compile(self):
		methods = (self.activate, self.__activate)
		self.__editor.optimize(methods)
		return False

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE
from gobject import SIGNAL_ACTION, SIGNAL_NO_RECURSE
SSIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Trigger(GObject):

	__gsignals__ = {
		"activate": (SSIGNAL, TYPE_NONE, ())
	}

	def __init__(self, editor, name, accelerator="", description="", error=True, removable=True):
		GObject.__init__(self)
		self.__init_attributes(editor, name, accelerator, description, error, removable)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, editor, name, accelerator, description, error, removable):
		self.__editor = editor
		self.__name = name
		self.__accelerator = accelerator
		self.__description = description
		self.__error = error
		self.__removable = removable
		return

########################################################################
#
#					Getters For Public Porperties
#
########################################################################

	def __get_name(self):
		return self.__name

	def __get_accelerator(self):
		if not (self.__accelerator): return None
		return self.__accelerator

	def __get_description(self):
		if not (self.__description): return None
		return self.__description

	def __get_error(self):
		return self.__error

	def __get_removable(self):
		return self.__removable

########################################################################
#
#							Public API
#
########################################################################

	name = property(__get_name)
	accelerator = property(__get_accelerator)
	description = property(__get_description)
	error = property(__get_error)
	removable = property(__get_removable)

	def __activate(self):
		if self.__editor.bar_is_active: return False
		self.__editor.refresh(False)
		self.emit("activate")
		self.__editor.refresh(False)
		return False

	def activate(self):
		from gobject import idle_add
		idle_add(self.__activate)
		return

	def destroy(self):
		del self.__name, self.__description, self.__accelerator, self
		self = None
		return

	def __precompile_methods(self):
		methods = (self.activate, self.__get_name, self.__get_accelerator)
		self.__editor.optimize(methods)
		return False

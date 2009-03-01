from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class Trigger(GObject):

	__gsignals__ = {
		"activate": (SIGNAL_RUN_LAST, TYPE_NONE, ())
	}

	def __init__(self, editor, name, accelerator=None, description=None, error=True, removable=True):
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
		self.emit("activate")
		self.__editor.refresh(False)
		return False

	def activate(self):
		self.__editor.refresh(False)
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

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_PYOBJECT

class Editor(GObject):

	__gsignals__ = {
		# Nobody should listen to this signal. For internal use only.
		"close": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		# QUIT signal to all core objects. This signal is emitted only after
		# a file has been properly saved. For internal use only. PlEASE NEVER
		# EMIT THIS SIGNAL. This is the signal to listen to for proper cleanup
		# before exit.
		"quit": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, manager, file_uri=None, encoding=None):
		GObject.__init__(self)
		self.__init_attributes(manager)
		from Window import Window
		Window(self)
		# Register with instance manager after a successful editor
		# initialization.
		self.__imanager.register_editor(self)

	def __init_attributes(self, manager):
		# Reference to instance manager.
		self.__imanager = manager
		from collections import deque
		# Key objects register with this object so that the editor does not
		# terminate before proper object cleanup.
		self.__registered_objects = deque([])
		from os.path import join
		glade_file = join(self.scribes_data_folder, "Editor.glade")
		from gtk.glade import XML
		self.__glade = XML(glade_file, "Window", "scribes")
		return False

	def __destroy(self):
		self.__glade.get_widget("Window").destroy()
		self.__imanager.unregister_editor(self)
		del self
		self = None
		from gc import collect
		from thread import start_new_thread
		start_new_thread(collect, ())
		return False

	def __get_gui(self):
		return self.__glade

	def __get_scribes_data_folder(self):
		from Globals import scribes_data_folder
		return scribes_data_folder

	gui = property(__get_gui)
	scribes_data_folder = property(__get_scribes_data_folder)

	def close(self, save_first=True):
		self.emit("close", save_first)
		return False

	def register_object(self, instance):
		self.__registered_objects.append(instance)
		return False

	def unregister_object(self, instance):
		self.__registered_objects.remove(instance)
		if not self.__registered_objects: self.__destroy()
		return False

	def calculate_resolution_independence(self, window, width, height):
		from Utils import calculate_resolution_independence
		return calculate_resolution_independence(window, width, height)

	def disconnect_signal(self, sigid, instance):
		from Utils import disconnect_signal
		return disconnect_signal(sigid, instance)

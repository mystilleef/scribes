class Handler(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__add_signals()
		self.__add_bindings()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__view.connect("enter-press", self.__enter_cb)
		self.__sigid3 = self.__view.connect("up-press", self.__up_cb)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__view = manager.gui.get_object("TreeView")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__view)
		self.__editor.disconnect_signal(self.__sigid3, self.__view)
		del self
		self = None
		return False

	def __add_signals(self):
		# Add new signal to window. 
		from gobject import signal_new, signal_query, SIGNAL_RUN_LAST
		from gobject import TYPE_PYOBJECT, SIGNAL_ACTION, TYPE_NONE
		from gobject import SIGNAL_NO_RECURSE, type_register
		from gobject import TYPE_BOOLEAN, type_register, TYPE_STRING
		SIGNAL = SIGNAL_ACTION|SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE
		from gtk import Window
		view = self.__view
		if signal_query("enter-press", view): return False
		signal_new("enter-press", view, SIGNAL, TYPE_BOOLEAN, (TYPE_STRING,))
		signal_new("up-press", view, SIGNAL, TYPE_BOOLEAN, (TYPE_STRING,))
#		type_register(type(self.__window))
		return False

	def __bind(self, shortcut, signal):
		from gtk import accelerator_parse
		keyval, modifier = accelerator_parse(shortcut)
#		if (keyval, modifier) in self.__editor.get_shortcuts(): return False
		from gtk import binding_entry_add_signal as bind
		bind(self.__view, keyval, modifier, signal, str, shortcut)
#		self.__editor.add_shortcut((keyval, modifier))
		return False

	def __add_bindings(self):
		self.__bind("Up", "up-press")
		return False

	def __destroy_cb(self, *args):
		return False

	def __up_cb(self, *args):
		print "up-press activated"
		return True

	def __enter_cb(self, *args):
		return False

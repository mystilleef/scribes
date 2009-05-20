from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE
from gobject import TYPE_PYOBJECT

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"update": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"show-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"hide-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		from Updater import Updater
		Updater(editor, self)
		from TreeView import TreeView
		TreeView(editor, self)
		from Window import Window
		Window(editor, self)

	def __init_attributes(self, editor):
		self.__editor = editor
		from os.path import join, split
		current_folder = split(globals()["__file__"])[0]
		glade_file = join(current_folder, "SymbolBrowser.glade")
		from gtk.gdk import pixbuf_new_from_file
		class_pixbuf = join(current_folder, "class.png")
		self.__class_pixbuf = pixbuf_new_from_file(class_pixbuf)
		function_pixbuf = join(current_folder, "function.png")
		self.__function_pixbuf = pixbuf_new_from_file(function_pixbuf)
		from gtk.glade import XML
		method_pixbuf = join(current_folder, "method.png")
		self.__method_pixbuf = pixbuf_new_from_file(method_pixbuf)
		from gtk.glade import XML
		self.__glade = XML(glade_file, "Window", "scribes")
		return

	def __get_glade(self):
		return self.__glade

	def __get_class_pixbuf(self):
		return self.__class_pixbuf

	def __get_function_pixbuf(self):
		return self.__function_pixbuf

	def __get_method_pixbuf(self):
		return self.__method_pixbuf

	glade = property(__get_glade)
	class_pixbuf = property(__get_class_pixbuf)
	function_pixbuf = property(__get_function_pixbuf)
	method_pixbuf = property(__get_method_pixbuf)

	def show_browser(self):
		self.emit("show-window")
		return

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return

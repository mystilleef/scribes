from SCRIBES.SignalConnectionManager import SignalManager

class Compositor(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "bar", self.__bar_cb, True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = editor.textview
		self.__bar = None
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __bar_cb(self, manager, bar):
		self.__bar = bar
		self.connect(bar, "expose-event", self.__bar_expose_cb)
		self.connect(self.__view, "expose-event", self.__view_expose_cb)
		return False

	def __view_expose_cb(self, view, event):
		from gtk import TEXT_WINDOW_TEXT
		window = view.get_window(TEXT_WINDOW_TEXT)
		cr = window.cairo_create()
		cr.set_source_pixmap(self.__bar.window, 
								self.__bar.allocation.x,
								self.__bar.allocation.y)
		from gtk.gdk import region_rectangle
		region = region_rectangle(self.__bar.allocation)
		r = region_rectangle(event.area)
		region.intersect(r)
		cr.region(region)
		cr.clip()
		#composite, with a 50% opacity
		from cairo import OPERATOR_OVER
		cr.set_operator(OPERATOR_OVER)
		cr.paint_with_alpha(0.9)
		self.__editor.refresh()
		return False

	def __bar_expose_cb(self, bar, event):
		cr = bar.window.cairo_create()
		from cairo import OPERATOR_OVER
		cr.set_operator(OPERATOR_OVER)
		from gtk.gdk import region_rectangle
		region = region_rectangle(event.area)
		cr.region(region)
		cr.fill()
		return False

	def __(self, parameters):
		return value



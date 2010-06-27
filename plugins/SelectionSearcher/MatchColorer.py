from SCRIBES.SignalConnectionManager import SignalManager

class Colorer(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "marked-matches", self.__matches_cb)
		self.connect(manager, "reset", self.__clear_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__tag = self.__create_tag()
		self.__colored = False
		return

	def __destroy(self):
		self.disconnect()
		self.__clear()
		del self
		return 

	def __create_tag(self):
		from gtk import TextTag
		tag = TextTag("selection_find_tag")
		self.__editor.textbuffer.get_tag_table().add(tag)
		tag.set_property("background", "yellow")
		tag.set_property("foreground", "brown")
		from pango import WEIGHT_ULTRABOLD
		tag.set_property("weight", WEIGHT_ULTRABOLD)
		return tag

	def __clear(self):
		if self.__colored is False: return False
		bounds = self.__editor.textbuffer.get_bounds()
		self.__editor.textbuffer.remove_tag(self.__tag, *bounds)
		self.__colored = False
		return False

	def __color(self, marks):
		self.__clear()
		if len(marks) < 2: return False
		apply_tag = self.__editor.textbuffer.apply_tag
		giam = self.__editor.textbuffer.get_iter_at_mark
		iam = lambda start, end: (giam(start), giam(end))
		tag = lambda start, end: apply_tag(self.__tag, *(iam(start, end)))
		self.__editor.response()
		[tag(*mark) for mark in marks]
		self.__editor.response()
		self.__colored = True
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __matches_cb(self, manager, marks):
		from gobject import idle_add
		idle_add(self.__color, marks, priority=9999)
		return False

	def __clear_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__clear, priority=9999)
#		self.__clear()
		return False

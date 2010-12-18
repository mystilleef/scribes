from SCRIBES.SignalConnectionManager import SignalManager

class Colorer(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "boundary-marks", self.__marks_cb)
		self.connect(manager, "exit-sparkup-mode", self.__exit_cb)
		self.connect(manager, "cursor-in-placeholder", self.__placeholder_cb)
		self.connect(manager, "removed-placeholders", self.__removed_cb, True)
		self.__sigid1 = self.connect(editor, "cursor-moved", self.__moved_cb, True)
		self.__block()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__blocked = False
		self.__marks = {}
		self.__placeholder = ()
		self.__nesting_level = 0
		self.__post_tag = self.__create_post_modification_tag()
		self.__mod_tag = self.__create_modification_tag()
		return

	def __update_tags(self, placeholder):
		try:
			self.__editor.freeze()
			self.__remove_tags_at(self.__placeholder)
			self.__tag(self.__placeholder, self.__post_tag)
			self.__placeholder = placeholder
			if not placeholder: raise AssertionError
			self.__tag(placeholder, self.__mod_tag)
		except AssertionError:
			pass
		finally:
			self.__editor.thaw()
		return False

	def __update_mod_tag(self):
		if not self.__placeholder: return False
		self.__editor.freeze()
		self.__tag(self.__placeholder, self.__mod_tag)
		self.__editor.thaw()
		return False

	def __tag(self, placeholder, tag):
		if not placeholder: return False
		start, end = self.__iter_at_marks(placeholder)
		self.__editor.textbuffer.apply_tag(tag, start, end)
		return False

	def __remove_tags_at(self, boundary):
		if not boundary: return False
		start, end = self.__iter_at_marks(boundary)
		self.__editor.textbuffer.remove_tag(self.__mod_tag, start, end)
		self.__editor.textbuffer.remove_tag(self.__post_tag, start, end)
		return False

	def __remove_tags(self):
		boundary = self.__marks[self.__nesting_level]
		self.__remove_tags_at(boundary)
		return False

	def __iter_at_marks(self, marks):
		if not marks: return None
		begin = self.__editor.textbuffer.get_iter_at_mark(marks[0])
		end = self.__editor.textbuffer.get_iter_at_mark(marks[1])
		return begin, end

	def __block(self):
		if self.__blocked: return False
		self.__editor.handler_block(self.__sigid1)
		self.__blocked = True
		return False

	def __unblock(self):
		if self.__blocked is False: return False
		self.__editor.handler_unblock(self.__sigid1)
		self.__blocked = False
		return False

	def __create_post_modification_tag(self):
		tag = self.__editor.textbuffer.create_tag()
		tag.set_property("background", "white")
		tag.set_property("foreground", "blue")
		from pango import WEIGHT_HEAVY, STYLE_ITALIC
		tag.set_property("weight", WEIGHT_HEAVY)
		tag.set_property("style", STYLE_ITALIC)
		return tag

	def __create_modification_tag(self):
		tag = self.__editor.textbuffer.create_tag()
		tag.set_property("background", "#ADD8E6")
#		tag.set_property("foreground", "white")
		tag.set_property("foreground", "#CB5A30")
		from pango import WEIGHT_HEAVY
		tag.set_property("weight", WEIGHT_HEAVY)
		return tag

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

	def __marks_cb(self, manager, marks):
		self.__nesting_level += 1
		self.__marks[self.__nesting_level] = marks
		return False

	def __exit_cb(self, *args):
		self.__remove_tags()
		del self.__marks[self.__nesting_level]
		self.__nesting_level -= 1
		if self.__nesting_level < 0: self.__nesting_level = 0
		self.__placeholder = ()
		if self.__nesting_level: return False
		self.__block()
		return False

	def __placeholder_cb(self, manager, placeholder):
		self.__update_tags(placeholder)
		return False

	def __moved_cb(self, *args):
		self.__remove_timer()
		from gobject import idle_add, PRIORITY_LOW
		self.__timer = idle_add(self.__update_mod_tag, priority=PRIORITY_LOW)
		return False

	def __removed_cb(self, *args):
		self.__unblock()
		return False

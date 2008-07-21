class Colorer(object):
	"""
	This class creates an object that colors placeholders.
	"""

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("tag-placeholder", self.__tag_placeholder_cb)
		self.__sigid3 = manager.connect("selected-placeholder", self.__selected_placeholder_cb)
		self.__sigid4 = manager.connect("template-boundaries", self.__template_boundaries_cb)
		self.__sigid5 = manager.connect("deactivate-template-mode", self.__deactivate_template_mode_cb)
		self.__sigid6 = editor.connect("cursor-moved", self.__cursor_moved_cb)
		self.__block_signal()
#		from gobject import idle_add
#		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		self.__old_placeholder = None
		self.__current_placeholder = None
		self.__boundaries_dictionary = {}
		self.__pre_tag = self.__create_pre_modification_tag()
		self.__pos_tag = self.__create_post_modification_tag()
		self.__mod_tag = self.__create_modification_tag()
		self.__enable = False
		self.__block = False
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__editor)
		del self
		self = None
		return

	def __precompile_methods(self):
		methods = (self.__tag, self.__tag_placeholder_cb, self.__tag_with_mod,
		self.__tag_with_pre, self.__tag_with_pos, self.__cursor_moved_cb,
		self.__check_boundary, self.__is_inside_range, self.__selected_placeholder_cb,
		self.__deactivate_template_mode_cb, self.__change_placeholder,
		self.__update_boundaries_dictionary, self.__remove_recent_boundaries,
		self.__remove_tags, self.__unblock_signal, self.__block_signal,
		self.__iter_at_marks)
		self.__editor.optimize(methods)
		return False

	def __unblock_signal(self):
		if self.__block is False: return
		self.__editor.handler_unblock(self.__sigid6)
		self.__block = False
		return

	def __block_signal(self):
		if self.__block: return
		self.__editor.handler_block(self.__sigid6)
		self.__block = True
		return

	def __create_pre_modification_tag(self):
		tag = self.__editor.textbuffer.create_tag()
		tag.set_property("background", "yellow")
		tag.set_property("foreground", "blue")
		from pango import WEIGHT_HEAVY
		tag.set_property("weight", WEIGHT_HEAVY)
		return tag

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
		tag.set_property("foreground", "#CB5A30")
		from pango import WEIGHT_HEAVY
		tag.set_property("weight", WEIGHT_HEAVY)
		return tag

	def __create_special_tag(self):
		tag = self.__editor.textbuffer.create_tag()
		tag.set_property("foreground", "pink")
		from pango import WEIGHT_HEAVY
		tag.set_property("weight", WEIGHT_HEAVY)
		return tag

	def __change_placeholder(self, placeholder):
		from copy import copy
		self.__old_placeholder = copy(self.__current_placeholder)
		self.__current_placeholder = placeholder
		self.__remove_tag(self.__old_placeholder, self.__mod_tag)
		self.__remove_tag(self.__old_placeholder, self.__pre_tag)
		self.__tag_with_pos(self.__old_placeholder)
		return False

	def __remove_tag(self, placeholder, tag):
		if not placeholder: return
		if len(placeholder) < 2: return
		start, end = self.__iter_at_marks(placeholder)
		self.__editor.textbuffer.remove_tag(tag, start, end)
		return

	def __iter_at_marks(self, marks):
		if not marks: return None
		if len(marks) < 2: return None
		begin = self.__editor.textbuffer.get_iter_at_mark(marks[0])
		end = self.__editor.textbuffer.get_iter_at_mark(marks[1])
		return begin, end

	def __tag(self, placeholder, tag):
		start, end = self.__iter_at_marks(placeholder)
		self.__editor.textbuffer.apply_tag(tag, start, end)
		return

	def __tag_with_pre(self, placeholder):
		if len(placeholder) != 2: return False
		self.__tag(placeholder, self.__pre_tag)
		return False

	def __tag_with_mod(self, placeholder):
		if not placeholder: return False
		if len(placeholder) < 2: return False
		self.__tag(placeholder, self.__mod_tag)
		return False

	def __tag_with_pos(self, placeholder):
		if not placeholder: return False
		if len(placeholder) < 2: return False
		if len(placeholder) > 2:
			self.__tag(placeholder[:2], self.__pos_tag)
			self.__tag_with_pos(placeholder[2:])
		else:
			self.__tag(placeholder, self.__pos_tag)
		return False

	def __remove_tags(self):
		key = len(self.__boundaries_dictionary)
		boundary = self.__boundaries_dictionary[key]
		start, end = self.__iter_at_marks(boundary)
		self.__editor.textbuffer.remove_tag(self.__pre_tag, start, end)
		self.__editor.textbuffer.remove_tag(self.__mod_tag, start, end)
		self.__editor.textbuffer.remove_tag(self.__pos_tag, start, end)
		return

	def __update_boundaries_dictionary(self, boundaries):
		key = len(self.__boundaries_dictionary) + 1
		self.__boundaries_dictionary[key] = boundaries
		return False

	def __remove_recent_boundaries(self):
		key = len(self.__boundaries_dictionary)
		marks = self.__boundaries_dictionary[key]
		for mark in marks:
			self.__editor.delete_mark(mark)
			del mark
		del self.__boundaries_dictionary[key]
		return False

	def __is_inside_range(self, boundary):
		if boundary is None: return False
		if len(boundary) < 2: return False
		start, end = self.__iter_at_marks(boundary)
		if self.__editor.cursor.equal(start): return True
		if self.__editor.cursor.equal(end): return True
		if self.__editor.cursor.in_range(start, end): return True
		return False

	def __check_boundary(self):
		if not len(self.__boundaries_dictionary): return False
		boundary = self.__current_placeholder
		if not boundary: return False
		if self.__is_inside_range(boundary):
			self.__tag_with_mod(boundary)
		else:
			if not self.__is_inside_range(self.__old_placeholder): return False
			self.__tag_with_pos(self.__old_placeholder)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __tag_placeholder_cb(self, manager, placeholder):
		self.__tag_with_pre(placeholder)
		return False

	def __selected_placeholder_cb(self, manager, placeholder):
		self.__change_placeholder(placeholder)
		return False

	def __deactivate_template_mode_cb(self, *args):
		self.__remove_tags()
		self.__remove_recent_boundaries()
		self.__current_placeholder = self.__old_placeholder = None
		if len(self.__boundaries_dictionary): return False
		self.__block_signal()
		return False

	def __template_boundaries_cb(self, manager, boundaries):
		self.__enable = True
		self.__update_boundaries_dictionary(boundaries)
		self.__unblock_signal()
		return False

	def __cursor_moved_cb(self, *args):
		self.__check_boundary()
		return False

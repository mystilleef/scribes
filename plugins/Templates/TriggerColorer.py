message = "Template trigger highlighted"

class Colorer(object):
	"""
	This class creates an object that colors template triggers.
	"""

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("trigger-found", self.__trigger_found_cb)
		self.__sigid3 = manager.connect("no-trigger-found", self.__no_trigger_found_cb)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__precompile_methods, priority=9000)

	def __init_attributes(self, editor, manager):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__is_highlighted = False
		self.__highlight_tag = self.__create_highlight_tag()
		self.__sigid1 = self.__sigid2 = None
		self.__status_id = None
		self.__lmark = self.__editor.create_left_mark()
		self.__rmark = self.__editor.create_right_mark()
		return

	def __destroy(self):
		self.__editor.delete_mark(self.__lmark)
		self.__editor.delete_mark(self.__rmark)
		self.__buffer.get_tag_table().remove(self.__highlight_tag)
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return

	def __precompile_methods(self):
		methods = (self.__trigger_found_cb, self.__no_trigger_found_cb,
			self.__color_trigger, self.__uncolor_trigger, self.__process,
			self.__get_trigger_position, self.__mark_trigger_position)
		self.__editor.optimize(methods)
		return False

	def __create_highlight_tag(self):
		from gtk import TextTag
		tag = TextTag("template-trigger")
		self.__editor.textbuffer.get_tag_table().add(tag)
		tag.set_property("background", "black")
		tag.set_property("foreground", "orange")
		from pango import WEIGHT_HEAVY
		tag.set_property("weight", WEIGHT_HEAVY)
		return tag

################################################################################
#
#						Processing Methods
#
################################################################################

	def __process(self, trigger):
		position = self.__get_trigger_position(len(trigger))
		self.__color_trigger(position)
		self.__mark_trigger_position(position)
		return False

	def __get_trigger_position(self, trigger_length):
		cursor = self.__editor.cursor
		begin = cursor.copy()
		for count in xrange(trigger_length): begin.backward_char()
		return begin, cursor

	def __mark_trigger_position(self, position):
		self.__buffer.move_mark(self.__lmark, position[0])
		self.__buffer.move_mark(self.__rmark, position[1])
		return

	def __color_trigger(self, position):
		self.__uncolor_trigger(False)
		self.__buffer.apply_tag(self.__highlight_tag, position[0], position[1])
		self.__is_highlighted = True
		return False

	def __uncolor_trigger(self, message=True):
		start = self.__buffer.get_iter_at_mark(self.__lmark)
		end = self.__buffer.get_iter_at_mark(self.__rmark)
		self.__buffer.remove_tag(self.__highlight_tag, start, end)
		self.__is_highlighted = False
		return False

################################################################################
#
# 						Event and Signal Callbacks
#
################################################################################

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __trigger_found_cb(self, manager, trigger):
#		if self.__is_highlighted: return
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__tid)
		except AttributeError:
			pass
		finally:
			self.__tid = idle_add(self.__process, trigger, priority=9999)
			self.__editor.set_message(message, "info")
		return

	def __no_trigger_found_cb(self, *args):
		if self.__is_highlighted is False: return
		try:
			from gobject import idle_add, PRIORITY_LOW, source_remove
			source_remove(self.__textid)
		except AttributeError:
			pass
		finally:
			self.__textid = idle_add(self.__uncolor_trigger, priority=9999)
			self.__editor.unset_message(message, "info")
		return

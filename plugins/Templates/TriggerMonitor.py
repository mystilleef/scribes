class Monitor(object):

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = editor.connect("cursor-moved", self.__cursor_moved_cb)
		self.__sigid3 = self.__view.connect("key-press-event", self.__key_press_event_cb)
		self.__sigid4 = manager.connect("loaded-language-templates", self.__loaded_language_templates_cb)
		self.__sigid5 = manager.connect("loaded-general-templates", self.__loaded_general_templates_cb)
		self.__sigid6 = manager.connect("activate-template-mode", self.__activate_template_mode_cb)
		self.__sigid7 = manager.connect("deactivate-template-mode", self.__deactivate_template_mode_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		self.__trigger_found = False
		self.__template_mode = 0
		from collections import deque
		self.__language_triggers = deque([])
		self.__general_triggers = deque([])
		self.__view = editor.textview
		return

	def __precompile_methods(self):
		methods = (self.__is_trigger, self.__emit_no_trigger_found_signal,
			self.__emit_trigger_found_signal, self.__cursor_moved_cb,
			self.__key_press_event_cb, self.__activate_template_mode_cb,
			self.__deactivate_template_mode_cb)
		self.__editor.optimize(methods)
		return

	def __destroy(self):
		self.__language_triggers.clear()
		self.__general_triggers.clear()
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__view)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		self.__editor.disconnect_signal(self.__sigid7, self.__manager)
		del self
		self = None
		return

	def __is_trigger(self, word):
		if not word: return False
		if word in self.__language_triggers: return True
		if word in self.__general_triggers: return True
		return False

	def __check_trigger(self):
		from utils import get_template_word
		word = get_template_word(self.__editor.cursor, self.__editor.textbuffer)
		if self.__is_trigger(word):
			self.__emit_trigger_found_signal(word)
		else:
			self.__emit_no_trigger_found_signal()
		return False

	def __emit_trigger_found_signal(self, word):
		self.__trigger_found = True
		self.__manager.emit("trigger-found", word)
		return

	def __emit_no_trigger_found_signal(self):
		if self.__trigger_found is False: return
		self.__manager.emit("no-trigger-found")
		self.__trigger_found = False
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __loaded_language_templates_cb(self, manager, dictionary):
		try:
			language = self.__editor.language
			get_trigger = lambda key: key[len(language):]
			keys = [get_trigger(key) for key in dictionary.keys()]
			from collections import deque
			self.__language_triggers = deque(keys)
		except AttributeError:
			pass
		return

	def __loaded_general_templates_cb(self, manager, dictionary):
		get_trigger = lambda key: key[len("General"):]
		keys = [get_trigger(key) for key in dictionary.keys()]
		from collections import deque
		self.__general_triggers = deque(keys)
		return

	def __deactivate_template_mode_cb(self, *args):
		self.__template_mode -= 1
		return False

	def __activate_template_mode_cb(self, *args):
		self.__template_mode += 1
		return False

	def __cursor_moved_cb(self, *args):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__cursor_id)
		except AttributeError:
			pass
		self.__cursor_id = idle_add(self.__check_trigger, priority=9999)
		return False

	def __key_press_event_cb(self, view, event):
		from gtk.keysyms import Tab, ISO_Left_Tab
		if not (event.keyval in (Tab, ISO_Left_Tab)): return False
		result = False
		if event.keyval == Tab and self.__trigger_found:
			self.__manager.emit("expand-trigger")
			result = True
		elif event.keyval == Tab and self.__template_mode:
			self.__manager.emit("next-placeholder")
			result = True
		elif event.keyval == ISO_Left_Tab and self.__template_mode:
			self.__manager.emit("previous-placeholder")
			result = True
		return result


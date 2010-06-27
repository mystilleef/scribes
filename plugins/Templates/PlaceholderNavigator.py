class Navigator(object):

	def __init__(self, editor, manager):
		editor.response()
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("previous-placeholder", self.__previous_placeholder_cb)
		self.__sigid3 = manager.connect("next-placeholder", self.__next_placeholder_cb)
		self.__sigid4 = manager.connect("template-boundaries", self.__template_boundaries_cb)
		self.__sigid5 = manager.connect("placeholders", self.__placeholders_cb)
		self.__sigid6 = manager.connect("deactivate-template-mode", self.__deactivate_template_mode_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)
		editor.response()

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		self.__placeholder_dictionary = {}
		self.__boundaries_dictionary = {}
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		del self
		self = None
		return

	def __precompile_methods(self):
		methods = (self.__select_placeholder, self.__next_placeholder,
			self.__next_placeholder_cb, self.__previous_placeholder_cb,
			self.__previous_placeholder, self.__placeholders_cb,
			self.__template_boundaries_cb, self.__deactivate_template_mode_cb,
			self.__rearrange_placeholders, self.__generate_navigation_dictionary,
			self.__update_navigation_dictionary, self.__update_mirrors,
			self.__update_boundaries_dictionary, self.__update_placeholders_dictionary,
			self.__get_current_placeholders, self.__get_cursor_placeholder,
			self.__replace_text, self.__extract_placeholders, self.__get_text,
			self.__update_mirrors)
		self.__editor.optimize(methods)
		return False

	def __select_placeholder(self, placeholder, end=False):
		if end and (len(placeholder) > 2):
			key = len(self.__boundaries_dictionary)
			emark = self.__boundaries_dictionary[key][1]
			iterator = self.__editor.textbuffer.get_iter_at_mark(emark)
			self.__editor.textbuffer.place_cursor(iterator)
		elif len(placeholder) > 1:
			mstart, mend = placeholder[:2]
			start = self.__editor.textbuffer.get_iter_at_mark(mstart)
			end = self.__editor.textbuffer.get_iter_at_mark(mend)
			self.__editor.textbuffer.select_range(start, end)
		else:
			iterator = self.__editor.textbuffer.get_iter_at_mark(placeholder[0])
			self.__editor.textbuffer.place_cursor(iterator)
		self.__manager.emit("selected-placeholder", placeholder)
		return

	def __next_placeholder(self):
		placeholders = self.__get_current_placeholders()
		placeholder = placeholders.popleft()
		if len(placeholder) > 2: self.__update_mirrors(self.__get_text((placeholder[0], placeholder[1])), placeholder[2:])
		placeholders.append(placeholder)
		key = len(self.__placeholder_dictionary)
		self.__placeholder_dictionary[key] = placeholders
		placeholder = placeholders[0]
		if placeholder: return self.__select_placeholder(placeholder)
		placeholder = (placeholders[-1][-1],)
		self.__select_placeholder(placeholder, True)
		self.__manager.emit("deactivate-template-mode")
		return

	def __previous_placeholder(self):
		placeholders = self.__get_current_placeholders()
		placeholder = placeholders.pop()
		placeholders.appendleft(placeholder)
		key = len(self.__placeholder_dictionary)
		self.__placeholder_dictionary[key] = placeholders
		placeholder = placeholders[0]
		if placeholder is None: return self.__previous_placeholder()
		self.__select_placeholder(placeholder)
		return

	def __update_mirrors(self, text, placeholders):
		if not placeholders: return
		if len(placeholders) < 2: return
		self.__replace_text(text, placeholders[0], placeholders[1])
		self.__update_mirrors(text, placeholders[2:])
		return

	def __replace_text(self, text, bmark, emark):
		begin = self.__editor.textbuffer.get_iter_at_mark(bmark)
		end = self.__editor.textbuffer.get_iter_at_mark(emark)
		self.__editor.textbuffer.place_cursor(begin)
		self.__editor.textbuffer.delete(begin, end)
		self.__editor.textbuffer.insert_at_cursor(text)
		return

	def __get_current_placeholders(self):
		key = len(self.__placeholder_dictionary)
		placeholders = self.__placeholder_dictionary[key]
		return placeholders

	def __get_cursor_placeholder(self, placeholders):
		for placeholder in placeholders:
			if len(placeholder) == 1: return placeholder
		return None

	def __rearrange_placeholders(self, placeholders):
		dictionary = self.__generate_navigation_dictionary(placeholders)
		placeholders = self.__extract_placeholders(dictionary)
		self.__manager.emit("last-placeholder", placeholders[-1])
		placeholders.append(None)
		from collections import deque
		return deque(placeholders)

	def __extract_placeholders(self, dictionary):
		values = dictionary.values()
		values.sort()
		extract_placeholders = lambda x: tuple(x[1])
		placeholders = [extract_placeholders(placeholder) for placeholder in values]
		return placeholders

	def __generate_navigation_dictionary(self, placeholders):
		dictionary = {}
		count = 0
		for placeholder in placeholders:
			count += 1
			dictionary = self.__update_navigation_dictionary(placeholder, dictionary, count)
		return dictionary

	def __update_navigation_dictionary(self, placeholder, dictionary, count):
		text = self.__get_text(placeholder)
		if text == "cursor": count = 9999
		if dictionary.has_key(text):
			data = dictionary[text]
			count = data[0]
			placeholder_ = data[1]
			placeholder_.extend(placeholder)
			dictionary[text] = count, placeholder_
		else:
			dictionary[text] = count, list(placeholder)
		return dictionary

	def __get_text(self, placeholder):
		if len(placeholder) < 2: return "cursor"
		begin = self.__editor.textbuffer.get_iter_at_mark(placeholder[0])
		end = self.__editor.textbuffer.get_iter_at_mark(placeholder[1])
		return self.__editor.textbuffer.get_text(begin, end)

	def __update_boundaries_dictionary(self, boundaries):
		key = len(self.__boundaries_dictionary) + 1
		self.__boundaries_dictionary[key] = boundaries
		return False

	def __update_placeholders_dictionary(self, placeholders):
		placeholders = self.__rearrange_placeholders(placeholders)
		key = len(self.__placeholder_dictionary) + 1
		self.__placeholder_dictionary[key] = placeholders
		self.__select_placeholder(placeholders[0])
		return False

	def __remove_recent_placeholders(self):
		key = len(self.__placeholder_dictionary)
		values = self.__placeholder_dictionary[key]
		values.remove(None)
		for marks in values:
			for mark in marks:
				self.__editor.delete_mark(mark)
				del mark
		del self.__placeholder_dictionary[key]
		return False

	def __remove_recent_boundaries(self):
		key = len(self.__boundaries_dictionary)
		marks = self.__boundaries_dictionary[key]
		del self.__boundaries_dictionary[key]
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __previous_placeholder_cb(self, *args):
		self.__previous_placeholder()
		self.__editor.response()
		return

	def __next_placeholder_cb(self, *args):
		self.__editor.response()
		self.__next_placeholder()
		return

	def __template_boundaries_cb(self, manager, boundaries):
		self.__update_boundaries_dictionary(boundaries)
		return

	def __placeholders_cb(self, manager, placeholders):
		self.__update_placeholders_dictionary(placeholders)
		return

	def __deactivate_template_mode_cb(self, *args):
		self.__remove_recent_placeholders()
		self.__remove_recent_boundaries()
#		self.__editor.response()
		return

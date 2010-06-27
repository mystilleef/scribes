from gettext import gettext as _

class Processor(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("tabs-to-spaces", self.__tabs_to_spaces_cb)
		self.__sigid3 = manager.connect("spaces-to-tabs", self.__spaces_to_tabs_cb)
		self.__sigid4 = manager.connect("remove-trailing-spaces", self.__remove_trailing_spaces_cb)
		self.__sigid5 = manager.connect("extracted-text", self.__extracted_text_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__use_tabs = None
		self.__function = None
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		del self
		self = None
		return

	def __send_processed_text(self, text):
		lines = text.splitlines()
		lines = [self.__function(line) for line in lines]
		text = "\n".join(lines) + "\n"
		self.__manager.emit("processed-text", text)
		self.__use_tabs = None
		self.__function = None
		return False

	def __convert(self, line):
		self.__editor.response()
		indentation_width = self.__editor.textview.get_tab_width()
		characters = self.__get_indent_characters(line)
		characters = self.__get_new_indentation(characters, indentation_width)
		if self.__use_tabs: characters = "\t" * (len(characters)/indentation_width)
		message = _("Converted spaces to tabs") if self.__use_tabs else _("Converted tabs to spaces")
		self.__editor.update_message(message, "pass")
		self.__editor.response()
		return characters + line.lstrip(" \t")

	def __get_indent_characters(self, line):
		characters = ""
		indentation_characters = (" ", "\t")
		for character in line:
			if not (character in indentation_characters): break
			characters += character
		return characters

	def __get_new_indentation(self, characters, indentation_width):
		characters = characters.replace("\t", (" " * indentation_width))
		number_of_characters = len(characters)
		if not number_of_characters: return ""
		remainder = number_of_characters % indentation_width
		return " " * (number_of_characters - remainder)

	def __remove(self, line):
		self.__editor.response()
		line = line.rstrip(" \t")
		self.__editor.response()
		message = _("Removed trailing spaces")
		self.__editor.update_message(message, "pass")
		return line

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __spaces_to_tabs_cb(self, *args):
		self.__use_tabs = True
		self.__function = self.__convert
		return False

	def __tabs_to_spaces_cb(self, *args):
		self.__use_tabs = False
		self.__function = self.__convert
		return False

	def __remove_trailing_spaces_cb(self, *args):
		self.__function = self.__remove
		return False

	def __extracted_text_cb(self, manager, text):
		self.__send_processed_text(text)
		return False

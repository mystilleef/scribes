from gettext import gettext as _

class Processor(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("extracted-text", self.__text_cb)
		self.__sigid3 = manager.connect("indent", self.__indent_cb)
		self.__sigid4 = manager.connect("unindent", self.__unindent_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__textview = editor.textview
		self.__function = None
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		del self
		self = None
		return 

	def __send_indented_text(self, text):
		text = self.__process_text(text)
		self.__manager.emit("iprocessed-text", text)
		self.__manager.emit("processed-text", text)
		self.__function = None
		return False

	def __process_text(self, text):
		lines = text.splitlines()
		use_tabs = not self.__textview.get_insert_spaces_instead_of_tabs()
		indentation_width = self.__textview.get_tab_width()
		lines = [self.__process_line(line, use_tabs, indentation_width) for line in lines]
		return "\n".join(lines)

	def __process_line(self, line, use_tabs, indentation_width):
		characters = self.__get_indent_characters(line)
		characters = self.__get_new_indentation(characters, indentation_width)
		if use_tabs: characters = "\t" * (len(characters)/indentation_width)
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
		remainder = number_of_characters if number_of_characters == 0 else (number_of_characters % indentation_width)
		return self.__function(number_of_characters, indentation_width, remainder)

	def __indent(self, number_of_characters, indentation_width, remainder):
		message = _("Indented line(s)")
		self.__editor.update_message(message, "pass")
		if number_of_characters == 0: return " " * indentation_width
		return " " * (number_of_characters + (indentation_width - remainder))

	def __dedent(self, number_of_characters, indentation_width, remainder):
		message = _("Dedented line(s)")
		self.__editor.update_message(message, "pass")
		if number_of_characters == 0: return ""
		dedent = remainder if remainder else indentation_width
		return " " * (number_of_characters - dedent)

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __text_cb(self, manager, text):
		self.__send_indented_text(text)
		return False

	def __indent_cb(self, *args):
		self.__function = self.__indent
		return False

	def __unindent_cb(self, *args):
		self.__function = self.__dedent
		return False

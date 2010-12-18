from SCRIBES.SignalConnectionManager import SignalManager

class Inserter(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "sparkup-template", self.__template_cb)
		self.connect(manager, "destroy", self.__destroy_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __insert(self, template):
		# convert spaces to tabs over vice versa depending on user's configuration.
		template = self.__format(template)
		# add indentation to templates before inserting it in the buffer.
		template = self.__indent(template)
		# insert proper.
		self.__editor.textbuffer.insert_at_cursor(template)
		self.__manager.emit("inserted-template", template)
		return False

	def __indent(self, template):
		indentation = self.__get_indentation()
		if not indentation: return template
		lines = template.split("\n")
		if len(lines) == 1: return template
		indent = lambda line: indentation + line
		indented_lines = [indent(line) for line in lines[1:]]
		indented_lines.insert(0, lines[0])
		return "\n".join(indented_lines)

	def __get_indentation(self):
		text = self.__editor.get_line_text()
		indentation = []
		for character in text:
			if not (character in (" ", "\t")): break
			indentation.append(character)
		return "".join(indentation)

	def __format(self, template):
		view = self.__editor.textview
		tab_width = view.get_property("tab-width")
		# Convert tabs to spaces
		template = template.expandtabs(tab_width)
		use_spaces = view.get_property("insert-spaces-instead-of-tabs")
		if use_spaces: return template
		# Convert spaces to tabs
		return self.__indentation_to_tabs(template, tab_width)

	def __indentation_to_tabs(self, template, tab_width):
		tab_indented_lines = [self.__spaces_to_tabs(line, tab_width) for line in template.splitlines(True)]
		return "".join(tab_indented_lines)

	def __spaces_to_tabs(self, line, tab_width):
		if line[0] != " ": return line
		indentation_width = self.__get_indentation_width(line)
		if indentation_width < tab_width: return line
		indentation = ("\t" * (indentation_width/tab_width)) + (" " * (indentation_width%tab_width))
		return indentation + line[indentation_width:]

	def __get_indentation_width(self, line):
		from itertools import takewhile
		is_space = lambda character: character == " "
		return len([space for space in takewhile(is_space, line)])

	def __template_cb(self, manager, template):
		from gobject import idle_add
		idle_add(self.__insert, template)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

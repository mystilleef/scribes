# Match any strings enclosed in ${} with the exception of ${}.
from re import UNICODE, compile
placeholder_pattern = compile("\$\{[^${}]*\}", UNICODE)
special_placeholders = ("${time}", "${timestring}", "${timestamp}",
					"${date}", "${day}", "${month}", "${year}", "${author}")

def replace_special_placeholder(placeholder):
	"""
	Replaces a variable/'special placeholder' with it's value.

	Any variables added here need to be added
	to self.special_placeholders in self.__init_attributes
	"""
	if placeholder == "${day}":
		from time import localtime
		thetime = localtime()
		return pad_zero(thetime[2])
	if placeholder == "${month}":
		from time import localtime
		thetime = localtime()
		return pad_zero(thetime[1])
	if placeholder == "${year}":
		from time import localtime
		thetime = localtime()
		return pad_zero(thetime[0])
	if placeholder == "${date}":
		from time import localtime
		thetime = localtime()
		return "%s:%s:%s" % (pad_zero(thetime[0]), pad_zero(thetime[1]), pad_zero(thetime[2]))
	if placeholder == "${time}":
		from time import localtime
		thetime = localtime()
		return "%s:%s:%s" % (pad_zero(thetime[3]), pad_zero(thetime[4]), pad_zero(thetime[5]))
	if placeholder == "${timestring}":
		from time import ctime
		return ctime()
	if placeholder == "${timestamp}":
		from time import localtime
		thetime = localtime()
		return "[%s-%s-%s] %s:%s:%s" % (thetime[0], pad_zero(thetime[1]), pad_zero(thetime[2]), pad_zero(thetime[3]), pad_zero(thetime[4]), pad_zero(thetime[5]))
	if placeholder == "${author}":
		return get_author_name()

def remove_trailing_spaces_on_line(sourceview, line_number):
	"""
	Convert beginning tab characters to space characters on a line.

	@param sourceview: The gtksourceview buffer's container
	@type sourceview: A gtksourceview.SourceView object.

	@param line_number: The line to perform conversion operation on.
	@type line_number: An Integer object.

	@return: True if the line was converted.
	@rtype: An Boolean object.
	"""
	sourcebuffer = sourceview.get_property("buffer")
	begin_position = sourcebuffer.get_iter_at_line(line_number)
	transition_position = begin_position.copy()
	end_position = begin_position.copy()
	end_position.forward_to_line_end()
	transition_position.forward_to_line_end()
	if transition_position.equal(begin_position): return
	from operator import not_, contains
	while True:
		transition_position.backward_char()
		if not_(contains((" ", "\t"), transition_position.get_char())):
			transition_position.forward_char()
			break
	if transition_position.equal(end_position): return
	sourcebuffer.delete(transition_position, end_position)
	return

def word_to_cursor(textbuffer, iterator):
	if iterator.starts_line(): return None
	temporary = iterator.copy()
	temporary.backward_char()
	from operator import contains, eq
	if contains((" ", "\t"), temporary.get_char()): return None
	while True:
		if temporary.starts_line(): break
		temporary.backward_char()
		if contains((" ", "\t", "`"), temporary.get_char()):
			if eq(temporary.get_char(), "`"): break
			temporary.forward_char()
			break
	text = textbuffer.get_text(temporary, iterator)
	return text

def get_placeholders(string):
	"""
	Get all placeholders in a string if any.

	@param string: A string representing a template.
	@type string: A String object.

	@return: All placeholders in a template.
	@rtype: A List object.
	"""
	from operator import not_, contains
	if not_(has_placeholders(string)): return []
	is_not_special = lambda placeholder: not_(contains(special_placeholders, placeholder))
	# Return all strings enclosed in ${} with the exception of ${}.
	from re import findall, UNICODE
	placeholders = findall(placeholder_pattern, string, UNICODE)
	return filter(is_not_special, placeholders)

def has_placeholders(string):
	"""
	Check whether or not a string contains placeholders.

	@param string: A string representing a template.
	@type string: A String object.

	@return: True if a string has placeholders.
	@rtype: A Boolean object.
	"""
	from re import search, UNICODE
	# Match any strings enclosed in ${} with the exception of ${}.
	if search(placeholder_pattern, string, UNICODE): return True
	return False

def get_special_placeholders(string):
	"""
	Get all placeholders in a string if any.

	@param placeholders: A list of placeholders
	@type placeholders: A List object.

	@return: All placeholders in a template.
	@rtype: A List object.
	"""
	from operator import contains
	from re import findall, UNICODE
	placeholders = findall(placeholder_pattern, string, UNICODE)
	has_special_placeholder = lambda placeholder: contains(special_placeholders, placeholder)
	return filter(has_special_placeholder, placeholders)

def insert_string(textbuffer, string):
	"""
	Insert a string into the editing area.

	@param textbuffer: The editor's editing area.
	@type textbuffer: A ScribesTextBuffer object.

	@param string: A string representing a template.
	@type string: A String object.
	"""
	from SCRIBES.lines import get_beginning_spaces
	spaces = get_beginning_spaces(textbuffer)
	if spaces:	string = __indent_string(string, "".join(spaces))
	textbuffer.insert_at_cursor(string)
	return

def __indent_string(string, indentation):
	"""
	Automatically indent string for insertion in editing area.

	@param string: A string to be indented.
	@type string: A String object.

	@param indentation: Space or tab characters to place before string.
	@type indentation: A String object.

	@return: An indented string.
	@rtype: A String object.
	"""
	lines = string.split("\n")
	from operator import eq
	if eq(len(lines), 1): return string
	indent = lambda line: indentation + line
	indented_lines = map(indent, lines[1:])
	indented_lines.insert(0, lines[0])
	return "\n".join(indented_lines)

def remove_trailing_spaces_on_line(sourceview, line_number):
	"""
	Convert beginning tab characters to space characters on a line.

	@param sourceview: The gtksourceview buffer's container
	@type sourceview: A gtksourceview.SourceView object.

	@param line_number: The line to perform conversion operation on.
	@type line_number: An Integer object.

	@return: True if the line was converted.
	@rtype: An Boolean object.
	"""
	sourcebuffer = sourceview.get_property("buffer")
	begin_position = sourcebuffer.get_iter_at_line(line_number)
	transition_position = begin_position.copy()
	end_position = begin_position.copy()
	end_position.forward_to_line_end()
	transition_position.forward_to_line_end()
	if transition_position.equal(begin_position): return False
	from operator import not_, contains
	while True:
		transition_position.backward_char()
		if not_(contains((" ", "\t"), transition_position.get_char())):
			transition_position.forward_char()
			break
	if transition_position.equal(end_position): return False
	sourcebuffer.delete(transition_position, end_position)
	return True

def pad_zero(num):
	if num < 10:
		return "0" + str(num)
	return str(num)

def get_author_name():
	"""
	Get author name from /etc/passwd.

	This code was contributed by Herman Polloni.

	@return: Return name of author.
	@rtype: A String object.
	"""
	import pwd,posix
	# get the user information
	# returns a list with the following information:
	# (username, 'x', uid, gid, real life information, home, shell)
	user = pwd.getpwuid(posix.getuid())
	# try to get the user's real name first
	# the real life information is a csv containing real information from the user
	# we want the first field that usually is the real name
	name = user[4].split(',')[0]
	# if the name we get is not what we want
	if name is None or name == '':
		# get the username
		name = user[0]
	return name

try:
	from psyco import bind
	bind(word_to_cursor)
	bind(insert_string)
except ImportError:
	pass

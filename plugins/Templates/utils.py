# Match any strings enclosed in ${} with the exception of ${}.
from re import UNICODE, compile as compile_
placeholder_pattern = compile_("\$\{[^${}]*\}", UNICODE)
special_placeholders = ("${time}", "${timestring}", "${timestamp}",
					"${date}", "${day}", "${month}", "${year}", "${author}")


def replace_special_placeholder(placeholder):
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
	sourcebuffer = sourceview.get_property("buffer")
	begin_position = sourcebuffer.get_iter_at_line(line_number)
	transition_position = begin_position.copy()
	end_position = begin_position.copy()
	end_position.forward_to_line_end()
	transition_position.forward_to_line_end()
	if transition_position.equal(begin_position): return
	while True:
		transition_position.backward_char()
		if transition_position.get_char() in (" ", "\t"): continue
		transition_position.forward_char()
		break
	if transition_position.equal(end_position): return
	sourcebuffer.delete(transition_position, end_position)
	return

def word_to_cursor(textbuffer, iterator):
	if iterator.starts_line(): return None
	iterator.backward_char()
	if iterator.get_char() in (" ", "\t", "\n", "\r", "\r\n"): return None
	iterator.forward_char()
	from SCRIBES.Utils import backward_to_line_begin
	start = backward_to_line_begin(iterator.copy())
	text = textbuffer.get_text(start, iterator)
	words = text.split()[-1].split("`")
	text = "`" + words[-1] if len(words) > 1 else words[-1]
	return text

def get_placeholders(string):
	if not has_placeholders(string): return []
	is_not_special = lambda placeholder: not (placeholder in special_placeholders)
	# Return all strings enclosed in ${} with the exception of ${}.
	from re import findall, UNICODE
	placeholders = findall(placeholder_pattern, string, UNICODE)
	return filter(is_not_special, placeholders)

def has_placeholders(string):
	from re import search, UNICODE
	# Match any strings enclosed in ${} with the exception of ${}.
	if search(placeholder_pattern, string, UNICODE): return True
	return False

def get_special_placeholders(string):
	from re import findall
	placeholders = findall(placeholder_pattern, string, UNICODE)
	has_special_placeholder = lambda placeholder: placeholder in special_placeholders
	return filter(has_special_placeholder, placeholders)

def get_beginning_spaces(textbuffer):
	iterator = textbuffer.get_iter_at_mark(textbuffer.get_insert())
	from SCRIBES.Utils import backward_to_line_begin, forward_to_line_end
	begin_position, end_position = backward_to_line_begin(iterator.copy()), forward_to_line_end(iterator.copy())
	if begin_position.get_char() in ["\n", "\x00"]: return None
	spaces = []
	transition_position = begin_position.copy()
	while transition_position.get_char() in [" ", "\t"]:
		spaces.append(transition_position.get_char())
		transition_position.forward_char()
	return spaces

def insert_string(textbuffer, string):
	spaces = get_beginning_spaces(textbuffer)
	if spaces: string = __indent_string(string, "".join(spaces))
	textbuffer.insert_at_cursor(string)
	return

def __indent_string(string, indentation):
	lines = string.split("\n")
	if len(lines) == 1: return string
	indent = lambda line: indentation + line
	indented_lines = [indent(line) for line in lines[1:]]
	indented_lines.insert(0, lines[0])
	return "\n".join(indented_lines)

def pad_zero(num):
	if num < 10: return "0" + str(num)
	return str(num)

def get_author_name():
	import pwd,posix
	user = pwd.getpwuid(posix.getuid())
	name = user[4].split(',')[0]
	if name is None or name == '': name = user[0]
	return name

def get_template_word(iterator, buffer_):
	if iterator.starts_line(): return None
	chars = (" ", "\t", "(", "{", "<", "[", "=", ")", "}", ">", "]", "|")
	begin = iterator.copy()
	while True:
		if begin.starts_line(): return buffer_.get_text(begin, iterator)
		success = begin.backward_char()
		if success is False: return buffer_.get_text(begin, iterator)
		if not (begin.get_char() in chars): continue
		begin.forward_char()
		break
	return buffer_.get_text(begin, iterator)

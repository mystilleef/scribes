from re import U, M, L, escape, compile as compile_
BEGIN_CHARACTER = "/\*+"
END_CHARACTER = "\*+/"
flags = U|M|L
BEGIN_RE = compile_(BEGIN_CHARACTER, flags)
END_RE = compile_(END_CHARACTER, flags)

def has_comment(text):
	text = text.strip(" \t")
	if text.startswith("//"): return True
	if text.startswith("/*") and text.endswith("*/"): return True
	return False

def get_indentation(text):
	is_indentation_character = lambda character: character in (" ", "\t")
	from itertools import takewhile
	whitespaces =  takewhile(is_indentation_character, text)
	return "".join(whitespaces)

def comment(text, multiline=False):
	if multiline is False: return __comment_single_line(text)
	return __comment_multiple_lines(text)

def __comment_single_line(text):
	return get_indentation(text) + "// " + text.lstrip(" \t")

def __comment_multiple_lines(text):
	indent_value = lambda line: len(line.replace("\t", "    "))
	line_indentations = [(indent_value(line), get_indentation(line)) for line in text.splitlines()]
	line_indentations.sort()
	indentation = line_indentations[0][1]
	return indentation + "/*\n" + text.rstrip(" \t") + "\n" + indentation + "*/"

def uncomment(text):
	tmp = text.lstrip(" \t")
	if tmp.startswith("//"): return __uncomment_single_line(text)
	text = BEGIN_RE.sub("", text)
	return END_RE.sub("", text)

def __uncomment_single_line(text):
	tmp = text.lstrip(" \t")
	if tmp.startswith("// "): return text.replace("// ", "", 1)
	return text.replace("//", "", 1)

def __uncomment_multiple_lines(text):
	return False

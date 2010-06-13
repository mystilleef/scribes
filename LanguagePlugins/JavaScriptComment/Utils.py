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

def comment(text, multiline=False):
	if multiline is False: return "//" + text
	return "/*\n" + text.rstrip(" \t") + "\n*/"

def uncomment(text):
	tmp = text.lstrip(" \t")
	if tmp.startswith("//"): return text.replace("//", "", 1)
	text = BEGIN_RE.sub("", text)
	return END_RE.sub("", text)

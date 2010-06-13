#from re import U, M, L, escape, compile as compile_
#BEGIN_CHARACTER = "/\*+" # r"%s" % escape("/*+")
#END_CHARACTER = r"%s" % escape("*/")
#flags = U|M|L
#BEGIN_RE = compile_(BEGIN_CHARACTER, flags)
#END_RE = compile_(END_CHARACTER, flags)

class Searcher(object):

	def find_comment_boundaries(self, text, cursor):
		# Find all start comment characters
		from Utils import BEGIN_RE, END_RE
		start_matches = self.__find_matches(BEGIN_RE, text, 0)
		if not start_matches: return ()
		# Find all end comment characters
		end_matches = self.__find_matches(END_RE, text, 1)
		if not end_matches: return ()
		if len(start_matches) != len(end_matches): print "Possible comment character mismatch"
		# Pair opening and closing comment characters
		paired_offsets = zip(start_matches, end_matches)
		# Find comment boundaries around cursor offset.
		return self.__find_boundary(paired_offsets, cursor)

	def __find_matches(self, RE, text, offset):
		iterator = RE.finditer(text.decode("utf-8"))
		matches = [match.span()[offset] for match in iterator]
		return matches

	def __find_boundary(self, paired_offsets, cursor):
		for start, end in paired_offsets:
			if start < cursor < end: return start, end
		return ()

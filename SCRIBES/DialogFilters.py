from gettext import gettext as _

def create_filter(name="", mime="", pattern=""):
	from gtk import FileFilter
	filefilter = FileFilter()
	filefilter.set_name(name)
	filefilter.add_mime_type(mime)
	if pattern: filefilter.add_pattern(pattern)
	return filefilter

def create_filter_list():
	filter_list = [
		create_filter(_("Text Documents"), "text/plain"),
		create_filter(_("Python Documents"), "text/x-python"),
		create_filter(_("Ruby Documents"), "text/x-ruby"),
		create_filter(_("Perl Documents"), "text/x-perl"),
		create_filter(_("C Documents"), "text/csrc"),
		create_filter(_("C++ Documents"), "text/c++src"),
		create_filter(_("C# Documents"), "text/csharp"),
		create_filter(_("Java Documents"), "text/x-java"),
		create_filter(_("PHP Documents"), "text/x-php"),
		create_filter(_("HTML Documents"), "text/html"),
		create_filter(_("XML Documents"), "text/xml"),
		create_filter(_("Haskell Documents"), "text/x-haskell"),
		create_filter(_("Scheme Documents"), "text/x-scheme"),
		create_filter(_("All Documents"), "", "*"),
	]
	return filter_list

def default_page_setup():
	from gtk import PageSetup, UNIT_INCH, PaperSize
	from gtk import paper_size_get_default, PAGE_ORIENTATION_LANDSCAPE
	setup = PageSetup()
	setup.set_paper_size_and_default_margins(PaperSize(paper_size_get_default()))
	return setup

def get_compositor(editor):
	editor.response()
	view = editor.textview
	font_name = view.get_pango_context().get_font_description().to_string()
	from gtksourceview2 import PrintCompositor
	compositor = PrintCompositor(view.get_buffer())
	compositor.set_body_font_name(font_name)
	compositor.set_footer_font_name(font_name)
	compositor.set_print_footer(True)
	compositor.set_footer_format(True, "", editor.filename, "%N of %Q")
	compositor.set_header_font_name(font_name)
	compositor.set_print_header(True)
	compositor.set_header_format(True, editor.name, "%b %d, %Y", "%N")
	compositor.set_highlight_syntax(True)
	compositor.set_line_numbers_font_name(font_name)
#	compositor.set_print_line_numbers(1)
	compositor.set_tab_width(view.get_property("tab-width"))
	compositor.set_wrap_mode(view.get_wrap_mode())
	editor.response()
	return compositor
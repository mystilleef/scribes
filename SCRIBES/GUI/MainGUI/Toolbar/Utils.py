def never_focus(widget):
	widget.set_property("can-default", False)
	widget.set_property("can-focus", False)
	widget.set_property("has-default", False)
	widget.set_property("has-focus", False)
	widget.set_property("is-focus", False)
	widget.set_property("receives-default", False)
	return False

def new_separator(draw=True, expand=False):
	from gtk import SeparatorToolItem
	separator = SeparatorToolItem()
	never_focus(separator)
	separator.set_draw(draw)
	separator.set_expand(expand)
	separator.show()
	return separator

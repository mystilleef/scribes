# Utility functions shared among modules belong here.
BOOKMARK_NAME = "ScribesBookmark"

def create_bookmark_image(editor):
	pixbuf = __create_pixbuf(editor)
	editor.textview.set_mark_category_pixbuf(BOOKMARK_NAME, pixbuf)
	editor.textview.set_mark_category_priority(BOOKMARK_NAME, 1)
	return

def __create_pixbuf(editor):
	from os.path import join
	current_folder = editor.get_current_folder(globals())
	image_file = join(current_folder, "bookmarks.png")
	from gtk import Image
	image = Image()
	image.set_from_file(image_file)
	pixbuf = image.get_pixbuf()
	return pixbuf

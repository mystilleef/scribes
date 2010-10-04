def new_uri_exists(editor, name):
	from gio import File
	return File(get_new_uri(editor, name)).query_exists()

def get_new_uri(editor, name):
	uri_folder = __get_uri_folder(editor)
	from os.path import join
	return join(uri_folder, name)

def __get_uri_folder(editor):
	from gio import File
	if editor.uri: return File(editor.uri).get_parent().get_uri()
	return editor.desktop_folder_uri

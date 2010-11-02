def window_is_active(editor):
	try:
		if editor is None: return False
		if editor.window.props.is_active is False: return False
		if editor.textview.props.has_focus is False: return False
	except AttributeError:
		return False
	return True

def get_modification_time(file_path):
	from SCRIBES.Utils import get_modification_time
	return get_modification_time(file_path)

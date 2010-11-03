from SCRIBES.Utils import response

MARK_NAME = "ScribesMultiEditMark"

def delete_mark(textbuffer, mark):
	response()
	mark.set_visible(False)
	response()
	if mark.get_deleted(): return
	response()
	textbuffer.delete_mark(mark)
	response()
	del mark
	mark = None
	return

MARK_NAME = "ScribesMultiEditMark"

def delete_mark(textbuffer, mark):
	mark.set_visible(False)
	if mark.get_deleted(): return
	textbuffer.delete_mark(mark)
	del mark
	mark = None
	return

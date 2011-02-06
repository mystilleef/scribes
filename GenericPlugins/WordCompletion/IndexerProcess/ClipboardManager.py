class Manager(object):

	def __init__(self, manager):
		from gtk import clipboard_get
		clipboard = clipboard_get()
		clipboard.connect("owner-change", self.__change_cb, manager)

	def __change_cb(self, clipboard, event, manager):
		clipboard.request_text(self.__text_cb, manager)
		return False

	def __text_cb(self, clipboard, text, manager):
		if not text: return False
		from string import whitespace
		text = text.strip(whitespace)
		if not text: return False
		manager.emit("clipboard-text", text)
		return False

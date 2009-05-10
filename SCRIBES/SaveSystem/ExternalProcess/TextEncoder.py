class Encoder(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		manager.connect("encode-text", self.__encode_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		return

	def __encode(self, data):
		try:
			encoding, text = data[2], data[3]
			encoded_text = text.encode(encoding)
			data = data[0], data[1], data[2], encoded_text
			self.__manager.emit("replace-file", data)
		except:
			from gettext import gettext as _
			message = _("""
Module: SCRIBES/SaveSystem/ExternalProcess/TextEncoder.py
Class: Encoder
Method: __encode
Exception: Unknown
Error: Failed to encode text before writing to file.

Automatic saving is temporarily disabled. You will loose information in
this window if you close it. Please try saving the file again, preferably
to a different location like your desktop.""")
			data = data + (message, )
			self.__manager.emit("oops", data)
		return False

	def __encode_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__encode, data)
		return False

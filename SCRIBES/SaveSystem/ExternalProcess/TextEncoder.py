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
			self.__manager.emit("create-swap-file", data)
		except:
			from gettext import gettext as _
			message = _("Failed to encode file for writing.")
			data = data + (message, )
			self.__manager.emit("oops", data)
		return False

	def __encode_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__encode, data)
		return False

from gio import Error

class GError(Error):

	def __init__(self, code, message):
		Error.__init__(self)
		self.code = code
		self.message = message

class Manager(object):

	def __init__(self, editor):
		editor.response()
		from FileEncodingsUpdater import Updater
		Updater(self, editor)
		from EncodingGuessListUpdater import Updater
		Updater(self, editor)
		editor.response()

	def format_encoding(self, encoding):
		from Utils import format_encoding
		return format_encoding(encoding)

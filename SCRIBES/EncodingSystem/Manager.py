class Manager(object):

	def __init__(self, editor):
		editor.response()
		from Error.Trigger import Trigger
		Trigger(editor)
		from SupportedEncodings.Trigger import Trigger
		Trigger(editor)
		from FileEncodingsUpdater import Updater
		Updater(self, editor)
		from EncodingGuessListUpdater import Updater
		Updater(self, editor)
		from EncodingListUpdater import Updater
		Updater(self, editor)
		from ComboBoxData.Manager import Manager
		Manager(editor)
		editor.response()

	def format_encoding(self, encoding):
		from Utils import format_encoding
		return format_encoding(encoding)

class Manager(object):

	def __init__(self, editor):
		editor.response()
		from MessageBar import MessageBar
		MessageBar(self, editor)
		editor.response()

class Manager(object):

	def __init__(self, editor):
		editor.response()
		from MessageBar.Manager import Manager
		Manager(editor)
		from Feedback.Manager import Manager
		Manager(editor)
		editor.response()

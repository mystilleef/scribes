class Manager(object):

	def __init__(self, editor):
		editor.response()
		from Bar.Manager import Manager
		Manager(editor)
		from Feedback.Manager import Manager
		Manager(editor)
		editor.response()

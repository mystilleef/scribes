class Manager(object):

	def __init__(self, editor):
		from MessageBar.Manager import Manager
		Manager(editor)
		from Feedback.Manager import Manager
		Manager(editor)

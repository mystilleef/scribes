class Manager(object):

	def __init__(self, editor):
		from CloseWindowBinder import Binder
		Binder(editor)
		from CloseWindowNoSaveBinder import Binder
		Binder(editor)
		from ShutdownBinder import Binder
		Binder(editor)
		from FullscreenBinder import Binder
		Binder(editor)

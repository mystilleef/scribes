class Generator(object):

	def __init__(self, editor):
		editor.response()
		self.__generate_stamp(editor)
		self.__destroy()
		editor.response()

	def __generate_stamp(self, editor):
		from time import strftime
		editor.set_data("uniquestamp", strftime("%Y-%m-%d %H:%M:%S"))
		return

	def __destroy(self):
		del self
		self = None
		return

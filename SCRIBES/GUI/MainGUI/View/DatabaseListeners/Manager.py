class Manager(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		from FontListener import Listener
		Listener(self, editor)
		from TabWidthListener import Listener
		Listener(self, editor)
		from UseTabsListener import Listener
		Listener(self, editor)
		from TextWrappingListener import Listener
		Listener(self, editor)
		from ShowRightMarginListener import Listener
		Listener(self, editor)
		from RightMarginPositionListener import Listener
		Listener(self, editor)
		from SpellCheckListener import Listener
		Listener(self, editor)
		editor.response()

	def get_path(self, database):
		from os.path import join
		folder = join(self.__editor.metadata_folder, "Preferences")
		return join(folder, database)

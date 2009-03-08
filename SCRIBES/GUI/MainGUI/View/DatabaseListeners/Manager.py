class Manager(object):

	def __init__(self, editor):
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

	def get_database_uri(self, database):
		from os.path import join
		folder = join(self.__editor.metadata_folder, "Preferences")
		_path = join(folder, database)
		from gnomevfs import get_uri_from_local_path as get_uri
		return get_uri(_path)

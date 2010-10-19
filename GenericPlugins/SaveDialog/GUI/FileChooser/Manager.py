class Manager(object):

	def __init__(self, manager, editor):
		from Initializer import Initializer
		Initializer(manager, editor)
		from FolderChanger import Changer
		Changer(manager, editor)
		from URISelector import Selector
		Selector(manager, editor)
#		from URILoader import Loader
#		Loader(manager, editor)
		from ActivatorHandler import Handler
		Handler(manager, editor)

class Initializer(object):

	def __init__(self, editor, manager, uri, encoding):
		editor.set_data("InstanceManager", manager)
		editor.response()
		from RegistrationManager import Manager
		Manager(editor)
		from ContentDetector import Detector
		Detector(editor, uri)
		from FileModificationMonitor import Monitor
		Monitor(editor)
		from URIManager import Manager
		Manager(editor, uri)
		from LanguageManager import Manager
		Manager(editor, uri)
		from SchemeManager import Manager
		Manager(editor)
		from GladeObjectManager import Manager
		Manager(editor)
		from BusyManager import Manager
		Manager(editor)
		from RecentManager import Manager
		Manager(editor)
		from GUI.Manager import Manager
		Manager(editor, uri)
########################################################################
		from EncodingSystem.Manager import Manager
		Manager(editor)
		from FileChangeMonitor import Monitor
		Monitor(editor)
		from SaveSystem.Manager import Manager
		Manager(editor)
		from TriggerSystem.Manager import Manager
		Manager(editor)
		from ReadonlyManager import Manager
		Manager(editor)
		# Register with instance manager after a successful editor
		# initialization.
		manager.register_editor(editor)
		from BarObjectManager import Manager
		Manager(editor)
		from FullScreenManager import Manager
		Manager(editor)
		# This should be the last lines in this method.
		from PluginSystemInitializer import Initializer
		Initializer(editor, uri)
		from URILoader.Manager import Manager
		Manager(editor, uri, encoding)
		editor.response()

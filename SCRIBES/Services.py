class InitServices(object):

	def __init__(self, editor, manager, uri, encoding):
		editor.set_data("InstanceManager", manager)
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
		# Manages the behavior of the window.
		from Window import Window
		Window(editor, uri)
		# Manages he behavior of the buffer's container.
		from TextView import View
		View(editor)
		# Manages the behavior of the buffer.
		from TextBuffer import Buffer
		Buffer(editor)
		# Manages error and information window.
		from MessageWindow import Window
		Window(editor)
		# Manages encoding information.
		from EncodingManager import Manager
		Manager(editor)
		# Object responsible for sending data to external process via
		# DBus to save files. An external process does the I/O operations.
		from SaveCommunicator import Communicator
		Communicator(editor)
		# Object responsible for saving files.
		from FileSaver import Saver
		Saver(editor)
		# Object responsible for deciding when to save files
		# automatically.
		from SaveManager import Manager
		Manager(editor)
		# Manages window that shows supported encodings.
		from SupportedEncodingsGUIManager import Manager
		Manager(editor)
		# Object responsible for showing encoding error window. The window
		# allows users to load files with the correct encoding.
		from EncodingErrorManager import Manager
		Manager(editor)
		# Object that share information for encoding combo box.
		from EncodingComboBoxDataManager import Manager
		Manager(editor)
		from StatusFeedback import Feedback
		Feedback(editor)
		from StatusImage import Image
		Image(editor)
		from StatusCursorPosition import Position
		Position(editor)
		from StatusInsertionType import Type
		Type(editor)
		from StatusContainer import Container
		Container(editor)
		from RecentManager import Manager
		Manager(editor)
		# Toolbar object.
		from Toolbar import Toolbar
		Toolbar(editor)
		from PopupMenuManager import Manager
		Manager(editor)
		from TriggerManager import Manager
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
		# Load files or initialize plugins. Always load files, if any,
		# before initializing plugin systems. This should be the last
		# line in this method.
		from PluginSystemInitializer import Initializer
		Initializer(editor, uri)
		from URILoader.Manager import Manager
		Manager(editor, uri, encoding)

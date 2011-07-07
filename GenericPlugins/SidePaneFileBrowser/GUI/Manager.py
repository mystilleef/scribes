class Manager(object):

	def __init__(self, manager, editor):
		self.__arrange_widgets(manager, editor)
		scrolled_window = manager.gui.get_object("scrolledwindow1")
		from gtk import POLICY_AUTOMATIC, POLICY_ALWAYS
		scrolled_window.set_policy(POLICY_AUTOMATIC, POLICY_AUTOMATIC)
		from ToolbarSensitivityManager import Manager
		Manager(manager)
		from TreeView.Manager import Manager
		Manager(manager, editor)
		toolbutton_names = ["back", "up", "home"]
		from ToolButton import Button
		for name in toolbutton_names: Button(manager, editor, name)
		from ToggleToolButton import Button
		Button(manager, editor)
		from DisplayManager import Manager
		Manager(manager, editor)

	def __arrange_widgets(self, manager, editor):
		browser_container = manager.gui.get_object("BrowserContainer1")
		browser_container.unparent()
		side_pane =  editor.gui.get_widget("SidePane")
		side_pane.pack_start(browser_container, True, True, 10)
		return False

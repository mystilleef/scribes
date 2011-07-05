from ..SensitivityManager import SensitivityManager

class Manager(SensitivityManager):

	def __init__(self, manager):
		treeview = manager.gui.get_object("TreeView")
		SensitivityManager.__init__(self, manager, treeview)

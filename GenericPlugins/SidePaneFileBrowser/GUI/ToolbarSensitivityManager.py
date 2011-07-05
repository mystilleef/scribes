from SensitivityManager import SensitivityManager

class Manager(SensitivityManager):

	def __init__(self, manager):
		toolbar = manager.gui.get_object("Toolbar")
		SensitivityManager.__init__(self, manager, toolbar)

from Utils import open_database
from os.path import join
basepath = join("Preferences", "ColorTheme.gdb")

def get_value():
	try:
		theme = "oblivion"
		database = open_database(basepath, "r")
		theme = database["theme"]
	except:
		pass
	finally:
		database.close()
	return theme

def set_value(theme):
	try:
		database = open_database(basepath, "w")
		database["theme"] = theme
	finally:
		database.close()
	return

from SCRIBES.Utils import open_database
from os.path import join
basepath = join("Preferences", "ColorTheme.gdb")

def get_value():
	try:
		value = "oblivion"
		database = open_database(basepath, "r")
		value = database["theme"]
	except:
		pass
	finally:
		database.close()
	return value

def set_value(value):
	try:
		database = open_database(basepath, "w")
		database["theme"] = value
	finally:
		database.close()
	return

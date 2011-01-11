from SCRIBES.Utils import open_database
from os.path import join
basepath = join("Preferences", "WidgetTransparency.gdb")

def get_value():
	try:
		value = False
		database = open_database(basepath, "r")
		value = database["transparency"]
	except:
		pass
	finally:
		database.close()
	return value

def set_value(value):
	try:
		database = open_database(basepath, "w")
		database["transparency"] = value
	finally:
		database.close()
	return

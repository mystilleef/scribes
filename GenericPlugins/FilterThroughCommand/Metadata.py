from SCRIBES.Utils import open_database
from os.path import join
basepath = join("PluginPreferences", "FilterThroughCommandOutputMode.gdb")

def get_value():
	try:
		value = "replace"
		database = open_database(basepath, "r")
		value = database["output"]
	except:
		pass
	finally:
		database.close()
	return value

def set_value(value):
	try:
		database = open_database(basepath, "w")
		database["output"] = value
	finally:
		database.close()
	return

from SCRIBES.Utils import open_database
from os.path import join
basepath = join("PluginPreferences", "LexicalScopeHighlight.gdb")

def get_value():
	try:
		value = "orange"
		database = open_database(basepath, "r")
		value = database["color"]
	except KeyError:
		pass
	finally:
		database.close()
	return value

def set_value(color):
	try:
		database = open_database(basepath, "w")
		database["color"] = color
	finally:
		database.close()
	return

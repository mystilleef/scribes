from SCRIBES.Utils import open_database
from os.path import join
basepath = join("PluginPreferences", "FocusLastDocument.gdb")

def get_value():
	try:
		value = None
		database = open_database(basepath, "r")
		value = database["last_document"]
	except:
		pass
	finally:
		database.close()
	return value

def set_value(value):
	try:
		database = open_database(basepath, "w")
		database["last_document"] = value
	finally:
		database.close()
	return

from SCRIBES.Utils import open_database
from os.path import join
basepath = join("PluginPreferences", "TriggerArea", "Size.gdb")

def get_value():
	try:
		size = 24
		database = open_database(basepath, "r")
		size = database["size"]
	except:
		pass
	finally:
		database.close()
	return size

def set_value(size):
	try:
		database = open_database(basepath, "w")
		database["size"] = size
	finally:
		database.close()
	return

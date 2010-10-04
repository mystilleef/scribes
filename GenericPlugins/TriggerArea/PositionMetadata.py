from SCRIBES.Utils import open_database
from os.path import join
basepath = join("PluginPreferences", "TriggerArea", "Position.gdb")

def get_value():
	try:
		position = "top-right"
		database = open_database(basepath, "r")
		position = database["position"]
	except:
		pass
	finally:
		database.close()
	return position

def set_value(position):
	try:
		database = open_database(basepath, "w")
		database["position"] = position
	finally:
		database.close()
	return

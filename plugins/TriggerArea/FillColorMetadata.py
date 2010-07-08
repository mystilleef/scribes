from SCRIBES.Utils import open_database
from os.path import join
basepath = join("PluginPreferences", "TriggerArea", "FillColor.gdb")

def get_value():
	try:
		color = "brown"
		database = open_database(basepath, "r")
		color = database["color"]
	except:
		pass
	finally:
		database.close()
	return color

def set_value(color):
	try:
		database = open_database(basepath, "w")
		database["color"] = color
	finally:
		database.close()
	return

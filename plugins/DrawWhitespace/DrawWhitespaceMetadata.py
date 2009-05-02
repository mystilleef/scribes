from SCRIBES.Utils import open_database
basepath = "/PluginPreferences/DrawWhitespace.gdb"

def get_value():
	try:
		value = False
		database = open_database(basepath, "r")
		value = database["show"]
	except KeyError:
		pass
	finally:
		database.close()
	return value

def set_value(value):
	database = open_database(basepath, "w")
	database["show"] = value
	database.close()
	return

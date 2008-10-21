from SCRIBES.Utils import open_database
basepath = "/PluginPreferences/MatchCase.gdb"

def get_value():
	try:
		value = False
		database = open_database(basepath, "r")
		value = database["match_case"]
	except KeyError:
		pass
	finally:
		database.close()
	return value

def set_value(match_case):
	try:
		database = open_database(basepath, "w")
		database["match_case"] = match_case
	finally:
		database.close()
	return

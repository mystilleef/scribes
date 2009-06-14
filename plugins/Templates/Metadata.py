from SCRIBES.Utils import open_database
basepath = "/PluginPreferences/Templates.gdb"

def get_value():
	try:
		dictionary = {}
		database = open_database(basepath, "r")
		dictionary = database["templates"]
	except:
		pass
	finally:
		database.close()
	return dictionary

def set_value(dictionary):
	try:
		database = open_database(basepath, "w")
		database["templates"] = dictionary
	finally:
		database.close()
	return

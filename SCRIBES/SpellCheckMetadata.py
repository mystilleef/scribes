from Utils import open_database
basepath = "/Preferences/SpellCheck.gdb"

def get_value():
	try:
		value = False
		database = open_database(basepath, "r")
		value = database["spell_check"]
	except KeyError:
		pass
	finally:
		database.close()
	return value

def set_value(value):
	try:
		database = open_database(basepath, "w")
		database["spell_check"] = value
	finally:
		database.close()
	return

from SCRIBES.Utils import open_database
basepath = "Preferences/MarginPosition.gdb"

def get_value():
	try:
		value = 72
		database = open_database(basepath, "r")
		value = database["margin_position"]
	except KeyError:
		pass
	finally:
		database.close()
	return value

def set_value(value):
	try:
		database = open_database(basepath, "w")
		database["margin_position"] = value
	finally:
		database.close()
	return

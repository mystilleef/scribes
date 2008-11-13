from SCRIBES.Utils import open_database
basepath = "Preferences/DisplayRightMargin.gdb"

def get_value():
	try:
		value = True
		database = open_database(basepath, "r")
		value = database["display_right"]
	except KeyError:
		pass
	finally:
		database.close()
	return value

def set_value(value):
	try:
		database = open_database(basepath, "w")
		database["display_right"] = value
	finally:
		database.close()
	return

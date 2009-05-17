from Utils import open_database
basepath = "/Preferences/TabWidth.gdb"

def get_value():
	try:
		value = 4
		database = open_database(basepath, "r")
		value = database["tab_width"]
	except KeyError:
		pass
	finally:
		database.close()
	return value

def set_value(value):
	try:
		database = open_database(basepath, "w")
		database["tab_width"] = value
	finally:
		database.close()
	return

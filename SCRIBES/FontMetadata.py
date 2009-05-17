from Utils import open_database
basepath = "/Preferences/Font.gdb"

def get_value():
	try:
		value = "Monospace 12"
		database = open_database(basepath, "r")
		value = database["font"]
	except KeyError:
		pass
	finally:
		database.close()
	return value

def set_value(value):
	try:
		database = open_database(basepath, "w")
		database["font"] = value
	finally:
		database.close()
	return

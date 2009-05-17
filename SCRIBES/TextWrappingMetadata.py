from Utils import open_database
basepath = "/Preferences/TextWrapping.gdb"

def get_value():
	try:
		value = True
		database = open_database(basepath, "r")
		value = database["text_wrapping"]
	except KeyError:
		pass
	finally:
		database.close()
	return value

def set_value(value):
	try:
		database = open_database(basepath, "w")
		database["text_wrapping"] = value
	finally:
		database.close()
	return

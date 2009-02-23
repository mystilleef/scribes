from Utils import open_database
basepath = "/Preferences/EncodingGuessList.gdb"

def get_value():
	try:
		value = []
		database = open_database(basepath, "r")
		value = database["encodings"]
	except KeyError:
		pass
	finally:
		database.close()
	return value

def set_value(value):
	try:
		database = open_database(basepath, "w")
		database["encodings"] = value
	finally:
		database.close()
	return

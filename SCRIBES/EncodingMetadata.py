from Utils import open_database
basepath = "Preferences/Encoding.gdb"

def get_value():
	try:
		value = ["ISO-8859-1", "ISO-8859-15"]
		database = open_database(basepath, "r")
		value = database["encoding"]
	except KeyError:
		pass
	finally:
		database.close()
	return value

def set_value(encoding_list):
	try:
		database = open_database(basepath, "w")
		database["encoding"] = encoding_list
	finally:
		database.close()
	return

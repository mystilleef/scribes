from Utils import open_database
basepath = "Preferences/EncodedFiles.gdb"

def get_value(uri):
	try:
		value = "utf-8"
		database = open_database(basepath, "r")
		value = database[str(uri)]
	except KeyError:
		pass
	finally:
		database.close()
	return value

def set_value(uri, encoding):
	try:
		database = open_database(basepath, "w")
		database[str(uri)] = encoding
	finally:
		database.close()
	return

def remove_value(uri):
	try:
		database = open_database(basepath, "w")
		del database[str(uri)]
	except KeyError:
		pass
	finally:
		database.close()
	return

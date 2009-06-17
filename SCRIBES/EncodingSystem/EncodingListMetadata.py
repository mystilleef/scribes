from SCRIBES.Utils import open_database
basepath = "Preferences/EncodingList.gdb"

def get_value():
	try:
		encodings = ["ISO-8859-1", "ISO-8859-15"]
		database = open_database(basepath, "r")
		encodings = database["encodings"]
	except KeyError:
		pass
	finally:
		database.close()
	return encodings

def set_value(encodings):
	try:
		database = open_database(basepath, "w")
		database["encodings"] = encodings
	finally:
		database.close()
	return

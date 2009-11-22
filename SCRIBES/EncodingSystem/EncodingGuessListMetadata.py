from SCRIBES.Utils import open_database
from os.path import join
basepath = join("Preferences", "EncodingGuessList.gdb")

def get_value():
	try:
		encodings = []
		database = open_database(basepath, "r")
		encodings = database["encodings"]
	except KeyError:
		pass
	finally:
		database.close()
	return encodings

def set_value(encoding):
	try:
		database = None
		if encoding == "utf-8": return
		encodings = get_value()
		if encoding in encodings: return
		encodings.append(encoding)
		database = open_database(basepath, "w")
		database["encodings"] = encodings
	finally:
		if database is not None: database.close()
	return

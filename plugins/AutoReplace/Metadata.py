from SCRIBES.Utils import open_database
basepath = "abbreviations.gdb"

def get_value():
	try:
		dictionary = {}
		database = open_database(basepath, "r")
		dictionary = database["dictionary"]
	except KeyError:
		pass
	finally:
		database.close()
	return dictionary

def set_value(dictionary):
	try:
		database = open_database(basepath, "w")
		database["dictionary"] = dictionary
	finally:
		database.close()
	return

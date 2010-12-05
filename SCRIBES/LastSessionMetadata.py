from SCRIBES.Utils import open_database
from os.path import join
basepath = join("Preferences", "LastSessionUris.gdb")

def get_value():
	try:
		value = []
		database = open_database(basepath, "r")
		value = database["last_session_uris"]
	except:
		pass
	finally:
		database.close()
	return value

def set_value(value):
	try:
		database = open_database(basepath, "w")
		database["last_session_uris"] = value
	finally:
		database.close()
	return

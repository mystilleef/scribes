from SCRIBES.Utils import open_database
from os.path import join
basepath = join("Preferences", "MinimalMode.gdb")

def get_value():
	try:
		minimal_mode = False
		database = open_database(basepath, "r")
		minimal_mode = database["minimal_mode"]
	except KeyError:
		pass
	finally:
		database.close()
	return minimal_mode

def set_value(minimal_mode):
	try:
		database = open_database(basepath, "w")
		database["minimal_mode"] = minimal_mode
	finally:
		database.close()
	return

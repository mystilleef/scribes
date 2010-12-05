from SCRIBES.Utils import open_database
from os.path import join
basepath = join("PluginPreferences", "PythonErrorCheckType.gdb")

def get_value():
	try:
		value = True
		database = open_database(basepath, "r")
		value = database["more_error_checks"]
	except:
		pass
	finally:
		database.close()
	return value

def set_value(value):
	try:
		database = open_database(basepath, "w")
		database["more_error_checks"] = value
	finally:
		database.close()
	return

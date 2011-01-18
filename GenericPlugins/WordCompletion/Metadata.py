from SCRIBES.Utils import open_database
from os.path import join
basepath = join("PluginPreferences", "ToggleWordCompletion.gdb")

def get_value():
	try:
		value = True
		database = open_database(basepath, "r")
		value = database["enable_word_completion"]
	except:
		pass
	finally:
		database.close()
	return value

def set_value(value):
	try:
		database = open_database(basepath, "w")
		database["enable_word_completion"] = value
	finally:
		database.close()
	return

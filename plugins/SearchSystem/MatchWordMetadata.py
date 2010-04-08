from SCRIBES.Utils import open_database
from os.path import join
basepath = join("PluginPreferences", "MatchWord.gdb")

def get_value():
	try:
		value = False
		database = open_database(basepath, "r")
		value = database["match_word"]
	except KeyError:
		pass
	finally:
		database.close()
	return value

def set_value(match_word):
	try:
		database = open_database(basepath, "w")
		database["match_word"] = match_word
	finally:
		database.close()
	return

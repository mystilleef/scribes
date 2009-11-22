from Utils import open_database
from os.path import join
basepath = join("Preferences", "Languages", "SpellCheck.gdb")

def get_value(language):
	try:
		spellcheck = False
		database = open_database(basepath, "r")
		spellcheck = database[language]
	except KeyError:
		if "def" in database: spellcheck = database["def"]
	finally:
		database.close()
	return spellcheck

def set_value(data):
	try:
		language, spellcheck = data
		database = open_database(basepath, "w")
		database[language] = spellcheck
	finally:
		database.close()
	return

def reset(language):
	try:
		database = open_database(basepath, "w")
		del database[language]
	except KeyError:
		pass
	finally:
		database.close()
	return

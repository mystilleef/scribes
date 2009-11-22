from Utils import open_database
from os.path import join
basepath = join("Preferences", "Languages", "DisplayRightMargin.gdb")

def get_value(language):
	try:
		display_margin = True
		database = open_database(basepath, "r")
		display_margin = database[language]
	except KeyError:
		if "def" in database: display_margin = database["def"]
	finally:
		database.close()
	return display_margin

def set_value(data):
	try:
		language, display_margin = data
		database = open_database(basepath, "w")
		database[language] = display_margin
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

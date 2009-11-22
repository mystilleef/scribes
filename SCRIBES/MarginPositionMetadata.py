from Utils import open_database
from os.path import join
basepath = join("Preferences", "Languages", "MarginPosition.gdb")

def get_value(language):
	try:
		margin_position = 72
		database = open_database(basepath, "r")
		margin_position = database[language]
	except KeyError:
		if "def" in database: margin_position = database["def"]
	finally:
		database.close()
	return margin_position

def set_value(data):
	try:
		language, margin_position = data
		database = open_database(basepath, "w")
		database[language] = margin_position
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

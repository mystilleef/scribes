from Utils import open_database
basepath = "/Preferences/Languages/TabWidth.gdb"

def get_value(language):
	try:
		tab_width = 4
		database = open_database(basepath, "r")
		tab_width = database[language]
	except KeyError:
		pass
	finally:
		database.close()
	return tab_width

def set_value(data):
	try:
		language, tab_width = data
		database = open_database(basepath, "w")
		database[language] = tab_width
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

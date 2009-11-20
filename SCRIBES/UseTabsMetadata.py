from Utils import open_database
basepath = "/Preferences/Languages/UseTabs.gdb"

def get_value(language):
	try:
		use_tabs = True
		database = open_database(basepath, "r")
		use_tabs = database[language]
	except KeyError:
		if "def" in database: use_tabs = database["def"]
	finally:
		database.close()
	return use_tabs

def set_value(data):
	try:
		language, use_tabs = data
		database = open_database(basepath, "w")
		database[language] = use_tabs
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

from Utils import open_database
basepath = "/Preferences/Languages/TextWrapping.gdb"

def get_value(language):
	try:
		text_wrapping = True
		database = open_database(basepath, "r")
		text_wrapping = database[language]
	except KeyError:
		pass
	finally:
		database.close()
	return text_wrapping

def set_value(data):
	try:
		language, text_wrapping = data
		database = open_database(basepath, "w")
		database[language] = text_wrapping
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

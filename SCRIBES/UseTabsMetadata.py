from Utils import open_database
basepath = "/Preferences/UseTabs.gdb"

def get_value():
	try:
		value = True
		database = open_database(basepath, "r")
		value = database["use_tabs"]
	except KeyError:
		pass
	finally:
		database.close()
	return value

def set_value(value):
	try:
		database = open_database(basepath, "w")
		database["use_tabs"] = value
	finally:
		database.close()
	return

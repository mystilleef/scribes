from SCRIBES.Utils import open_database
basepath = "/PluginPreferences/SearchType.gdb"

def get_value():
	try:
		# Type values are: "normal", "forward" and "backward"
		type_ = "normal"
		database = open_database(basepath, "r")
		type_ = database["type_"]
	except KeyError:
		pass
	finally:
		database.close()
	return type_

def set_value(type_):
	if not (type_ in ("normal", "forward", "backward")): raise ValueError
	try:
		database = open_database(basepath, "w")
		database["type_"] = type_
	finally:
		database.close()
	return

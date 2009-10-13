from SCRIBES.Utils import open_database
basepath = "/PluginPreferences/SearchMode.gdb"

def get_value():
	try:
		# Mode values are: "default", "regex" and "findasyoutype"
		mode = "findasyoutype"
		database = open_database(basepath, "r")
		mode = database["mode"]
	except KeyError:
		pass
	finally:
		database.close()
	return mode

def set_value(mode):
	if not (mode in ("default", "regex", "findasyoutype")): raise ValueError
	try:
		database = open_database(basepath, "w")
		database["mode"] = mode
	finally:
		database.close()
	return

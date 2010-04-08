from SCRIBES.Utils import open_database
from os.path import join
basepath = join("PluginPreferences", "TemplateIndentation.gdb")

def get_value():
	try:
		value = True
		database = open_database(basepath, "r")
		value = database["indentation"]
	except KeyError:
		pass
	finally:
		database.close()
	return value

def set_value(indentation):
	try:
		database = open_database(basepath, "w")
		database["indentation"] = indentation
	finally:
		database.close()
	return

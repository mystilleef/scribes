from Utils import open_database
from os.path import join
basepath = join("Preferences", "Languages", "Font.gdb")

def get_value(language):
	try:
		font = __get_default_font()
		database = open_database(basepath, "r")
		font = database[language]
	except KeyError:
		if "def" in database: font = database["def"]
	finally:
		database.close()
	return font

def set_value(data):
	try:
		language, font = data
		database = open_database(basepath, "w")
		database[language] = font
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

def __get_default_font():
	try:
		font = "Monospace 11"
		gconf_font_location = "/desktop/gnome/interface/monospace_font_name"
		from gconf import client_get_default
		client = client_get_default()
		font = client.get_string(gconf_font_location)
		if font is None: font = "Monospace 11"
	except Exception:
		pass
	return font

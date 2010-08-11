from Utils import open_database
basepath = "position.gdb"

def get_window_position_from_database(uri):
	try:
		database = open_database(basepath, "r")
		window_position = database[uri]
	except KeyError:
		KEY = "<EMPTY>"
		window_position = database[KEY] if database.has_key(KEY) else None
	finally:
		database.close()
	return window_position

def update_window_position_in_database(uri, window_position):
	try:
		database = open_database(basepath, "w")
		database[str(uri)] = window_position
	finally:
		database.close()
	return

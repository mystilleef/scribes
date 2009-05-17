from Utils import open_database
basepath = "position.gdb"

def get_window_position_from_database(uri):
	try:
		database = open_database(basepath, "r")
		window_position = database[uri]
	except KeyError:
		window_position = None
	finally:
		database.close()
	return window_position

def update_window_position_in_database(uri, data):
	try:
		database = open_database(basepath, "w")
		database[str(uri)] = data
	finally:
		database.close()
	return

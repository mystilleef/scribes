from Utils import open_database
basepath = "cursor.gdb"

def get_value(uri):
	try:
		cursor_position = 0, 0
		database = open_database(basepath, "r")
		cursor_position = database[uri]
	except KeyError:
		pass
	finally:
		database.close()
	return cursor_position

def set_value(uri, cursor_position):
	try:
		database = open_database(basepath, "w")
		database[str(uri)] = cursor_position
	finally:
		database.close()
	return

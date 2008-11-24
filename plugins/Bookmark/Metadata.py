from SCRIBES.Utils import open_database
basepath = "bookmark.gdb"

def get_value(uri):
	try:
		uri = str(uri)
		database = open_database(basepath, "r")
		bookmarks = database[uri] if database.has_key(uri) else None
	finally:
		database.close()
	return bookmarks

def set_value(uri, data):
	try:
		if uri in (None, ""): return
		database = open_database(basepath, "w")
		uri = str(uri)
		if data:
			database[uri] = data
		else:
			if database.has_key(uri): del database[uri]
	finally:
		database.close()
	return

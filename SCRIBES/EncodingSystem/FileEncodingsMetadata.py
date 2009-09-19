from SCRIBES.Utils import open_database
basepath = "Preferences/FileEncodings.gdb"

def get_value(uri):
	try:
		value = "utf-8"
		database = open_database(basepath, "r")
		value = database[str(uri)]
	except KeyError:
		pass
	finally:
		database.close()
	return value

def set_value(uri, encoding):
	try:
		database = open_database(basepath, "w")
		database[str(uri)] = encoding
		__remove_utf8_uris(database)
	finally:
		database.close()
	return

def __remove_utf8_uris(database):
	# Remove uris with utf-8 encodings. We don't need them.
	utf8_uris = [uri for uri, encoding in database.iteritems() if encoding =="utf-8"]
	print utf8_uris
	for uri in utf8_uris: del database[str(uri)]
	return

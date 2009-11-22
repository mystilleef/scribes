from SCRIBES.Utils import open_database
from os.path import join
basepath = join("Preferences", "FileEncodings.gdb")

def get_value(uri):
	try:
		encoding = "utf-8"
		database = open_database(basepath, "r")
		encoding = database[str(uri)]
	except KeyError:
		pass
	finally:
		database.close()
	return encoding

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
	for uri in utf8_uris: del database[str(uri)]
	return
